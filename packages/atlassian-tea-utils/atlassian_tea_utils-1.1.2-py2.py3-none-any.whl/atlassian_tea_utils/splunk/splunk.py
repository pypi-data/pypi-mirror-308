import getpass
import json
import logging
import os
from functools import cached_property
from typing import Any, Dict, Generator, List

import requests

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


class Splunk:
    """
    A class to interact with Splunk server.

    Attributes
    ----------
    server_url : str
        The URL of the Splunk server.
    session : requests.Session
        The session object to interact with the Splunk server.

    Methods
    -------
    search(data: Dict[str, str]) -> Dict[str, Any]:
        Performs a non-streamed search on the Splunk server.
    isearch(data: Dict[str, str]) -> Generator[Dict[str, Any], None, None]:
        Performs a streamed search on the Splunk server.
    """

    @property
    def server_url(self) -> str:
        """The URL of the Splunk server."""
        return "https://nosso.splunk.paas-inf.net:8089/"

    @cached_property
    def session(self) -> requests.Session:
        """
        The session object to interact with the Splunk server.

        Returns
        -------
        requests.Session
            The session object.
        """

        new_session = requests.Session()
        new_session.params.update({"output_mode": "json"})  # type: ignore[union-attr]
        new_session.proxies.update(
            {"http": "http://edge-whitelistproxy01-prd-euwest1.net.atlassian.com:8080"}
        )  # type: ignore[union-attr]

        data = {
            "username": os.environ["USER"],
            "password": os.environ.get("PW") or getpass.getpass(),
            "cookie": "1",
        }
        response = new_session.post(
            f"{self.server_url}services/auth/login",
            data,
        )
        response.raise_for_status()

        return new_session

    def search(self, data: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Performs a non-streamed search on the Splunk server.

        Parameters
        ----------
        data : Dict[str, str]
            The search parameters.

        Returns
        -------
        List[Dict[str, Any]]
            The search results.
        """

        response = self.session.post(f"{self.server_url}services/search/jobs", data)
        response.raise_for_status()
        return response.json()["results"]

    def isearch(self, data: Dict[str, str]) -> Generator[Dict[str, Any], None, None]:
        """
        Performs a streamed search on the Splunk server.

        Parameters
        ----------
        data : Dict[str, str]
            The search parameters.

        Yields
        ------
        Dict[str, Any]
            The search results.
        """

        with self.session.post(
            f"{self.server_url}services/search/v2/jobs/export", data, stream=True
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    yield json.loads(line)["result"]
