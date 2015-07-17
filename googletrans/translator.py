# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import re
import requests
from collections import namedtuple
from future.moves.urllib.parse import quote

from . import __version__
from googletrans import urls
from googletrans.conversion import format_json
from googletrans.conversion import LANGUAGES, SPECIAL_CASES
from googletrans.response import Translated, Detected

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36 Gt/{0}'.format(__version__)

EXCLUDES = ['en', 'ca', 'fr']
RE_SRC = re.compile(',\[\["([\w]{2})"\]')

__agent = None
__headers = {
    'User-Agent': user_agent,
    'Referer': urls.TRANSLATOR,
}
def agent():
    """
    A requests session for translator
    """
    global __agent
    # create new object when object doesn't created yet.
    if not __agent:
        __agent = requests.Session()
        # this code may help to avoid a ban.
        __agent.get(urls.TRANSLATOR, headers=__headers)

    return __agent

def translate(text, dest='en', src='auto'):
    """
    Translate the passed text into destination language.

Basic usage: 
    >>> from googletrans import translator
    >>> translator.translate('안녕하세요.')
    <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
    >>> translator.translate('안녕하세요.', dest='ja')
    <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
    >>> translator.translate('veritas lux mea', src='la')
    <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

Advanced usage:
    >>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
    >>> for translation in translations:
    ...    print(translation.origin, ' -> ', translation.text)
    The quick brown fox  ->  빠른 갈색 여우
    jumps over  ->  이상 점프
    the lazy dog  ->  게으른 개

    :param text: the text you want to translate.
        you can pass this parameter as a list object, as shown in the advanced usage above.
    :param dest: the destination language you want to translate. (default: en)
    :param src: the source language you want to translate. (default: auto)

    :rtype: Translated
    :rtype: list (when list is passed)
    """
    if isinstance(text, list):
        result = []
        for item in text:
            translated = translate(item, dest=dest, src=src)
            result.append(translated)
        return result

    if src != 'auto' and src not in LANGUAGES.keys() and src in SPECIAL_CASES.keys():
        src = SPECIAL_CASES[src]
    elif src != 'auto' and src not in LANGUAGES.keys():
        raise ValueError('incorrect source language')

    if dest not in LANGUAGES.keys() and dest in SPECIAL_CASES.keys():
        dest = SPECIAL_CASES[dest]
    elif dest not in LANGUAGES.keys():
        raise ValueError('incorrect destination language')

    result = ''
    sess = agent() # acquire requests session
    origin = text
    text = quote(text)
    url = urls.TRANSLATE.format(query=text, src=src, dest=dest)
    r = sess.get(url, headers=__headers)

    """
    Resposne Sample (20150605)
    $ ./translate "republique" -d ko

    [[["공화국","republique"],[,,"gonghwagug"]],,"fr",,,[["republique",1,[["공화국",1000,true,false],["공화국의",0,true,false],["공화국에",0,true,false],["공화국에서",0,true,false]],[[0,10]],"republique",0,1]],0.94949496,,[["fr"],,[0.94949496]],,,[["명사",[[["communauté","démocratie"],""]],"république"]]]
    """
    data = format_json(r.text)

    # this code will be updated when the format is changed.
    translated = data[0][0][0]

    # actual source language that will be recognized by Google Translator when the
    # src passed is equal to auto.
    try:
        src = data[-1][0][0]
    except: pass

    pron = origin
    try:
        pron = data[0][1][-1]
    except: pass
    if dest in EXCLUDES and pron == origin:
        pron = translated

    # put final values into new Translated object
    result = Translated(src=src, dest=dest, origin=origin,
        text=translated, pronunciation=pron)

    return result

def detect(text):
    """
    Detect the language of a text.

Basic usage: 
    >>> from googletrans import translator
    >>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
    <Detected lang=ko confidence=0.27041003>
    >>> translator.detect('この文章は日本語で書かれました。')
    <Detected lang=ja confidence=0.64889508>
    >>> translator.detect('This sentence is written in English.')
    <Detected lang=en confidence=0.22348526>
    >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
    <Detected lang=eo confidence=0.10538048>

Advanced usage:
    >>> langs = translator.detect(['한국어', '日本語', 'English', 'le français'])
    >>> for lang in langs:
    ...    print(lang.lang, lang.confidence)
    ko 1
    ja 0.92929292
    en 0.96954316
    fr 0.043500196

    :param text: the text you want to detect.

    :rtype: Detected
    :rtype: list (when list is passed)
    """
    if isinstance(text, list):
        result = []
        for item in text:
            lang = detect(item)
            result.append(lang)
        return result

    result = ''
    sess = agent() # acquire requests session
    origin = text
    text = quote(text)
    url = urls.DETECT.format(query=text)
    r = sess.get(url, headers=__headers)
    data = format_json(r.text)

    # actual source language that will be recognized by Google Translator when the
    # src passed is equal to auto.
    src = ''
    confidence = 0.0
    try:
        src = ''.join(data[-1][0])
        confidence = data[-1][-1][0]
    except: pass
    result = Detected(lang=src, confidence=confidence)

    return result

def get_languages():
    return LANGUAGES

