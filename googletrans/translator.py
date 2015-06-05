# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.

Basic usage: 
    >>> from googletrans import translator
    >>> translator.translate(u'안녕하세요.')
    <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
    >>> translator.translate(u'안녕하세요.', dest='ja')
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
"""
import re
import requests
from collections import namedtuple
from future.moves.urllib.parse import quote

from . import __version__
from googletrans import urls
from googletrans.translated import Translated

user_agent = 'PyGt/{0}'.format(__version__)

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

# translator.translate(text, to='')
def translate(text, dest='en', src='auto'):
    """
    Translate the passed text into destination language.

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

    # this code will be updated when the format is changed.
    # (I know this code is not really efficient and so sketchy.)
    translated = r.text.split('[[[')[1][1:].split('"')[0]
    # actual source language that will be recognized by Google Translator when the
    # src passed is equal to auto.
    try:
        src = RE_SRC.findall(r.text)[0]
    except: pass

    pron = origin
    if src not in EXCLUDES:
        try:
            pron_table = r.text.split('[[[')[1].split('[')[1]
            pron = pron_table.split('"')[1].split('"')[0]
        except: pass
    if dest in EXCLUDES:
        pron = translated

    # put final values into new Translated object
    result = Translated(src=src, dest=dest, origin=origin,
        text=translated, pronunciation=pron)

    return result
