"""A conversion module for googletrans"""

import json
import re
from typing import Any, Dict, Iterator, List, Optional, Tuple


def build_params(
    client: str,
    query: str,
    src: str,
    dest: str,
    token: str,
    override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "client": client,
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


def legacy_format_json(original: str) -> Dict[str, Any]:
    # save state
    states: List[Tuple[int, str]] = []
    text: str = original

    # save position for double-quoted texts
    for i, pos in enumerate(re.finditer('"', text)):
        # pos.start() is a double-quote
        p: int = pos.start() + 1
        if i % 2 == 0:
            nxt: int = text.find('"', p)
            states.append((p, text[p:nxt]))

    # replace all wiered characters in text
    while text.find(",,") > -1:
        text = text.replace(",,", ",null,")
    while text.find("[,") > -1:
        text = text.replace("[,", "[null,")

    # recover state
    for i, pos in enumerate(re.finditer('"', text)):
        p: int = pos.start() + 1
        if i % 2 == 0:
            j: int = int(i / 2)
            nxt: int = text.find('"', p)
            # replacing a portion of a string
            # use slicing to extract those parts of the original string to be kept
            text = text[:p] + states[j][1] + text[nxt:]

    converted: Dict[str, Any] = json.loads(text)
    return converted


def get_items(dict_object: Dict[str, Any]) -> Iterator[Tuple[Any, Any]]:
    for key in dict_object:
        yield key, dict_object[key]


def format_json(original: str) -> Dict[str, Any]:
    try:
        converted: Dict[str, Any] = json.loads(original)
    except ValueError:
        converted = legacy_format_json(original)

    return converted


def rshift(val: int, n: int) -> int:
    """python port for '>>>'(right shift with padding)"""
    return (val % 0x100000000) >> n
