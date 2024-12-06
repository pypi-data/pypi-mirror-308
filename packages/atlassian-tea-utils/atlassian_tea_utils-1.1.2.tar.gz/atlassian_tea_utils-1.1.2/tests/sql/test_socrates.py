import time
from dataclasses import dataclass
from unittest.mock import Mock, call

import pytest
from databricks.sql.exc import ServerOperationError
from databricks.sql.types import Row

from atlassian_tea_utils.sql import databricks, socrates


@pytest.fixture()
def mock_expected_rows():
    return [
        Row(name="Alice", age=30),
        Row(name="Bob", age=40),
        Row(name="Charlie", age=50),
    ]


@pytest.fixture
def soc_table_not_available_error() -> ServerOperationError:
    return ServerOperationError(
        message="Error while reading file s3://atl-ai-zone-foo/foo/foo. java.io.EOFException",
        context={
            "diagnostic-info": "org.apache.hive.service.cli.HiveSQLException: Error running query: org.apache.spark.SparkException: Jo/..."
        },
    )


@pytest.fixture()
def mock_sleep(monkeypatch):
    fake_sleep = Mock(name="sleep")
    monkeypatch.setattr(
        time,
        "sleep",
        fake_sleep,
    )
    return fake_sleep


@pytest.fixture()
def mock_socrates_access_credentials(monkeypatch):
    fake_socrates_access_credentials = Mock(name="socrates_access_credentials")
    fake_socrates_access_credentials.return_value = ("access_token", "http://path")
    monkeypatch.setattr(
        socrates,
        "socrates_access_credentials",
        fake_socrates_access_credentials,
    )
    return fake_socrates_access_credentials


@pytest.fixture()
def mock_dbsql(monkeypatch):
    fake_dbsql = Mock(name="dbsql")
    monkeypatch.setattr(
        databricks,
        "dbsql",
        fake_dbsql,
    )
    return fake_dbsql


@dataclass
class Person:
    name: str
    age: int


def test_sql(mock_socrates_access_credentials, mock_dbsql, mock_expected_rows) -> None:
    # Given
    mock_dbsql.connect().cursor().fetchall.return_value = mock_expected_rows

    # When
    socrates._socrates.reset()
    result = socrates.sql("hi")

    # Then
    assert result == mock_expected_rows
    mock_dbsql.connect.assert_called_with(
        server_hostname="socrates-gateway.us-east-1.prod.atl-paas.net",
        http_path="http://path",
        access_token="access_token",
        use_inline_params=True,
    )
    mock_dbsql.connect().cursor().execute.assert_called_with("hi", {})
    mock_dbsql.connect().cursor().fetchall.assert_called()

    # When
    result = list(socrates.isql("some query", _cast=Person))

    # Then
    assert result == [
        Person(name="Alice", age=30),
        Person(name="Bob", age=40),
        Person(name="Charlie", age=50),
    ]


def test_isql(mock_socrates_access_credentials, mock_dbsql, mock_expected_rows) -> None:
    # Given
    mock_dbsql.connect().cursor().fetchall.return_value = mock_expected_rows

    # When
    socrates._socrates.reset()
    result = list(socrates.isql("some query", _cast=Person))

    # Then
    assert result == [
        Person(name="Alice", age=30),
        Person(name="Bob", age=40),
        Person(name="Charlie", age=50),
    ]
    mock_dbsql.connect.assert_called_with(
        server_hostname="socrates-gateway.us-east-1.prod.atl-paas.net",
        http_path="http://path",
        access_token="access_token",
        use_inline_params=True,
    )
    mock_dbsql.connect().cursor().execute.assert_called_with("some query", {})
    mock_dbsql.connect().cursor().fetchall.assert_called()


def test_general_failure(
    mock_socrates_access_credentials, mock_dbsql, mock_expected_rows
):
    # Given
    mock_dbsql.exc.RequestError = RuntimeError
    mock_dbsql.connect.side_effect = mock_dbsql.exc.RequestError

    # When
    socrates._socrates.reset()
    with pytest.raises(mock_dbsql.exc.RequestError):
        list(socrates.isql("some query", _cast=Person))

    # Then
    mock_dbsql.connect.assert_called_with(
        server_hostname="socrates-gateway.us-east-1.prod.atl-paas.net",
        http_path="http://path",
        access_token="access_token",
        use_inline_params=True,
    )


def test_io_failure(
    mock_sleep, mock_socrates_access_credentials, mock_dbsql, mock_expected_rows
):
    # Given
    # mock_sleep will reduce the sleeping time between retries
    class RequestError(Exception):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.context = {"http-code": 504}

    mock_dbsql.exc.RequestError = RequestError

    def raise_error(server_hostname, http_path, access_token, use_inline_params):
        raise mock_dbsql.exc.RequestError()

    mock_dbsql.connect.side_effect = raise_error

    # When
    socrates._socrates.reset()
    with pytest.raises(OSError):
        list(socrates.isql("some query", _cast=Person))

    # Then
    mock_sleep.assert_called()
    assert mock_sleep.call_args_list == [call(1), call(2), call(4), call(8)]


@pytest.mark.parametrize("method", [socrates.sql, socrates.isql])
def test_sql_and_isql_sleep_for_table_not_being_temporary_available_error_path(
    mock_sleep,
    mock_socrates_access_credentials,
    mock_dbsql,
    soc_table_not_available_error,
    method,
) -> None:
    # Given
    mock_dbsql.connect().cursor().execute.side_effect = [
        soc_table_not_available_error,
        soc_table_not_available_error,
        soc_table_not_available_error,
        soc_table_not_available_error,
        soc_table_not_available_error,
    ]

    # When
    socrates._socrates.reset()

    # Then
    with pytest.raises(ServerOperationError):
        list(method("select * from something"))

    mock_sleep.assert_any_call(60)

    assert mock_sleep.call_args_list == [
        call(60),
        call(1),
        call(60),
        call(2),
        call(60),
        call(4),
        call(60),
        call(8),
        call(60),
    ]


@pytest.mark.parametrize("method", [socrates.sql, socrates.isql])
def test_sql_and_isql_sleep_for_table_not_being_temporary_available_happy_path(
    mock_sleep,
    mock_socrates_access_credentials,
    mock_dbsql,
    soc_table_not_available_error,
    method,
) -> None:
    # Given
    expected = ["expected"]
    cursor = mock_dbsql.connect().cursor()

    cursor.fetchall.return_value = expected

    cursor.execute.side_effect = [soc_table_not_available_error, None]

    # When
    socrates._socrates.reset()

    # Then
    results = list(method("select something from something"))
    assert results == expected

    mock_sleep.assert_any_call(60)
    assert mock_sleep.call_args_list == [call(60), call(1)]
