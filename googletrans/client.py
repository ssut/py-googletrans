"""
A Translation module.

You can translate text using this module.
"""

import asyncio
import random
import re
import typing

import httpx
from httpx import Response, Timeout
from httpx._types import ProxyTypes

from googletrans import urls, utils
from googletrans.constants import (
    DEFAULT_CLIENT_SERVICE_URLS,
    DEFAULT_RAISE_EXCEPTION,
    DEFAULT_USER_AGENT,
    DUMMY_DATA,
    LANGCODES,
    LANGUAGES,
    SPECIAL_CASES,
)
from googletrans.gtoken import TokenAcquirer
from googletrans.models import Detected, Translated

EXCLUDES = ("en", "ca", "fr")


class Translator:
    """Google Translate ajax API implementation class

    You have to create an instance of Translator to use this API

    :param service_urls: google translate url list. URLs will be used randomly.
                         For example ``['translate.google.com', 'translate.google.co.kr']``
                         To preferably use the non webapp api, service url should be translate.googleapis.com
    :type service_urls: a sequence of strings

    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`

    :param proxy: httpx proxy configuration.

    :param timeout: Definition of timeout for httpx library.
                    Will be used for every request.
    :type timeout: number or a double of numbers
    :param raise_exception: if `True` then raise exception if smth will go wrong
    :type raise_exception: boolean
    """

    def __init__(
        self,
        service_urls: typing.Sequence[str] = DEFAULT_CLIENT_SERVICE_URLS,
        user_agent: str = DEFAULT_USER_AGENT,
        raise_exception: bool = DEFAULT_RAISE_EXCEPTION,
        proxy: typing.Optional[ProxyTypes] = None,
        timeout: typing.Optional[Timeout] = None,
        http2: bool = True,
        list_operation_max_concurrency: int = 2,
    ):
        self.client = httpx.AsyncClient(
            http2=http2,
            proxy=proxy,
            headers={
                "User-Agent": user_agent,
            },
        )

        self.service_urls = ["translate.google.com"]
        self.client_type = "webapp"
        self.token_acquirer = TokenAcquirer(
            client=self.client, host=self.service_urls[0]
        )

        if timeout is not None:
            self.client.timeout = timeout

        if service_urls:
            # default way of working: use the defined values from user app
            self.service_urls = service_urls
            self.client_type = "webapp"
            self.token_acquirer = TokenAcquirer(
                client=self.client, host=self.service_urls[0]
            )

            # if we have a service url pointing to client api we force the use of it as defaut client
            for t in enumerate(service_urls):
                api_type = re.search("googleapis", service_urls[0])
                if api_type:
                    self.service_urls = ["translate.googleapis.com"]
                    self.client_type = "gtx"
                    break

        self.raise_exception = raise_exception
        self.list_operation_max_concurrency = list_operation_max_concurrency

    def _pick_service_url(self) -> str:
        if len(self.service_urls) == 1:
            return self.service_urls[0]
        return random.choice(self.service_urls)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _translate(
        self, text: str, dest: str, src: str, override: typing.Dict[str, typing.Any]
    ) -> typing.Tuple[typing.List[typing.Any], Response]:
        token = "xxxx"  # dummy default value here as it is not used by api client
        if self.client_type == "webapp":
            token = await self.token_acquirer.do(text)

        params = utils.build_params(
            client=self.client_type,
            query=text,
            src=src,
            dest=dest,
            token=token,
            override=override,
        )

        url = urls.TRANSLATE.format(host=self._pick_service_url())
        r = await self.client.get(url, params=params)

        if r.status_code == 200:
            data = utils.format_json(r.text)
            if not isinstance(data, list):
                data = [data]  # Convert dict to list to match return type
            return data, r

        if self.raise_exception:
            raise Exception(
                'Unexpected status code "{}" from {}'.format(
                    r.status_code, self.service_urls
                )
            )

        DUMMY_DATA[0][0][0] = text
        return DUMMY_DATA, r

    async def build_request(
        self, text: str, dest: str, src: str, override: typing.Dict[str, typing.Any]
    ) -> httpx.Request:
        """Async helper for making the translation request"""
        token = "xxxx"  # dummy default value here as it is not used by api client
        if self.client_type == "webapp":
            token = await self.token_acquirer.do(text)

        params = utils.build_params(
            client=self.client_type,
            query=text,
            src=src,
            dest=dest,
            token=token,
            override=override,
        )

        url = urls.TRANSLATE.format(host=self._pick_service_url())

        return self.client.build_request("GET", url, params=params)

    def _parse_extra_data(
        self, data: typing.List[typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        response_parts_name_mapping = {
            0: "translation",
            1: "all-translations",
            2: "original-language",
            5: "possible-translations",
            6: "confidence",
            7: "possible-mistakes",
            8: "language",
            11: "synonyms",
            12: "definitions",
            13: "examples",
            14: "see-also",
        }

        extra = {}

        for index, category in response_parts_name_mapping.items():
            extra[category] = (
                data[index] if (index < len(data) and data[index]) else None
            )

        return extra

    @typing.overload
    async def translate(
        self, text: str, dest: str = ..., src: str = ..., **kwargs: typing.Any
    ) -> Translated: ...

    @typing.overload
    async def translate(
        self,
        text: typing.List[str],
        dest: str = ...,
        src: str = ...,
        **kwargs: typing.Any,
    ) -> typing.List[Translated]: ...

    async def translate(
        self,
        text: typing.Union[str, typing.List[str]],
        dest: str = "en",
        src: str = "auto",
        **kwargs: typing.Any,
    ) -> typing.Union[Translated, typing.List[Translated]]:
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
            >>> from googletrans import Translator
            >>> translator = Translator()
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
        """
        dest = dest.lower().split("_", 1)[0]
        src = src.lower().split("_", 1)[0]

        if src != "auto" and src not in LANGUAGES:
            if src in SPECIAL_CASES:
                src = SPECIAL_CASES[src]
            elif src in LANGCODES:
                src = LANGCODES[src]
            else:
                raise ValueError("invalid source language")

        if dest not in LANGUAGES:
            if dest in SPECIAL_CASES:
                dest = SPECIAL_CASES[dest]
            elif dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError("invalid destination language")

        if isinstance(text, list):
            concurrency_limit = kwargs.pop(
                "list_operation_max_concurrency", self.list_operation_max_concurrency
            )
            semaphore = asyncio.Semaphore(concurrency_limit)

            async def translate_with_semaphore(item):
                async with semaphore:
                    return await self.translate(item, dest=dest, src=src, **kwargs)

            tasks = [translate_with_semaphore(item) for item in text]
            result = await asyncio.gather(*tasks)
            return result

        origin = text
        data, response = await self._translate(text, dest, src, kwargs)

        # this code will be updated when the format is changed.
        translated = "".join([d[0] if d[0] else "" for d in data[0]])

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
            except:  # pragma: nocover  # noqa: E722
                pass

        if dest in EXCLUDES and pron == origin:
            pron = translated

        # put final values into a new Translated object
        result = Translated(
            src=src,
            dest=dest,
            origin=origin,
            text=translated,
            pronunciation=pron,
            extra_data=extra_data,
            response=response,
        )

        return result

    @typing.overload
    async def detect(self, text: str, **kwargs: typing.Any) -> Detected: ...

    @typing.overload
    async def detect(
        self, text: typing.List[str], **kwargs: typing.Any
    ) -> typing.List[Detected]: ...

    async def detect(
        self, text: typing.Union[str, typing.List[str]], **kwargs: typing.Any
    ) -> typing.Union[Detected, typing.List[Detected]]:
        """Detect language of the input text

        :param text: The source text(s) whose language you want to identify.
                     Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from googletrans import Translator
            >>> translator = Translator()
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
        """
        if isinstance(text, list):
            concurrency_limit = kwargs.pop(
                "list_operation_max_concurrency", self.list_operation_max_concurrency
            )
            semaphore = asyncio.Semaphore(concurrency_limit)

            async def detect_with_semaphore(item):
                async with semaphore:
                    return await self.detect(item, **kwargs)

            tasks = [detect_with_semaphore(item) for item in text]
            result = await asyncio.gather(*tasks)
            return result

        data, response = await self._translate(text, "en", "auto", kwargs)

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ""
        confidence = 0.0
        try:
            if len(data[8][0]) > 1:
                src = data[8][0]
                confidence = data[8][-2]
            else:
                src = "".join(data[8][0])
                confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence, response=response)

        return result
