import os
from typing import Optional

from openai import OpenAI


def get_openai_client(
    cloud_id: Optional[str] = None,
    use_case_id: Optional[str] = None,
    staff_context: Optional[str] = None,
    stage: str = "staging",
    region: str = "us-east-1",
) -> OpenAI:
    """
    Initializes and returns an OpenAI client.
    See https://developer.atlassian.com/platform/ai-gateway/intro/getting-started/
    for more information on the fields.

    Parameters
    ----------
    cloud_id : str, optional
        The cloud identifier. This is mandatory if the AI gateway is being used.
    use_case_id : str, optional
        The API key for authentication. This is mandatory if the AI gateway is
        being used.
    staff_context : str, optional
        UCT token. This is mandatory if the AI gateway is being used.
    stage : str, optional
        The stage of the environment (e.g., "staging", "production"). Default is
        "staging".
    region : str, optional
        The region of the environment (e.g., "us-east-1"). Default is
        "us-east-1".

    Returns
    -------
    OpenAI
        An instance of the OpenAI client.

    Notes
    -----
    The parameters `cloud_id`, `use_api_key`, and `staff_context` are mandatory if the
    AI gateway is being used. user_context is currently not supported.

    References
    ----------
    .. [1] https://bitbucket.org/atlassian/nl2jql-finetuning/src/75be9f7f783417c553a8dddfe1e3fccdbca86f75/src/nl2jql_finetuning/pipeline/openai_client.py
    """
    if os.getenv("OPENAI_API_KEY"):
        return OpenAI()
    if slauth_token := os.getenv("SLAUTH_TOKEN"):
        token = f"slauth {slauth_token}"
    elif asap_token := os.getenv("ASAP_TOKEN"):
        token = f"bearer {asap_token}"
    else:
        raise RuntimeError(
            "Expecting either OPENAI_API_KEY, SLAUTH_TOKEN or ASAP_TOKEN"
        )

    assert (
        cloud_id and use_case_id and staff_context
    ), "Expecting cloud_id, use_case_id and staff_context"

    return OpenAI(
        api_key="Unused value",
        base_url=f"https://ai-gateway.{region}.{stage}.atl-paas.net/v1/openai/v1",
        default_headers={
            "Content-Type": "application/json",
            "Authorization": token,
            # Required by ai-gateway
            "X-Atlassian-CloudId": cloud_id,
            "X-Atlassian-UseCaseId": use_case_id,
            "Staff-Context": staff_context,
        },
    )
