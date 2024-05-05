"""A conversion module for googletrans"""

import re
from typing import Any, Dict, List, Tuple, Union

import ujson


def build_params(
    query: str,
    src: str,
    dest: str,
    token: str,
    override: Union[Dict[str, Any], None] = None,
):
    """
    build_params is a helper function for Translator._translate

    Parameters
    ----------
    query : str
        the text to be translated
    src : str
        the source language
    dest : str
        the destination language
    token : str
        google translate token
    override : Union[Dict[str, Any], None], optional
        additional parameters, by default None

    Returns
    -------
    dict
        the build parameters
    """
    params = {
        "client": "webapp",
        "sl": src,
        "tl": dest,
        "hl": dest,
        "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],
        "ie": "UTF-8",
        "oe": "UTF-8",
        "otf": 1,
        "ssel": 0,
        "tsel": 0,
        "tk": token,
        "q": query,
    }

    if override is not None:
        for key, value in get_items(override):
            params[key] = value

    return params


def legacy_format_json(original: str):
    """
    legacy_format_json is a simple wrapper function to convert json strings to python objects

    Parameters
    ----------
    original : str
        a JSON string

    Returns
    -------
    any
        a python object
    """

    # save state
    states: List[Tuple[int, str]] = []
    text = original

    # save position for double-quoted texts
    for i, pos in enumerate(re.finditer('"', text)):
        # pos.start() is a double-quote
        p = pos.start() + 1
        if i % 2 == 0:
            nxt = text.find('"', p)
            states.append((p, text[p:nxt]))

    # replace all wiered characters in text
    while text.find(",,") > -1:
        text = text.replace(",,", ",null,")
    while text.find("[,") > -1:
        text = text.replace("[,", "[null,")

    # recover state
    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            j = int(i / 2)
            nxt = text.find('"', p)
            # replacing a portion of a string
            # use slicing to extract those parts of the original string to be kept
            text = text[:p] + states[j][1] + text[nxt:]

    converted = ujson.loads(text)
    return converted


def get_items(dict_object: Dict[Any, Any]):
    """
    get_items A generator function to iterate over all items in a dictionary

    Parameters
    ----------
    dict_object : Dict[Any, Any]
        a dictionary

    Yields
    ------
    Tuple[Any, Any]
        a tuple of key and value in every iteration
    """
    for key in dict_object:
        yield key, dict_object[key]


def format_json(original: str):
    """
    format_json is a simple wrapper function to convert json strings to python objects

    Parameters
    ----------
    original : str
        a JSON string

    Returns
    -------
    any
        a python object
    """

    try:
        converted = ujson.loads(original)
    except ValueError:
        converted = legacy_format_json(original)

    return converted


def rshift(val: int, n: int) -> int:
    """python port for '>>>'(right shift with padding)"""
    return (val % 0x100000000) >> n
