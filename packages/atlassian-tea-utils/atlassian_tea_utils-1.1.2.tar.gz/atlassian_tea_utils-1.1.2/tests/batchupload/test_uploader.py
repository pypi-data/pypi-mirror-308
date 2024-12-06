import uuid
from unittest import mock

import pytest
from requests import Response

from atlassian_tea_utils.batchupload import uploader


@pytest.fixture(autouse=True)
def requests_request():
    with mock.patch("requests.Session.request") as request:
        yield request


@pytest.fixture
def sleep_mock():
    with mock.patch("time.sleep"):
        yield


def test_upload_file(requests_request):
    flow_id = uuid.uuid4()
    task_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.return_value = {
        "task_id": task_id,
        "flow_id": flow_id,
        "file_id": file_id,
    }
    request.return_value = response
    session = uploader.get_data_portal_session("example-auth")
    res_task_id, res_file_id = uploader.upload_file(session, flow_id, [])
    assert res_task_id == task_id
    assert res_file_id == file_id


def test_upload_file_flow_id_mismatch(requests_request):
    flow_id = uuid.uuid4()
    task_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.return_value = {
        "task_id": task_id,
        "flow_id": uuid.uuid4(),  # Expect this to cause an exception
        "file_id": file_id,
    }
    request.return_value = response
    session = uploader.get_data_portal_session("example-auth")
    with pytest.raises(RuntimeError):
        uploader.upload_file(session, flow_id, [])


def test_wait_for_run_to_finish_success(requests_request):
    flow_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.return_value = {
        "status": "SUCCESS",
    }
    request.return_value = response
    session = uploader.get_data_portal_session("a-value")
    assert uploader.wait_for_run_finish(session, flow_id, file_id)


def test_send_to_socrates(requests_request, sleep_mock) -> None:
    flow_id = uuid.uuid4()
    task_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.side_effect = [
        {
            "task_id": task_id,
            "flow_id": flow_id,
            "file_id": file_id,
        },
        {
            "status": "SUCCESS",
        },
    ]
    request.return_value = response
    session = uploader.get_data_portal_session("a-value")
    uploader.send_to_socrates([], flow_id, "prod", "egtable", session)


def test_wait_for_run_to_finish_wait_success(requests_request, sleep_mock):
    flow_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.side_effect = [
        {
            "status": "RUNNING",
        },
        {
            "status": "SUCCESS",
        },
    ]
    request.return_value = response
    session = uploader.get_data_portal_session("a-value")
    assert uploader.wait_for_run_finish(session, flow_id, file_id)


def test_wait_for_run_to_finish_failed(requests_request, sleep_mock):
    flow_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.return_value = {"status": "FAILED", "error": "Something failed"}
    request.return_value = response
    session = uploader.get_data_portal_session("a-value")
    with pytest.raises(RuntimeError):
        uploader.wait_for_run_finish(session, flow_id, file_id)


def test_wait_for_run_to_finish_unknown_state(requests_request, sleep_mock):
    flow_id = uuid.uuid4()
    file_id = uuid.uuid4()
    request = requests_request
    response = mock.create_autospec(Response)
    response.json.return_value = {
        "status": "UNKNOWN_STATE_RESPONSE",
        "error": "Something failed",
    }
    request.return_value = response
    session = uploader.get_data_portal_session("a-value")
    with pytest.raises(RuntimeError):
        uploader.wait_for_run_finish(session, flow_id, file_id)


def test_get_auth_value_for_data_portal() -> None:
    # Given
    expected = "A token"
    env = "prod"
    with mock.patch.object(uploader, "possibly_get_auth_from_atlas_cli") as mocked:
        mocked.return_value = expected

        # When
        result = uploader.get_auth_value_for_data_portal(env)

        # Then
        assert result == expected

        mocked.assert_called_with(
            for_service="data-portal",
            local_env_var="LOCAL_DATAPORTAL_TOKEN",
            command=[
                "atlas",
                "slauth",
                "token",
                "-e",
                env,
                "--aud",
                "data-portal",
                "-o",
                "jwt",
            ],
            fallback_command="Use `atlas slauth token -e prod --aud data-portal -o jwt` to generate a token for data-portal",
        )
