import sys
import django
import numpy as np
import pandas as pd
from django.core.cache import cache
from django.db.models import Field
from django.utils.encoding import force_str as force_text


class ReadFrame:
    FieldDoesNotExist = (
        django.db.models.fields.FieldDoesNotExist
        if django.VERSION < (1, 8)
        else django.core.exceptions.FieldDoesNotExist
    )

    def __init__(
        self,
        qs,
        fieldnames=(),
        index_col=None,
        coerce_float=False,
        verbose=True,
        datetime_index=False,
        column_names=None,
    ):
        """
        Initialize the ReadFrame object with the parameters for creating a DataFrame.

        :param qs: The queryset or list of objects.
        :param fieldnames: The field names to include in the DataFrame.
        :param index_col: The name of the column to use as the index in the DataFrame.
        :param coerce_float: Whether to coerce all values to floats.
        :param verbose: Whether to print verbose output during the process.
        :param datetime_index: Whether to convert the index column to datetime if it contains datetime values.
        :param column_names: Custom column names for the DataFrame.
        """
        self.qs = qs
        self.fieldnames = pd.unique(np.array(fieldnames)) if fieldnames else ()
        self.index_col = index_col
        self.coerce_float = coerce_float
        self.verbose = verbose
        self.datetime_index = datetime_index
        self.column_names = column_names

        if self.index_col and self.index_col not in self.fieldnames:
            self.fieldnames = tuple(self.fieldnames) + (self.index_col,)
            if self.column_names:
                self.column_names = tuple(self.column_names) + (self.index_col,)

    @staticmethod
    def replace_from_choices(choices):
        def inner(values):
            return [choices.get(v, v) for v in values]

        return inner

    @staticmethod
    def get_model_name(model):
        """Returns the name of the model."""
        return model._meta.model_name

    @staticmethod
    def get_related_model(field):
        """Gets the related model from a related field."""
        model = None
        if hasattr(field, "related_model") and field.related_model:
            model = field.related_model
        elif hasattr(field, "rel") and field.rel:
            model = field.rel.to
        return model

    @classmethod
    def get_base_cache_key(cls, model):
        return (
            f"pandas_{model._meta.app_label}_{cls.get_model_name(model)}_%s_rendering"
        )

    @classmethod
    def replace_pk(cls, model):
        base_cache_key = cls.get_base_cache_key(model)

        def get_cache_key_from_pk(pk):
            return None if pk is None else base_cache_key % str(pk)

        def inner(pk_series):
            pk_series = pk_series.astype(object).where(pk_series.notnull(), None)
            cache_keys = pk_series.apply(get_cache_key_from_pk, convert_dtype=False)
            unique_cache_keys = list(filter(None, cache_keys.unique()))
            if not unique_cache_keys:
                return pk_series

            out_dict = cache.get_many(unique_cache_keys)
            if len(out_dict) < len(unique_cache_keys):
                out_dict = dict(
                    [
                        (base_cache_key % obj.pk, force_text(obj))
                        for obj in model.objects.filter(
                            pk__in=list(filter(None, pk_series.unique()))
                        )
                    ]
                )
                cache.set_many(out_dict)
            return list(map(out_dict.get, cache_keys))

        return inner

    @classmethod
    def build_update_functions(cls, fieldnames, fields):
        for fieldname, field in zip(fieldnames, fields):
            if not isinstance(field, Field):
                yield fieldname, None
            else:
                if field.choices:
                    choices = dict([(k, force_text(v)) for k, v in field.flatchoices])
                    yield fieldname, cls.replace_from_choices(choices)
                elif field.get_internal_type() == "ForeignKey":
                    yield fieldname, cls.replace_pk(cls.get_related_model(field))

    @classmethod
    def update_with_verbose(cls, df, fieldnames, fields):
        for fieldname, function in cls.build_update_functions(fieldnames, fields):
            if function is not None:
                df[fieldname] = function(df[fieldname])

    @classmethod
    def to_fields(cls, qs, fieldnames):
        """Get fields from a queryset based on the given fieldnames."""
        for fieldname in fieldnames:
            model = qs.model
            for fieldname_part in fieldname.split("__"):
                try:
                    field = model._meta.get_field(fieldname_part)
                except cls.FieldDoesNotExist:
                    try:
                        rels = model._meta.get_all_related_objects_with_model()
                    except AttributeError:
                        field = fieldname
                    else:
                        for relobj, _ in rels:
                            if relobj.get_accessor_name() == fieldname_part:
                                field = relobj.field
                                model = field.model
                                break
                else:
                    model = cls.get_related_model(field)
            yield field

    @staticmethod
    def is_values_queryset(qs):
        """Check if the queryset is a ValuesQuerySet."""
        if django.VERSION < (1, 9):
            return isinstance(qs, django.db.models.query.ValuesQuerySet)
        else:
            try:
                return qs._iterable_class == django.db.models.query.ValuesIterable
            except:
                return False

    @staticmethod
    def object_to_dict(obj, fields=None):
        """Convert a Django model instance to a dictionary based on specified fields."""
        if not fields:
            obj.__dict__.pop("_state")
            return obj.__dict__
        return {field: obj.__dict__.get(field) for field in fields}

    def read_frame(self):
        """
        Generate and return a DataFrame from the initialized queryset or list of objects.
        """
        qs = self.qs
        fieldnames = self.fieldnames
        index_col = self.index_col
        coerce_float = self.coerce_float
        verbose = self.verbose
        datetime_index = self.datetime_index
        column_names = self.column_names

        if fieldnames:
            fields = self.to_fields(qs, fieldnames)
        elif self.is_values_queryset(qs):
            annotation_field_names = list(qs.query.annotation_select)
            extra_field_names = list(qs.query.extra_select)
            select_field_names = list(qs.query.values_select)

            fieldnames = select_field_names + annotation_field_names + extra_field_names
            fields = [
                None if "__" in f else qs.model._meta.get_field(f)
                for f in select_field_names
            ] + [None] * (len(annotation_field_names) + len(extra_field_names))

            uniq_fields = set()
            fieldnames, fields = zip(
                *(
                    f
                    for f in zip(fieldnames, fields)
                    if f[0] not in uniq_fields and not uniq_fields.add(f[0])
                )
            )
        else:
            fields = qs.model._meta.fields
            fieldnames = [f.name for f in fields]
            fieldnames += list(qs.query.annotation_select.keys())

        if self.is_values_queryset(qs):
            recs = list(qs)
        else:
            recs = (
                list(qs.values_list(*fieldnames))
                if fieldnames
                else [self.object_to_dict(q) for q in qs]
            )

        df = pd.DataFrame.from_records(
            recs,
            columns=column_names if column_names else fieldnames,
            coerce_float=coerce_float,
        )

        if verbose:
            self.update_with_verbose(df, fieldnames, fields)

        if index_col is not None:
            df.set_index(index_col, inplace=True)

        if datetime_index:
            df.index = pd.to_datetime(df.index, errors="ignore")

        return df
