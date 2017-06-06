"""A conversion module for googletrans"""
from __future__ import print_function
import re
import json
from urllib.parse import urlencode


def build_params(query, src, dest, token):
    params = {
        'client': 't',
        'sl': src,
        'tl': dest,
        'hl': dest,
        'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'otf': 1,
        'ssel': 0,
        'tsel': 0,
        'tk': token,
        'q': query,
    }
    return urlencode(params, doseq=True)


def format_json(original):
    # save state
    states = []
    text = original
    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            nxt = text.find('"', p)
            states.append((p, text[p:nxt]))

    # replace all weired characters in text
    while text.find(',,') > -1:
        text = text.replace(',,', ',null,')
    while text.find('[,') > -1:
        text = text.replace('[,', '[null,')

    # recover state
    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            j = int(i / 2)
            nxt = text.find('"', p)
            # replacing a portion of a string
            # use slicing to extract those parts of the original string to be kept
            text = text[:p] + states[j][1] + text[nxt:]

    converted = json.loads(text)
    return converted


def rshift(val, n):
    """python port for '>>>'(right shift with padding)
    """
    return (val % 0x100000000) >> n
