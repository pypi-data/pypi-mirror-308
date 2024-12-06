import json
from typing import Dict

import pandas as pd
from django.db.models import Q
import dask.dataframe as dd

from sibi_dst.df_helper.plugins.django import ReadFrameDask, ReadFrame

conversion_map: Dict[str, callable] = {
    "CharField": lambda x: x.astype(str),
    "TextField": lambda x: x.astype(str),
    "IntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "AutoField": lambda x: pd.to_numeric(x, errors="coerce"),
    "BigIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "SmallIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "PositiveIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "PositiveSmallIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "FloatField": lambda x: pd.to_numeric(x, errors="coerce"),
    "DecimalField": lambda x: pd.to_numeric(x, errors="coerce"),
    "BooleanField": lambda x: x.astype(bool),
    "NullBooleanField": lambda x: x.astype(bool),
    "DateTimeField": lambda x: pd.to_datetime(x, errors="coerce"),
    "DateField": lambda x: pd.to_datetime(x, errors="coerce").dt.date,
    "TimeField": lambda x: pd.to_datetime(x, errors="coerce").dt.time,
    "DurationField": lambda x: pd.to_timedelta(x, errors="coerce"),
    # for JSONField, assuming JSON objects are represented as string in df
    "JSONField": lambda x: x.apply(json.loads),
    "ArrayField": lambda x: x.apply(eval),
    "UUIDField": lambda x: x.astype(str),
}


class DjangoLoadFromDb:
    df: pd.DataFrame
    def __init__(self, db_connection, db_query, db_params, logger, **kwargs):
        self.connection_config = db_connection
        self.debug = kwargs.pop('debug', False)
        self.verbose_debug = kwargs.pop('verbose_debug', False)
        self.logger = logger
        if self.connection_config.model is None:
            if self.debug:
                self.logger.critical('Model must be specified')
                if self.verbose_debug:
                    print('Model must be specified')
            raise ValueError('Model must be specified')

        self.query_config = db_query
        self.params_config = db_params
        self.params_config.parse_params(kwargs)


    def build_and_load(self):
        self.df=self._build_and_load()
        if self.df is not None:
            self._process_loaded_data()
        return self.df

    def _build_and_load(self)->pd.DataFrame:
        query = self.connection_config.model.objects.using(self.connection_config.connection_name)
        if not self.params_config.filters:
            # IMPORTANT: if no filters are provided show only the first n_records
            # this is to prevent loading the entire table by mistake
            queryset = query.all()[:self.query_config.n_records]
        else:
            q_objects = self.__build_query_objects(self.params_config.filters, self.query_config.use_exclude)
            queryset = query.filter(q_objects)
        if queryset.exists():
            self.df=ReadFrameDask(queryset, **self.params_config.df_params).read_frame()
        else:
            self.df=dd.from_pandas(pd.DataFrame(), npartitions=1)
        return self.df

    @staticmethod
    def __build_query_objects(filters: dict, use_exclude: bool):
        q_objects = Q()
        for key, value in filters.items():
            if not use_exclude:
                q_objects.add(Q(**{key: value}), Q.AND)
            else:
                q_objects.add(~Q(**{key: value}), Q.AND)
        return q_objects

    def _process_loaded_data(self):
        self._convert_columns()

        if self.params_config.field_map:
            if self.debug:
                self.logger.info(f'Renaming columns...{[col for col in self.params_config.field_map.keys()]}')
                if self.verbose_debug:
                    print(f'Renaming columns...{[col for col in self.params_config.field_map.keys()]}')

            # Convert to Dask Series for lazy operations
            set_to_keep1 = list(self.df.columns)  # Keep original order of columns in self.df
            set_to_keep2 = self.params_config.df_params.get('column_names', [])

            # Identify columns in set_to_keep2 that are not in set_to_keep1
            columns_to_add = [col for col in set_to_keep2 if col not in set_to_keep1]

            # Maintain order from set_to_keep1 and append missing columns from set_to_keep2
            columns_to_keep = set_to_keep1 + columns_to_add

            self.df = self.df[columns_to_keep]
            self.df = self.df.rename(columns=self.params_config.field_map)

    def _convert_columns(self):
        """
        Convert the data types of columns in the Dask DataFrame based on the field type in the Django model.
        """
        df = self.df
        if self.debug:
            self.logger.info(f'Converting columns: {[col for col in df.columns]}')

        model_fields = self.connection_config.model._meta.get_fields()

        # Define the type conversions based on field type
        conversions = {}

        for field in model_fields:
            field_name = field.name
            field_type = type(field).__name__

            if field_name in df.columns:
                if self.debug:
                    self.logger.debug(f"Found column {field_name} of type {field_type}")
                    if self.verbose_debug:
                        print(f"Found column {field_name} of type {field_type}")

                # Check if a conversion exists for this field type
                if field_type in conversion_map:
                    conversions[field_name] = conversion_map[field_type]
                else:
                    if self.debug:
                        self.logger.error(f"Field type {field_type} not found in conversion_map")
                        if self.verbose_debug:
                            print(f"Field type {field_type} not found in conversion_map")
            else:
                if self.debug:
                    self.logger.error(f"Column {field_name} not found in df.columns")
                    if self.verbose_debug:
                        print(f"Column {field_name} not found in df.columns")

        # Define meta with expected data types for each column after conversion
        meta = df.copy().head(0)
        for col, convert_func in conversions.items():
            try:
                # Apply the conversion function to an empty column to determine the output type
                meta[col] = convert_func(meta[col])
            except Exception as e:
                if self.debug:
                    self.logger.error(f"Error determining type for column {col}: {e}")
                    if self.verbose_debug:
                        print(f"Error determining type for column {col}: {e}")
                # Use object type as a fallback if the conversion type is undetermined
                meta[col] = pd.Series(dtype="object")

        # Apply conversions lazily using map_partitions
        self.df = df.map_partitions(
            lambda part: part.assign(**{col: func(part[col]) for col, func in conversions.items()}), meta=meta)

        if self.debug:
            for col in conversions:
                self.logger.info(f"Applied conversion to column {col}")
                if self.verbose_debug:
                    print(f"Applied conversion to column {col}")