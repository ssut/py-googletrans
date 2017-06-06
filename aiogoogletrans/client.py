# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import aiohttp
import random
import asyncio

from aiogoogletrans import urls, utils
from aiogoogletrans.gtoken import TokenAcquirer
from aiogoogletrans.constants import DEFAULT_USER_AGENT, LANGCODES, LANGUAGES, SPECIAL_CASES
from aiogoogletrans.models import Translated, Detected


EXCLUDES = ('en', 'ca', 'fr')


class Translator(object):
    """Google Translate ajax API implementation class

    You have to create an instance of Translator to use this API

    :param service_urls: google translate url list. URLs will be used randomly.
                         For example ``['translate.google.com', 'translate.google.co.kr']``
    :type service_urls: a sequence of strings

    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`
    """

    def __init__(self, service_urls=None, user_agent=DEFAULT_USER_AGENT):
        self.headers = {
            'User-Agent': user_agent,
        }
        self.service_urls = service_urls or ['translate.google.com']
        self.token_acquirer = TokenAcquirer(host=self.service_urls[0])

    def _pick_service_url(self):
        if len(self.service_urls) == 1:
            return self.service_urls[0]
        return random.choice(self.service_urls)

    async def _translate(self, text, dest, src):
        token = await self.token_acquirer.do(text)
        params = utils.build_params(query=text, src=src, dest=dest,
                                    token=token)
        url = urls.TRANSLATE.format(host=self._pick_service_url())

        with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url + '?' + params) as resp:
                text = await resp.text()

        return utils.format_json(text)

    async def translate(self, text, dest='en', src='auto'):
        """Translate text from source language to destination language

        :param text: The source text(s) to be translated. Batch translation is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :param dest: The language to translate the source text into.
                     The value should be one of the language codes listed in :const:`googletrans.LANGUAGES`
                     or one of the language names listed in :const:`googletrans.LANGCODES`.
        :param dest: :class:`str`; :class:`unicode`

        :param src: The language of the source text.
                    The value should be one of the language codes listed in :const:`googletrans.LANGUAGES`
                    or one of the language names listed in :const:`googletrans.LANGCODES`.
                    If a language is not specified,
                    the system will attempt to identify the source language automatically.
        :param src: :class:`str`; :class:`unicode`

        :rtype: Translated
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from aiogoogletrans import Translator
            >>> translator = Translator()
            >>> await translator.translate('안녕하세요.')
            <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
            >>> await translator.translate('안녕하세요.', dest='ja')
            <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
            >>> await translator.translate('veritas lux mea', src='la')
            <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

        Advanced usage:
            >>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
            >>> for translation in translations:
            ...    print(translation.origin, ' -> ', translation.text)
            The quick brown fox  ->  빠른 갈색 여우
            jumps over  ->  이상 점프
            the lazy dog  ->  게으른 개
        """
        dest = dest.lower().split('_', 1)[0]
        src = src.lower().split('_', 1)[0]

        if src != 'auto' and src not in LANGUAGES:
            if src in SPECIAL_CASES:
                src = SPECIAL_CASES[src]
            elif src in LANGCODES:
                src = LANGCODES[src]
            else:
                raise ValueError('invalid source language')

        if dest not in LANGUAGES:
            if dest in SPECIAL_CASES:
                dest = SPECIAL_CASES[dest]
            elif dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError('invalid destination language')

        if isinstance(text, list):
            result = []
            for item in text:
                translated = await self.translate(item, dest=dest, src=src)
                result.append(translated)
            return result

        origin = text
        data = await self._translate(text, dest, src)
        print(data)

        # this code will be updated when the format is changed.
        translated = ''.join([d[0] if d[0] else '' for d in data[0]])

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
        if dest in EXCLUDES and pron == origin:
            pron = translated

        # put final values into a new Translated object
        result = Translated(src=src, dest=dest, origin=origin,
                            text=translated, pronunciation=pron)

        return result

    async def detect(self, text):
        """Detect language of the input text

        :param text: The source text(s) whose language you want to identify.
                     Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from aiogoogletrans import Translator
            >>> translator = Translator()
            >>> await translator.detect('이 문장은 한글로 쓰여졌습니다.')
            <Detected lang=ko confidence=0.27041003>
            >>> await translator.detect('この文章は日本語で書かれました。')
            <Detected lang=ja confidence=0.64889508>
            >>> await translator.detect('This sentence is written in English.')
            <Detected lang=en confidence=0.22348526>
            >>> await translator.detect('Tiu frazo estas skribita en Esperanto.')
            <Detected lang=eo confidence=0.10538048>

        Advanced usage:
            >>> langs = await translator.detect(['한국어', '日本語', 'English', 'le français'])
            >>> for lang in langs:
            ...    print(lang.lang, lang.confidence)
            ko 1
            ja 0.92929292
            en 0.96954316
            fr 0.043500196
        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = await self.detect(item)
                result.append(lang)
            return result

        data = await self._translate(text, dest='en', src='auto')

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
