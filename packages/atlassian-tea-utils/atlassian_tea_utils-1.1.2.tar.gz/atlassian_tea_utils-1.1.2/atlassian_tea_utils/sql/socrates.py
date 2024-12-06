import logging
from typing import Any, Callable, Generator, List, Tuple, Type, Union

from databricks.sql.types import Row

from .config import socrates_access_credentials, socrates_host
from .databricks import CustomRow, Databricks

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


class Socrates(Databricks):
    @property
    def access_credentials(self) -> Tuple[str, str, str]:
        """
        Returns access_token, http_path, and server_hostname.

        Returns
        -------
        Tuple[str, str, str]
            The access token, HTTP path, and server hostname.
        """
        access_token, http_path = socrates_access_credentials()
        return access_token, http_path, socrates_host()


_socrates: Databricks = Socrates()


def sql(
    statement: str,
    _cast: Union[Callable[..., Any], Type[CustomRow], None] = None,
    **kwargs: Any,
) -> List[Union[Any, CustomRow, Row]]:
    """
    Executes arbitrary SQL and returns a list of cast objects according to the `_cast` format or
    `Row` if no cast was returned. The lines are retrieved from socrates.

    Parameters
    ----------
    statement : str
        The SQL query in databricks/apache spark format supporting `%()s` substitutions.
    _cast : Union[Callable[..., Any], Type[CustomRow], None]
        A function or Class to apply to all the rows. It can be a lambda as well.
    kwargs : Any
        A generic list of parameters to be replaced from the statement as `%(param)s`.

    Returns
    -------
    List[Union[CustomRow, Row]]
        The result of the SQL query.
    """
    return list(isql(statement, _cast=_cast, **kwargs))


def isql(
    statement: str,
    _cast: Union[Callable[..., Any], Type[CustomRow], None] = None,
    **kwargs: Any,
) -> Generator[Union[Any, CustomRow, Row], None, None]:
    """
    Executes arbitrary SQL and generates lines in the `_cast` format or `Row` if no cast was returned.
    The lines are retrieved from socrates.

    Note: isql, unlikely sql, does not currently support retrying failed queries.

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

    yield from _socrates.isql(statement, _cast=_cast, **kwargs)
