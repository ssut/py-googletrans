# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import requests

from googletrans import urls, utils
from googletrans.compat import PY3
from googletrans.gtoken import TokenAcquirer
from googletrans.constants import DEFAULT_USER_AGENT, LANGUAGES, SPECIAL_CASES
from googletrans.models import Translated, Detected


EXCLUDES = ('en', 'ca', 'fr')


class Translator(object):

    def __init__(self, user_agent=DEFAULT_USER_AGENT):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
        })
        self.token_acquirer = TokenAcquirer(session=self.session)

        # Use HTTP2 Adapter if hyper is installed
        try:  # pragma: nocover
            from hyper.contrib import HTTP20Adapter
            self.session.mount(urls.BASE, HTTP20Adapter())
        except ImportError:  # pragma: nocover
            pass

    def _translate(self, text, dest='en', src='auto'):
        if src != 'auto':
            if src not in LANGUAGES.keys() and src in SPECIAL_CASES.keys():
                src = SPECIAL_CASES[src]
            elif src not in LANGUAGES.keys():
                raise ValueError('invalid source language')

        if dest not in LANGUAGES.keys():
            if dest in SPECIAL_CASES.keys():
                dest = SPECIAL_CASES[dest]
            else:
                raise ValueError('invalid destination language')

        if not PY3 and isinstance(text, str):  # pragma: nocover
            text = text.decode('utf-8')

        token = self.token_acquirer.do(text)
        params = utils.build_params(query=text, src=src, dest=dest,
                                    token=token)
        r = self.session.get(urls.TRANSLATE, params=params)

        data = utils.format_json(r.text)
        return data

    def translate(self, text, dest='en', src='auto'):
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
                translated = self.translate(item, dest=dest, src=src)
                result.append(translated)
            return result

        origin = text
        data = self._translate(text, dest, src)

        # this code will be updated when the format is changed.
        translated = data[0][0][0]

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        try:
            src = data[-1][0][0]
        except Exception:  # pragma: nocover
            pass

        pron = origin
        try:
            pron = data[0][1][-1]
        except Exception:  # pragma: nocover
            pass
        if not PY3 and isinstance(pron, unicode) and isinstance(origin, str):  # pragma: nocover
            origin = origin.decode('utf-8')
        if dest in EXCLUDES and pron == origin:
            pron = translated

        # for python 2.x compatbillity
        if not PY3:  # pragma: nocover
            if isinstance(src, str):
                src = src.decode('utf-8')
            if isinstance(dest, str):
                dest = dest.decode('utf-8')
            if isinstance(translated, str):
                translated = translated.decode('utf-8')

        # put final values into a new Translated object
        result = Translated(src=src, dest=dest, origin=origin,
                            text=translated, pronunciation=pron)

        return result

    def detect(self, text):
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
                lang = self.detect(item)
                result.append(lang)
            return result

        data = self._translate(text, dest='en', src='auto')

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ''
        confidence = 0.0
        try:
            src = ''.join(data[8][0])
            confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence)

        return result
