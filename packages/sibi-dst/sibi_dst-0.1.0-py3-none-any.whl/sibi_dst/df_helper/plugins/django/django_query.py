from typing import Dict, Union, Optional

from pydantic import BaseModel, model_validator

query_defaults: Dict[str, Union[str, int, None]] = {
    "use_exclude": False,
    "n_records": 100,
    "dt_field": None,
    "use_dask": False,
    "as_dask": False
}

class QueryConfig(BaseModel):
    use_exclude: bool = False
    n_records: int = 0
    dt_field: Optional[str] = None
    use_dask: bool = False
    as_dask: bool = False

    @model_validator(mode='after')
    def check_n_records(self):
        if self.n_records < 0:
            raise ValueError('Number of records must be non-negative')
        return self

