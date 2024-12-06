import logging
import re
import time
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Callable, Dict, Generator, Optional, Tuple, Type, Union

from databricks import sql as dbsql
from databricks.sql import ServerOperationError
from databricks.sql.client import Connection, Cursor
from databricks.sql.types import Row
from retry import retry

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


class CustomRow:
    pass


class Databricks(ABC):
    """
    A class to interact with Databricks.

    Attributes
    ----------
    server_hostname : str
        The hostname of the Databricks server.
    access_token : str
        The access token to connect to the Databricks server.
    http_path : str
        The HTTP path to connect to the Databricks server.
    last_connection_time : Optional[datetime]
        The last time a connection was made to the Databricks server.
    reconnection_interval : timedelta
        The interval at which to reconnect to the Databricks server.2
    use_inline_params:  boolean
        If inline params should be used with Databricks.

    Methods
    -------
    reset() -> None:
        Resets the last connection time.
    _ensure_connection() -> None:
        Ensures a connection to the Databricks server.
    _connect() -> None:
        Connects to the Databricks server.
    _execute_query(statement: str, kwargs: Optional[Dict[str, str]] = None, table_unavailable_sleep_time: int = 60) -> None:
        Executes the given query.
    isql(statement: str, _cast: Optional[Callable[..., T]] = None, kwargs: Optional[Dict[str, str]] = None) -> Generator[Union[CustomRow, Row], None, None]:
        Executes arbitrary SQL and generates lines in the `_cast` format or `Row` is no cast was returned.
    """

    def __init__(self) -> None:
        """
        Initializes the Databricks with the given Socrates host.
        """

        self.cursor: Cursor
        self.connection: Connection

        self.server_hostname: str
        self.access_token: str
        self.http_path: str

        self.last_connection_time: Optional[datetime] = None
        self.reconnection_interval: timedelta = timedelta(minutes=15)
        self.use_inline_params: bool = True

    def reset(self) -> None:
        """
        Resets the last connection time.
        """

        self.last_connection_time = None

    def _ensure_connection(self) -> None:
        """
        Ensures a connection to the Databricks server.
        """

        # If we've connected in the last self.reconnection_interval then don't reconnect
        utc_now = datetime.now(timezone.utc)
        if (
            self.last_connection_time is not None
            and self.last_connection_time + self.reconnection_interval > utc_now
        ):
            logger.info(
                f"Not reconnecting to Databricks because interval {self.reconnection_interval} has not"
                f" passed ({utc_now - self.last_connection_time} since last connection)"
            )
            return

        (
            self.access_token,
            self.http_path,
            self.server_hostname,
        ) = self.access_credentials

        self._connect()

    @property
    @abstractmethod
    def access_credentials(self) -> Tuple[str, str, str]:
        """
        Returns access_token, http_path, and server_hostname.

        Returns
        -------
        Tuple[str, str, str]
            The access token, HTTP path, and server hostname.
        """
        raise NotImplementedError(
            "Please override this class and implement this property"
        )

    @retry(exceptions=IOError, tries=5, delay=1, backoff=2)
    def _connect(self) -> None:
        """
        Connects to the Databricks server.
        """

        logger.info(
            f"Connecting to databricks host {self.server_hostname} path {self.http_path}"
        )
        try:
            self.connection = dbsql.connect(
                server_hostname=self.server_hostname,
                http_path=self.http_path,
                access_token=self.access_token,
                use_inline_params=self.use_inline_params,
            )
        except dbsql.exc.RequestError as e:
            http_resp_code = getattr(e, "context", {}).get("http-code", None)
            if http_resp_code == 504:
                raise IOError(e)
            raise

        self.last_connection_time = datetime.now(timezone.utc)
        logger.info(f"Connected to databricks at {self.last_connection_time}.")
        self.cursor = self.connection.cursor()

    @retry(tries=5, delay=1, backoff=2)
    def _execute_query(
        self,
        statement: str,
        kwargs: Optional[
            Dict[str, str | int | float | datetime | date | bool | Decimal | None]
        ] = None,
        table_unavailable_sleep_time: int = 60,
    ) -> None:
        """
        Executes the given query.

        Parameters
        ----------
        statement : str
            The SQL query.
        kwargs : Optional[Dict[str, str]]
            The parameters to replace in the SQL query.
        table_unavailable_sleep_time : int
            The time to sleep when a table is not available.
        """

        try:
            self.cursor.execute(statement, kwargs)
        except ServerOperationError as e:
            if "Error while reading file" in e.message:
                logger.warning(
                    f"Sleeping for {table_unavailable_sleep_time} seconds due to a table not being available & then triggering a retry - {e.message}"
                )
                time.sleep(table_unavailable_sleep_time)
            raise

    def isql(
        self,
        statement: str,
        _cast: Union[Callable[..., Any], Type[CustomRow], None] = None,
        **kwargs: Any,
    ) -> Generator[Union[Any, CustomRow, Row], None, None]:
        """
        Executes arbitrary SQL and generates lines in the `_cast` format or `Row` is no cast was returned.

        Parameters
        ----------
        statement : str
            The SQL query in databricks/apache spark format supporting `%()s` substitutions.
        _cast : Union[Callable[..., Any], Type[CustomRow], None]
            A function or Class to apply to all the rows. It can be a lambda as well.
        kwargs : Any
            A generic list of parameters to be replaced from the statement as `%(param)s`.

        Yields
        ------
        Union[CustomRow, Row]
            The result of the SQL query.
        """

        self._ensure_connection()

        # The current parameter substitution done by databricks-sql-connector is to encapsulate in single quotes
        # but this doesn't work for database & table names in the Spark dialect. To resolve this, we encourage
        # users to use the `validate_table` function as in:
        # `f"SELECT * from {databricks.validate_table('table')} where id=%(id)s"`

        self._execute_query(statement, kwargs)

        for row in self.cursor.fetchall():
            if _cast is None:
                yield row
            else:
                yield _cast(*row)


def validate_table(table: str) -> str:
    """
    Validates the given table.

    Parameters
    ----------
    table : str
        The table to validate.

    Raises
    ------
    ValueError
        If the table is not valid.
    """

    validated_table = re.sub(r"[^a-zA-Z0-9_]", "", table)
    if validated_table != table:
        raise ValueError(
            f"Invalid table provided. Please provide a table.\n"
            f"Provided table: '{table}'\n"
            f"Valid table format: '{validated_table}'"
        )
    return table
