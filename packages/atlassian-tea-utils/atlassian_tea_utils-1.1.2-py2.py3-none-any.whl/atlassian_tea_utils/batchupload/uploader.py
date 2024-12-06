import json
import logging
import time
import uuid
from typing import Iterable, Tuple, Union

import requests

from atlassian_tea_utils.atlas.auth import possibly_get_auth_from_atlas_cli

DATA_PORTAL_URL = "https://data-portal.internal.atlassian.com"

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


def get_data_portal_session(auth_header_value: str) -> requests.Session:
    """
    Returns a session with the data portal service.

    Parameters
    ----------
    auth_header_value : str
        The authorization header value.

    Returns
    -------
    requests.Session
        The session with the data portal service.
    """
    session = requests.Session()
    session.headers = {"Accept": "application/json", "Authorization": auth_header_value}
    return session


def upload_file(
    session: requests.Session, flow_id: Union[str, uuid.UUID], json_items: Iterable[str]
) -> Tuple[str, str]:
    """
    Uploads a file to the data portal service.

    Parameters
    ----------
    session : requests.Session
        The session with the data portal service.
    flow_id : Union[str, uuid.UUID]
        The flow ID.
    json_items : Iterable[str]
        The JSON items to upload.

    Returns
    -------
    Tuple[str, str]
        The task ID and file ID.
    """
    upload_response = session.post(
        f"{DATA_PORTAL_URL}/api/sim/batchupload/v1/flow/{flow_id}/files",
        data="\n".join(json_items),
        headers={
            "Content-Type": "application/jsonlines",
        },
    )
    upload_response.raise_for_status()
    file_upload_data = upload_response.json()
    task_id = file_upload_data["task_id"]
    file_id = file_upload_data["file_id"]
    if flow_id != file_upload_data["flow_id"]:
        raise RuntimeError(
            f"Invalid flow_id {file_upload_data['flow_id']}, expected {flow_id}"
        )
    logger.debug(
        f"Uploaded data to flow ID {flow_id} with file ID {file_id} returned "
        f"task id {task_id}."
    )
    return task_id, file_id


def wait_for_run_finish(
    session: requests.Session,
    flow_id: Union[str, uuid.UUID],
    file_id: Union[str, uuid.UUID],
) -> bool:
    """
    Waits for the run to finish.

    Parameters
    ----------
    session : requests.Session
        The session with the data portal service.
    flow_id : Union[str, uuid.UUID]
        The flow ID.
    file_id : Union[str, uuid.UUID]
        The file ID.

    Returns
    -------
    bool
        True if the run was successful, False otherwise.
    """
    # Check on the run until it's finished
    final_states = {"SUCCESS", "FAILED", "UPLOAD_FAILED"}
    other_states = {
        "RUNNING",
        "CREATING",
        "CREATED",
        "UPLOADING",
        "UPLOADED",
        "APPENDING",
        "DELETING",
    }
    while True:
        file_status_response = session.get(
            f"{DATA_PORTAL_URL}/api/sim/batchupload/v1/flow/{flow_id}/files/{file_id}"
        )
        file_status_response.raise_for_status()
        file_status_data = file_status_response.json()
        run_status = file_status_data["status"]
        if run_status in final_states:
            logger.info(
                f"Upload for file_id {file_id} reached status {run_status}, stopping"
            )
            if run_status == "SUCCESS":
                return True
            elif run_status == "FAILED":
                error_message = file_status_data.get("error", "")
                logger.error(
                    f"Run for file_id {file_id} reached {run_status} with error message "
                    f'"{error_message}"'
                )
                logger.error(json.dumps(file_status_data, indent=4))
                raise RuntimeError("Upload failed")
            else:
                raise ValueError(f"Final state {run_status} not handled")
        if run_status not in other_states:
            logger.error(
                f"Received unknown state {run_status} for run with file_id {file_id}, "
                f"returning to avoid infinite loop. This call may have "
                f"succeeded, we just don't know what's happening here."
            )
            raise RuntimeError(f"Unknown run state {run_status}")
        logger.debug(
            f"Upload status for file_id {file_id} is {run_status}, waiting for it to "
            f"complete."
        )
        time.sleep(1)


def send_to_socrates(
    json_items: Iterable[str],
    flow_id: Union[str, uuid.UUID],
    zone: str,
    table: str,
    data_portal_session: requests.Session,
) -> None:
    """
    Sends data to Socrates.

    Parameters
    ----------
    json_items : Iterable[str]
        The JSON items to send.
    flow_id : Union[str, uuid.UUID]
        The flow ID.
    zone : str
        The zone.
    table : str
        The table.
    data_portal_session : requests.Session
        The session with the data portal service.
    """
    logger.info("Starting upload to Socrates")
    logger.info(
        f"Uploading data to {zone}.{table} via "
        f"https://data-portal.internal.atlassian.com/batchupload/flows/{flow_id}"
    )
    task_id, file_id = upload_file(data_portal_session, flow_id, json_items)
    wait_for_run_finish(data_portal_session, flow_id, file_id)


def get_auth_value_for_data_portal(env: str) -> str:
    """
    Returns an appropriate Authorization header value for use with the data-portal service for the given env.

    Parameters
    ----------
    env : str
        The environment.

    Returns
    -------
    str
        The Authorization header value.
    """
    cmd = [
        "atlas",
        "slauth",
        "token",
        "-e",
        env,
        "--aud",
        "data-portal",
        "-o",
        "jwt",
    ]
    generate_error_message = f"Use `atlas slauth token -e {env} --aud data-portal -o jwt` to generate a token for data-portal"
    return possibly_get_auth_from_atlas_cli(
        for_service="data-portal",
        local_env_var="LOCAL_DATAPORTAL_TOKEN",
        command=cmd,
        fallback_command=generate_error_message,
    )
