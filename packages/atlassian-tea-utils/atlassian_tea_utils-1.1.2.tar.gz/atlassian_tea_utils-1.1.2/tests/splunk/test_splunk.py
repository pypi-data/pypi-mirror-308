import unittest.mock
from unittest.mock import Mock, patch

import pytest
import requests
from requests.models import Response

from atlassian_tea_utils.splunk import Splunk


@pytest.fixture()
def mock_session(monkeypatch):
    fake_session = Mock(name="session", scope=requests.session)
    monkeypatch.setattr(
        Splunk,
        "session",
        fake_session,
    )
    return fake_session


@pytest.fixture()
def mock_response():
    response = Mock(spec=Response)
    response.json.return_value = {"results": "fake_results"}
    return response


@pytest.fixture()
def patch_env(monkeypatch) -> None:
    monkeypatch.setenv("PW", "some-value")
    monkeypatch.setenv("USER", "a-user")


def test_server_url(patch_env):
    # Given
    splunk = Splunk()

    # When
    server_url = splunk.server_url

    # Then
    assert server_url == "https://nosso.splunk.paas-inf.net:8089/"


@patch.object(requests, "Session")
def test_session(mock_session_class, patch_env):
    # Given
    mock_session = mock_session_class.return_value
    mock_session.post.return_value = Mock(status_code=200)

    # When
    splunk = Splunk()
    session = splunk.session

    # Then
    assert session == mock_session
    mock_session_class.assert_called_once()
    mock_session.post.assert_called_once_with(
        "https://nosso.splunk.paas-inf.net:8089/services/auth/login",
        {
            "username": unittest.mock.ANY,
            "password": unittest.mock.ANY,
            "cookie": "1",
        },
    )


def test_search(mock_session, mock_response, patch_env):
    # Given
    mock_session.post.return_value = mock_response
    splunk = Splunk()
    data = {"search": "fake_search"}

    # When
    result = splunk.search(data)

    # Then
    assert result == "fake_results"
    mock_session.post.assert_called_once_with(
        "https://nosso.splunk.paas-inf.net:8089/services/search/jobs", data
    )


def test_isearch(mock_session, patch_env):
    # Given
    splunk = Splunk()
    data = {"search": "fake_search"}
    expected = [{"seq": str(i)} for i in range(1, 4)]
    mock_response_context_manager = Mock()
    mock_response = Mock()

    mock_response_context_manager.__enter__ = Mock(return_value=mock_response)
    mock_response_context_manager.__exit__ = Mock(return_value=False)
    mock_response.iter_lines.return_value = iter(
        [
            b'{"something": null, "result": {"seq": "1"}}',
            b'{"something": null, "result": {"seq": "2"}}',
            b'{"something": null, "result": {"seq": "3"}}',
        ]
    )
    mock_session.post.return_value = mock_response_context_manager

    # When
    result = list(splunk.isearch(data))

    # Then
    assert result == expected
    mock_session.post.assert_called_once_with(
        "https://nosso.splunk.paas-inf.net:8089/services/search/v2/jobs/export",
        data,
        stream=True,
    )
    mock_response_context_manager.__enter__.assert_called_once()
    mock_response_context_manager.__exit__.assert_called_once()
    mock_response.iter_lines.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


def test_search_raise_for_status_exception(mock_session, mock_response, patch_env):
    # Given
    mock_response.raise_for_status.side_effect = requests.HTTPError
    mock_session.post.return_value = mock_response
    splunk = Splunk()
    data = {"search": "fake_search"}

    # When
    with pytest.raises(requests.HTTPError):
        splunk.search(data)

    # Then
    mock_session.post.assert_called_once_with(
        "https://nosso.splunk.paas-inf.net:8089/services/search/jobs", data
    )


def test_isearch_raise_for_status_exception(mock_session, patch_env):
    # Given
    splunk = Splunk()
    data = {"search": "fake_search"}
    mock_response_context_manager = Mock()
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError

    mock_response_context_manager.__enter__ = Mock(return_value=mock_response)
    mock_response_context_manager.__exit__ = Mock(return_value=False)
    mock_session.post.return_value = mock_response_context_manager

    # When
    with pytest.raises(requests.HTTPError):
        list(splunk.isearch(data))

    # Then
    mock_session.post.assert_called_once_with(
        "https://nosso.splunk.paas-inf.net:8089/services/search/v2/jobs/export",
        data,
        stream=True,
    )
    mock_response_context_manager.__enter__.assert_called_once()
    mock_response_context_manager.__exit__.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
