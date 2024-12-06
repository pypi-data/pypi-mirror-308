import asyncio
from typing import Union, Optional

import dask.dataframe as dd
import pandas as pd

from sibi_dst.utils import Logger, ParquetSaver
from .plugins.django import *
from .plugins.http import HttpConfig
from .plugins.parquet import ParquetConfig

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')


class DfHelper:
    df: Union[dd.DataFrame, pd.DataFrame] = None
    plugin_db_connection: ConnectionConfig = None
    plugin_db_query: QueryConfig = None
    plugin_db_params: ParamsConfig = None
    plugin_parquet: ParquetConfig = None
    plugin_http: HttpConfig = None
    parquet_filename: str = None
    logger: Logger

    def __init__(self, source='django_db', **kwargs):
        self.source = source
        self.logger = logger
        self.debug = kwargs.setdefault("debug", False)
        self.verbose_debug = kwargs.setdefault("verbose_debug", False)
        self.parquet_storage_path = kwargs.setdefault("parquet_storage_path", None)
        kwargs.setdefault("live", True)
        self.post_init(**kwargs)

    def post_init(self, **kwargs):
        if self.source == 'django_db':
            self.plugin_db_connection = self.__get_config(ConnectionConfig, connection_defaults, kwargs)
            self.plugin_db_query = self.__get_config(QueryConfig, query_defaults, kwargs)
            self.plugin_db_params = self.__get_config(ParamsConfig, params_defaults, kwargs)
        elif self.source == 'parquet':
            self.parquet_filename = kwargs.setdefault("parquet_filename", None)
            self.plugin_parquet = ParquetConfig(**kwargs)
        elif self.source == 'http':
            self.plugin_http = HttpConfig(**kwargs)

    @staticmethod
    def __get_config(config_class, defaults, kwargs):
        keys = defaults.keys()
        options = {k: kwargs.pop(k, defaults[k]) for k in keys}
        return config_class(**options)

    def load(self, **options):
        # this will be the universal method to load data from a df irrespective of the source
        return self._load(**options)

    def _load(self, **options):
        if self.source == 'django_db':
            return self._load_from_db(**options)
        elif self.source == 'parquet':
            return self._load_from_parquet()
        elif self.source == 'http':
            if asyncio.get_event_loop().is_running():
                return self._load_from_http(**options)
            else:
                return asyncio.run(self._load_from_http(**options))


    def _load_from_db(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        try:
            loader_plugin = DjangoLoadFromDb(
                self.plugin_db_connection,
                self.plugin_db_query,
                self.plugin_db_params,
                self.logger,
                **options
            )
            self.df = loader_plugin.build_and_load()
            self.logger.info("Data successfully loaded from django database.")
        except Exception as e:
            self.logger.error(f"Failed to load data from django database: {e}")
            self.df = None

        return self.df

    async def _load_from_http(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        """Delegate asynchronous HTTP data loading to HttpDataSource plugin."""
        if self.plugin_http:
            self.df = await self.plugin_http.fetch_data(**options)
            return self.df
        else:
            self.logger.error("HTTP plugin not configured properly.")
            return None

    def save_to_parquet(self, parquet_filename: Optional[str] = None):
        ps = ParquetSaver(self.df, self.parquet_storage_path, self.logger)
        ps.save_to_parquet(parquet_filename)


    def _load_from_parquet(self) -> Union[pd.DataFrame, dd.DataFrame]:
        self.df = self.plugin_parquet.load_files()
        return self.df
