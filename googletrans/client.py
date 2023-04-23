# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import random
import typing

import httpcore
import httpx
from httpx import Timeout

from googletrans import utils
from googletrans.gtoken import TokenAcquirer
from googletrans.constants import (
    TRANSLATE,
    TRANSLATE_NEW,
    BASE,
    DEFAULT_USER_AGENT,
    LANGCODES,
    LANGUAGES,
    SPECIAL_CASES,
    DEFAULT_RAISE_EXCEPTION,
    DUMMY_DATA,
    RESPONSE_PARTS_NAME_MAP,
)
from googletrans.models import Translated, Detected


EXCLUDES = ('en', 'ca', 'fr')


class Translator:
    """
    Google Translate ajax API implementation class
    You have to create an instance of Translator to use this API
    :param service_urls: google translate url list. URLs will be used randomly.
    For example ``['translate.google.com', 'translate.google.co.kr']``
    :type service_urls: a sequence of strings
    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`
    :param timeout: Definition of timeout for httpx library.
    Will be used for every request.
    :type timeout: number or a double of numbers
    :param raise_exception: if `True` then raise exception if smth will go wrong
    :type raise_exception: boolean
    """

    def __init__(self, service_urls=None, user_agent=DEFAULT_USER_AGENT,
                 raise_exception=DEFAULT_RAISE_EXCEPTION,
                 timeout: Timeout = None,
                 http2=True):

        self.client = httpx.Client(http2=http2)
        self.client.headers.update({'User-Agent': user_agent,})

        if timeout is not None:
            self.client.timeout = timeout

        self.service_urls = service_urls if service_urls else ['translate.google.com']
        self.token_acquirer = TokenAcquirer(client=self.client, host=self.service_urls[0])
        self.raise_exception = raise_exception

    def _pick_service_url(self):
        if len(self.service_urls) == 1:
            return self.service_urls[0]
        return random.choice(self.service_urls)

    def _translate(self, text, dest, src, override):
        token = self.token_acquirer.do(text)
        # params = utils.build_params(query=text, src=src, dest=dest, token=token, override=override)
        # url = TRANSLATE.format(host=self._pick_service_url())
        url = TRANSLATE_NEW.format(text=text, src=src, dest=dest)

        # r = self.client.get(url, params=params)
        r = self.client.get(url)

        if r.status_code == 200:
            data = utils.format_json(r.text)
            return data, r

        if self.raise_exception:
            raise Exception('Unexpected status code "{}" from {}'.format(
                r.status_code, self.service_urls))

        DUMMY_DATA[0][0][0] = text
        return DUMMY_DATA, r

    def _parse_extra_data(self, data):
        extra = {}
        for index, category in RESPONSE_PARTS_NAME_MAP.items():
            extra[category] = data[index] if (
                index < len(data) and data[index]) else None
        return extra

    def translate(self, text, dest='en', src='auto', **kwargs):
        """
        Translate text from source language to destination language.
        :param text: The source text(s) to be translated. Batch translation is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)
        :param dest:The language to translate the source text into.
                    The value should be one of the language codes listed in :const:`googletrans.LANGUAGES`
                    or one of the language names listed in :const:`googletrans.LANGCODES`.
                    :class:`str`; :class:`unicode`
        :param src: The language of the source text.
                    The value should be one of the language codes listed in :const:`googletrans.LANGUAGES`
                    or one of the language names listed in :const:`googletrans.LANGCODES`.
                    If a language is not specified,
                    the system will attempt to identify the source language automatically.
                    :class:`str`; :class:`unicode`
        :rtype: Translated
        :rtype: :class:`list` (when a list is passed)
        """
        dest = dest.lower().split('_', 1)[0]
        src = src.lower().split('_', 1)[0]

        # only valid languages!
        if src != 'auto' and src not in LANGUAGES:
            if src in SPECIAL_CASES:
                src = SPECIAL_CASES[src]
            elif src in LANGCODES:
                src = LANGCODES[src]
            else:
                raise ValueError('invalid source language')

        # only valid languages!
        if dest not in LANGUAGES:
            if dest in SPECIAL_CASES:
                dest = SPECIAL_CASES[dest]
            elif dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError('invalid destination language')

        # if param is list: assume iterable of texts to translate
        if isinstance(text, list):
            result = []
            for item in text:
                translated = self.translate(item, dest=dest, src=src, **kwargs)
                result.append(translated)
            return result

        origin = text
        data, response = self._translate(text, dest, src, kwargs)

        # this code will be updated when the format is changed.
        translated = ''.join([d[0] if d[0] else '' for d in data[0]])
        extra_data = self._parse_extra_data(data)

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        try:
            src = data[2]
        except Exception:  # pragma: nocover
            pass

        pron = origin
        try:
            pron = data[0][1][-2]
        except Exception:  # pragma: nocover
            pass

        if pron is None:
            try:
                pron = data[0][1][2]
            except:  # pragma: nocover
                pass

        if dest in EXCLUDES and pron == origin:
            pron = translated

        # put final values into a new Translated object
        result = Translated(src=src, dest=dest, origin=origin,
                            text=translated, pronunciation=pron,
                            extra_data=extra_data,
                            response=response)

        return result

    def detect(self, text, **kwargs):
        """
        Detect language of the input text
        :param text: The source text(s) whose language you want to identify.
                    Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)
        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)
        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data, response = self._translate(text, 'en', 'auto', kwargs)

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ''
        confidence = 0.0
        try:
            if len(data[8][0]) > 1:
                src = data[8][0]
                confidence = data[8][-2]
            else:
                src = ''.join(data[8][0])
                confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence, response=response)

        return result
