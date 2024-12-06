import os
from unittest.mock import patch, sentinel

import pytest

from atlassian_tea_utils.ai.ai import get_openai_client


@pytest.fixture
def mock_openai():
    with patch("atlassian_tea_utils.ai.ai.OpenAI", autospec=True) as mock:
        mock.return_value = sentinel.client
        yield mock


def test_openai_api_key(mock_openai):
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy_key"}, clear=True):
        client = get_openai_client()
        mock_openai.assert_called_once_with()
        assert client is sentinel.client


def test_slauth_token(mock_openai):
    with patch.dict(os.environ, {"SLAUTH_TOKEN": "dummy_slauth_token"}, clear=True):
        client = get_openai_client(
            cloud_id="cloud",
            use_case_id="api_key",
            staff_context="mock staff context token",
        )
        mock_openai.assert_called_once_with(
            api_key="Unused value",
            base_url="https://ai-gateway.us-east-1.staging.atl-paas.net/v1/openai/v1",
            default_headers={
                "Content-Type": "application/json",
                "Authorization": "slauth dummy_slauth_token",
                "X-Atlassian-CloudId": "cloud",
                "X-Atlassian-UseCaseId": "api_key",
                "Staff-Context": "mock staff context token",
            },
        )
        assert client is sentinel.client


def test_asap_token(mock_openai):
    with patch.dict(os.environ, {"ASAP_TOKEN": "dummy_asap_token"}, clear=True):
        client = get_openai_client(
            cloud_id="cloud",
            use_case_id="api_key",
            staff_context="mock staff context token",
        )
        mock_openai.assert_called_once_with(
            api_key="Unused value",
            base_url="https://ai-gateway.us-east-1.staging.atl-paas.net/v1/openai/v1",
            default_headers={
                "Content-Type": "application/json",
                "Authorization": "bearer dummy_asap_token",
                "X-Atlassian-CloudId": "cloud",
                "X-Atlassian-UseCaseId": "api_key",
                "Staff-Context": "mock staff context token",
            },
        )
        assert client is sentinel.client


def test_no_tokens():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(
            RuntimeError,
            match="Expecting either OPENAI_API_KEY, SLAUTH_TOKEN or ASAP_TOKEN",
        ):
            get_openai_client()


def test_missing_parameters():
    with patch.dict(os.environ, {"SLAUTH_TOKEN": "dummy_slauth_token"}, clear=True):
        with pytest.raises(
            AssertionError, match="Expecting cloud_id, use_case_id and staff_context"
        ):
            get_openai_client()
