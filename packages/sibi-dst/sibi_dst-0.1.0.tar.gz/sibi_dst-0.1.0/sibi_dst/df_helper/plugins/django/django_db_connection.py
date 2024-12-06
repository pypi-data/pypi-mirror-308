from typing import Any, Dict, Union

from pydantic import BaseModel, model_validator

from .sql_model_builder import SqlModelBuilder

connection_defaults: Dict[str, Union[str, int, None]] = {
    "live": False,
    "connection_name": None,
    "table": None,
    "model": None,
}


class ConnectionConfig(BaseModel):
    live: bool = False
    connection_name: str = None
    table: str = None
    model: Any = None

    @model_validator(mode="after")
    def check_model(self):
        if self.connection_name is None:
            raise ValueError("Connection name must be specified")

        if self.live is False:
            if self.model is None:
                raise ValueError("Model must be specified")
            self.table = self.model._meta.db_table
        else:
            # if live is True, then connection_name and table must be specified
            if self.table is None:
                raise ValueError("Table name must be specified")
            self.model = SqlModelBuilder(
                connection_name=self.connection_name, table=self.table
            ).build_model()
        # After all checks, validate the connection
        self.validate_connection()
        return self

    def validate_connection(self):
        """Test if the database connection is valid by executing a simple query."""
        try:
            # Perform a simple query to test the connection
            self.model.objects.using(self.connection_name).exists()
        except Exception as e:
            raise ValueError(
                f"Failed to connect to the database '{self.connection_name}': {e}"
            )
