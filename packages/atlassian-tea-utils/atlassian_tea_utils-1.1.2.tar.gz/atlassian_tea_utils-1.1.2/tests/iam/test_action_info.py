from datetime import date as Date
from unittest.mock import Mock

import pytest
import requests
from requests.models import Response

from atlassian_tea_utils.iam import IamInformation


@pytest.fixture()
def fake_get(monkeypatch):
    fake_response = Mock(spec=Response)
    fake_response.content.decode.return_value = 'app.PolicyEditorConfig={"serviceMap": {"s3": {"Actions": ["ListBucket", "ListObjects"], "StringPrefix": "s3"}}}'
    fake_response.raise_for_status.return_value = None
    fake_get = Mock(return_value=fake_response)
    monkeypatch.setattr(requests, "get", fake_get)
    return fake_get


def test_iam_information(fake_get):
    # Given
    iam_info = IamInformation()

    # When
    data = iam_info.data

    # Then
    assert data == {
        "s3": {"Actions": ["ListBucket", "ListObjects"], "StringPrefix": "s3"}
    }
    assert isinstance(iam_info.retrieved, Date)
    fake_get.assert_called_with("https://awspolicygen.s3.amazonaws.com/js/policies.js")

    # When
    action_list = list(iam_info.generate_action_list)

    # Then
    assert action_list == [
        (iam_info.retrieved, "s3", "s3:ListBucket"),
        (iam_info.retrieved, "s3", "s3:ListObjects"),
    ]

    # When
    expanded_action = list(iam_info.expand_action("s3:*"))

    # Then
    assert expanded_action == ["s3:ListBucket", "s3:ListObjects"]

    # When
    expanded_action = list(iam_info.expand_action("s3:listo*"))

    # Then
    assert expanded_action == ["s3:ListObjects"]


def test_iam_information_invalid_content(fake_get):
    # Given
    fake_get.return_value.content.decode.return_value = "Invalid content"
    iam_info = IamInformation()

    # When / Then
    with pytest.raises(ValueError, match="The page changed the format"):
        iam_info.data
