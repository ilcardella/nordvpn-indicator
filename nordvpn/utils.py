import re
from typing import Any, Optional


def find_string_value(key: str, source: str) -> Optional[str]:
    """
    Find the string value associated with the specified key in the source string
    as pair "key:value"
    Return the value string of the parsed key otherwise it returns None
    """
    match = re.search(r"{}:\s(.*)".format(key), source)
    if match is None:
        return None
    return match.group(1).strip()


def find_bool_value(key: str, source: str) -> Optional[bool]:
    """
    Find the bool value associated with the specified key in the source string
    as pair "key:value"
    Return the value string of the parsed key otherwise it returns None
    """
    match = re.search(r"{}:\s(.*)".format(key), source)
    if match is None:
        return None
    value = match.group(1).strip()
    return value == "enabled" or value == "on" or value == "true"


def find_list_value(key: str, source: str) -> Optional[list[Any]]:
    """
    Find the list value associated with the specified key in the source string
    as pair "key:value". The list must be commad separated
    Return the value string of the parsed key otherwise it returns None
    """
    match = re.search(r"{}:\s(.*)".format(key), source)
    if match is None:
        return None
    value = match.group(1).strip()
    return value.split(sep=",")


def parse_words(raw: str) -> list[str]:
    """
    Search for any separated words from the raw input string.
    Returns a list of the extracted words.
    """
    if raw is None:
        return []
    parsed_list = re.findall(r"(\w{2,})+", raw)
    if parsed_list is None:
        return []
    return parsed_list
