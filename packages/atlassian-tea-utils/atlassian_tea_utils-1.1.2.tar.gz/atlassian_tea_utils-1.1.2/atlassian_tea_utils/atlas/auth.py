import logging
import os
import subprocess
import sys
from typing import List

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


def possibly_get_auth_from_atlas_cli(
    for_service: str,
    local_env_var: str,
    command: List[str],
    fallback_command: str,
    with_prefix: bool = True,
) -> str:
    """Returns an appropriate Authorization header value for use with various services."""
    if "PIPELINES_JWT_TOKEN" in os.environ:
        value = os.environ["PIPELINES_JWT_TOKEN"]
        if with_prefix:
            return f"Bearer {value}"
        return f"{value}"

    if local_env_var not in os.environ or os.environ[local_env_var] == "":
        if not sys.stdout.isatty() and "LOCAL_IDE_IN_USE" not in os.environ:
            raise RuntimeError(
                f"It looks like you're running locally but don't have {local_env_var} in your environment. Please run:\n{fallback_command}\nand export the result as {local_env_var}."
            )
        logger.info(f"Attempting to generate a token for {for_service}")
        try:
            process = subprocess.run(
                command, encoding="utf-8", stdout=subprocess.PIPE, check=True
            )
            slauth_token = process.stdout.strip()
            logger.info(f"Finished generating a token for {for_service}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(fallback_command)
            raise RuntimeError(
                f"Error executing the given auth command, try running: {fallback_command}"
            )
    else:
        slauth_token = os.environ.get(local_env_var)  # type: ignore[assignment]

    if with_prefix:
        return f"SLAUTH {slauth_token}"
    return slauth_token
