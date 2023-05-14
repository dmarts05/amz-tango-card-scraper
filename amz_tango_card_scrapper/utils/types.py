"""Module for defining types."""

from typing import Dict, List, NewType, Union

"""A custom type that encapsulates the structure of the config file."""
ConfigFile = NewType(
    "ConfigFile", Dict[str, Union[Dict[str, str], List[str], Dict[str, bool]]]
)
