"""
This module provides functions to retrieve different settings. It encapsulates the source.
"""

import logging
import os
import subprocess
import sys
from typing import Optional, Tuple

import click

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


def is_a_tty() -> bool:
    """
    Checks if the code is running in a TTY.

    Returns
    -------
    bool
        True if running as a TTY, False otherwise.
    """
    return sys.stdout.isatty()


def local_ide_in_use() -> Optional[str]:
    """
    Checks the LOCAL_IDE_IN_USE environment variable.

    Returns
    -------
    Optional[str]
        The setting contents or None if missing.
    """
    return os.environ.get("LOCAL_IDE_IN_USE")


def pipelines_jwt_token() -> Optional[str]:
    """
    Checks the PIPELINES_JWT_TOKEN environment variable.

    Returns
    -------
    Optional[str]
        The setting contents or None if missing.
    """
    return os.environ.get("PIPELINES_JWT_TOKEN")


def pipelines_path() -> str:
    """
    Returns the path to connect to socrates on pipelines.

    Returns
    -------
    str
        A string with the path.
    """
    prefix_http_path = "/workspaces/atlassian-discover/jdbc?clusterPath="
    http_path = "sql/1.0/endpoints/baf1e48f949e4ba2"
    return prefix_http_path + http_path


def socrates_gateway_slauth_token_from_env() -> Optional[str]:
    """
    Checks the SOCRATES_GATEWAY_SLAUTH_TOKEN environment variable.

    Returns
    -------
    Optional[str]
        The setting contents or None if missing.
    """
    return os.environ.get("SOCRATES_GATEWAY_SLAUTH_TOKEN")


def socrates_atlas_slauth_token_cmd() -> str:
    """
    Returns the shell command to retrieve the SOCRATES_GATEWAY_SLAUTH_TOKEN.

    Returns
    -------
    str
        A string with the command.
    """
    return "atlas slauth token -e prod -a socrates-gateway -m"


def socrates_gateway_slauth_token() -> str:
    """
    Tries several methods to find the slauth access token.

    1) Check the environment
    2) If on a TTY (interactive mode):
       2.1 Use the Atlas CLI to retrieve it
       2.2 Ask for it on a prompt line

    Returns
    -------
    str
        A string with the slauth access token.
    """
    auth_token = socrates_gateway_slauth_token_from_env()
    cmd = socrates_atlas_slauth_token_cmd()

    if auth_token:
        return auth_token
    if not is_a_tty() and local_ide_in_use() is None:
        raise RuntimeError(
            "It looks like you're running locally but don't have SOCRATES_GATEWAY_SLAUTH_TOKEN in your environment. Please run:\n"
            f"{cmd}\n"
            "and export the result as SOCRATES_GATEWAY_SLAUTH_TOKEN."
        )

    logger.info("Attempting to generate a token for socrates-gateway")
    try:
        process = subprocess.run(
            cmd.split(" "),
            encoding="utf-8",
            stdout=subprocess.PIPE,
            check=True,
            timeout=180,
        )
        return process.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo(f"Use `{cmd}` to generate a token for socrates-gateway.")
        return click.prompt("Enter your slauth token for socrates-gateway: ", type=str)


def socrates_access_credentials() -> Tuple[str, str]:
    """
    Returns the socrates access token and path. Depending on the environment setup it will find
    the correct credentials to return.

    Returns
    -------
    Tuple[str, str]
        A tuple with the two values in it.
    """
    access_token = pipelines_jwt_token()
    if access_token is not None:
        # Authenticate using the PIPELINES_JWT_TOKEN if we are running in CI
        return access_token, pipelines_path()
    else:
        return f"slauth:{socrates_gateway_slauth_token()}", "/jdbc"


def socrates_host() -> str:
    return "socrates-gateway.us-east-1.prod.atl-paas.net"
