import fnmatch
import json
import logging
from datetime import date as Date
from functools import cached_property
from typing import Any, Dict, Iterable, Optional, Tuple

import requests

logger: logging.Logger = logging.getLogger("tea").getChild(__name__)


class IamInformation:
    """
    A class to interact with AWS IAM information.

    Attributes
    ----------
    retrieved : Optional[Date]
        The date when the data was retrieved.

    Methods
    -------
    data() -> Dict[str, Any]:
        Downloads a JSON file from a given URL and lazily initialises data.
    generate_action_list() -> Iterable[Tuple[Date, str, str]]:
        Generates a list of actions.
    expand_action(action_pattern: str) -> Iterable[str]:
        Expands the action based on the given pattern.
    """

    def __init__(self) -> None:
        """Initializes the IamInformation with the retrieved date set to None."""
        self.retrieved: Optional[Date] = None

    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Downloads a JSON file from a given URL and lazily initialises data.

        Returns
        -------
        Dict[str, Any]
            The downloaded data.
        """

        url = "https://awspolicygen.s3.amazonaws.com/js/policies.js"
        initialisation = "app.PolicyEditorConfig="

        response = requests.get(url)
        content = response.content.decode("UTF8")
        response.raise_for_status()  # Raise an exception if the request was unsuccessful.
        if not content.startswith(initialisation):
            raise ValueError("The page changed the format")
        offset = len(initialisation)
        data = json.loads(content[offset:])["serviceMap"]
        self.retrieved = Date.today()

        return data

    @property
    def generate_action_list(self) -> Iterable[Tuple[Date, str, str]]:
        """
        Generates a list of actions.

        Yields
        ------
        Tuple[Date, str, str]
            The date when the data was retrieved, the service, and the action.
        """

        items = self.data.items()
        assert isinstance(self.retrieved, Date)

        for service, data in items:
            for action in data["Actions"]:
                yield self.retrieved, service, f"{data['StringPrefix']}:{action}"

    @cached_property
    def _get_action_dict(self) -> Dict[str, str]:
        """Returns a dictionary of actions."""
        return {action.lower(): action for _, _, action in self.generate_action_list}

    def expand_action(self, action_pattern: str) -> Iterable[str]:
        """
        Expands the action based on the given pattern.

        Parameters
        ----------
        action_pattern : str
            The action pattern. It can include the wildcard `*` to match everything (the one-character wildcard `?` is
            also supported)

        Yields
        ------
        str
            The expanded action.
        """

        for action in fnmatch.filter(self._get_action_dict, action_pattern.lower()):
            yield self._get_action_dict[action]
