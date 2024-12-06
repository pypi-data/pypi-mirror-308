import datetime
from pathlib import Path
from typing import Optional

import dask.dataframe as dd
import fsspec
import pandas as pd
import pyarrow as pa


class ParquetSaver:
    def __init__(self, df_result, parquet_storage_path, logger):
        self.df_result = df_result
        self.parquet_storage_path = parquet_storage_path
        self.logger = logger

    def save_to_parquet(self, parquet_filename: Optional[str] = None):
        full_path = self._construct_full_path(parquet_filename)

        if len(self.df_result) == 0:
            self.logger.warning('No data to save')
            return  # Exit early if there's no data to save

        # Ensure directory exists and clear if necessary
        self._ensure_directory_exists(full_path, clear_existing=True)

        # Define schema and save DataFrame to parquet
        schema = self._define_schema()
        self._convert_dtypes(schema)
        self._save_dataframe_to_parquet(full_path, schema)

    def _define_schema(self) -> pa.Schema:
        """Define a PyArrow schema dynamically based on df_result column types."""
        type_mapping = {
            'object': pa.string(),
            'string': pa.string(),
            'Int64': pa.int64(),
            'int64': pa.int64(),
            'float64': pa.float64(),
            'bool': pa.bool_(),
            'datetime64[ns]': pa.timestamp('ns'),
            'date': pa.string()  # Convert dates to string as fallback
        }

        fields = []
        for col in self.df_result.columns:
            # Identify the dtype of each column
            col_dtype = str(self.df_result[col].dtype)
            # Map dtype to pyarrow type, default to string if type not found
            arrow_type = type_mapping.get(col_dtype, pa.string())
            fields.append(pa.field(col, arrow_type))

        return pa.schema(fields)

    def _convert_dtypes(self, schema: pa.Schema):
        """Convert DataFrame columns to match the specified schema."""
        for field in schema:
            col_name = field.name
            if col_name in self.df_result.columns:
                if field.type == pa.string():
                    self.df_result[col_name] = self.df_result[col_name].astype(str)
                elif field.type == pa.int64():
                    self.df_result[col_name] = pd.to_numeric(self.df_result[col_name], errors='coerce').fillna(0).astype('int64')
                elif field.type == pa.float64():
                    self.df_result[col_name] = pd.to_numeric(self.df_result[col_name], errors='coerce')
                elif field.type == pa.bool_():
                    self.df_result[col_name] = self.df_result[col_name].astype(bool)
                elif field.type == pa.timestamp('ns'):
                    self.df_result[col_name] = pd.Series(pd.to_datetime(self.df_result[col_name], errors='coerce').values)

    def _construct_full_path(self, parquet_filename: Optional[str]) -> Path:
        """Construct and return the full path for the parquet file."""
        fs, base_path = fsspec.core.url_to_fs(self.parquet_storage_path)
        parquet_filename = parquet_filename or "default.parquet"
        return Path(base_path) / parquet_filename

    @staticmethod
    def _ensure_directory_exists(full_path: Path, clear_existing=False):
        """Ensure that the directory for the path exists, clearing it if specified."""
        fs, _ = fsspec.core.url_to_fs(str(full_path))
        directory = str(full_path.parent)

        if fs.exists(directory):
            if clear_existing:
                fs.rm(directory, recursive=True)
        else:
            fs.mkdirs(directory, exist_ok=True)

    def _save_dataframe_to_parquet(self, full_path: Path, schema: pa.Schema):
        """Save the DataFrame to parquet with fsspec using specified schema."""
        fs, _ = fsspec.core.url_to_fs(str(full_path))
        if fs.exists(full_path):
            fs.rm(full_path, recursive=True)
        if isinstance(self.df_result, dd.DataFrame):
            self.df_result.to_parquet(
                str(full_path), engine="pyarrow", schema=schema, write_index=False
            )
        elif isinstance(self.df_result, pd.DataFrame):
            dd.from_pandas(self.df_result, npartitions=1).to_parquet(
                str(full_path), engine="pyarrow", schema=schema, write_index=False
            )

class FilePathGenerator:
    def __init__(self, base_path=''):
        self.base_path = base_path.rstrip('/')
        self.fs = fsspec.filesystem("file") if "://" not in base_path else fsspec.filesystem(base_path.split("://")[0])

    def generate_file_paths(self, start_date, end_date):
        """
        Generate monthly directory patterns instead of individual files for Dask to read more efficiently.

        :param start_date: Start date for generating patterns.
        :param end_date: End date for generating patterns.
        :return: List of file path patterns.
        """
        start_date = self._convert_to_datetime(start_date)
        end_date = self._convert_to_datetime(end_date)

        patterns = []
        curr_date = start_date

        while curr_date <= end_date:
            year = curr_date.year
            month = str(curr_date.month).zfill(2)
            month_pattern = f"{self.base_path}/{year}/{month}/*/*.parquet"

            # Check if any files match the monthly pattern and only add if files exist
            if self.fs.glob(month_pattern):
                patterns.append(month_pattern)

            curr_date = self._increment_month(curr_date)

        return patterns

    @staticmethod
    def _convert_to_datetime(date):
        if isinstance(date, str):
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        return date

    @staticmethod
    def _increment_month(curr_date):
        # Move to the first day of the next month
        if curr_date.month == 12:
            return datetime.datetime(curr_date.year + 1, 1, 1)
        else:
            return datetime.datetime(curr_date.year, curr_date.month + 1, 1)