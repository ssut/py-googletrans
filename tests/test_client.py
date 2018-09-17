# -*- coding: utf-8 -*-
from pytest import raises

from aiogoogletrans import Translator
import pytest

@pytest.mark.asyncio
async def test_bind_multiple_service_urls():
    service_urls = [
        'translate.google.com',
        'translate.google.co.kr',
    ]

    translator = Translator(service_urls=service_urls)
    assert translator.service_urls == service_urls

    assert await translator.translate('test', dest='ko')


@pytest.mark.asyncio
async def test_latin_to_english(translator):
    result = await translator.translate('veritas lux mea', src='la', dest='en')
    assert result.text == 'The truth is my light'


@pytest.mark.asyncio
async def test_chinese_traditional_to_english(translator):
    result = await translator.translate('資料庫', src='zh-tw', dest='en')
    assert result.text == 'database'


@pytest.mark.asyncio
async def test_chinese_simplified_to_english(translator):
    result = await translator.translate('电脑', src='zh-cn', dest='en')
    assert result.text == 'computer'


@pytest.mark.asyncio
async def test_unicode(translator):
    result = await translator.translate(u'안녕하세요.', src='ko', dest='ja')
    print(result)
    assert result.text == u'こんにちは。'


@pytest.mark.asyncio
async def test_language_name(translator):
    result = await translator.translate(u'Hello', src='ENGLISH', dest='iRiSh')
    assert result.text == u'Dia dhuit'


@pytest.mark.asyncio
async def test_language_rfc1766(translator):
    result = await translator.translate(u'luna', src='it_ch@euro', dest='en')
    assert result.text == u'moon'


@pytest.mark.asyncio
async def test_special_chars(translator):
    text = u"©×《》"

    result = await translator.translate(text, src='en', dest='en')
    assert result.text == text


@pytest.mark.asyncio
async def test_multiple_sentences(translator):
    text = u"""Architecturally, the school has a Catholic character.
Atop the Main Building's gold dome is a golden statue of the Virgin Mary.
Immediately in front of the Main Building and facing it,
is a copper statue of Christ with arms upraised with the legend Venite Ad Me Omnes."""

    result = await translator.translate(text, src='en', dest='es')
    assert result.text == u"""Arquitectónicamente, la escuela tiene un carácter católico.
Encima de la cúpula de oro del edificio principal es una estatua de oro de la Virgen María.
Inmediatamente frente al edificio principal y frente a él,
Es una estatua de cobre de Cristo con los brazos levantados con la leyenda Venite Ad Me Omnes."""


@pytest.mark.asyncio
async def test_translate_list(translator):
    args = (['test', 'exam'], 'ko', 'en')
    translations = await translator.translate(*args)
    print(translations)

    assert translations[0].text == u'테스트'
    assert translations[1].text == u'시험'

@pytest.mark.asyncio
async def test_translate_detect_language(translator):
    ko = await translator.translate(u'한국어')
    en = await translator.translate('English')

    assert ko.src == 'ko'
    assert en.src == 'en'


@pytest.mark.asyncio
async def test_translate_detect_list(translator):
    items = [u'한국어', ' English']

    result = await translator.translate(items)

    assert result[0].src == 'ko'
    assert result[1].src == 'en'

@pytest.mark.asyncio
async def test_detect(translator):
    mapping = {
        'it': 'Ciao, mi chiamo Mario',
        'en': 'The pen is on the table',
        'ko': '한국어',
    }
    for language, text in mapping.items():
        T = await translator.detect(text)
        assert T.lang == language


@pytest.mark.asyncio
async def test_src_in_special_cases(translator):
    args = ('Tere', 'en', 'ee')

    result = await translator.translate(*args)

    assert result.text == 'Hello'


@pytest.mark.asyncio
async def test_src_not_in_supported_languages(translator):
    args = ('Hello', 'en', 'zzz')

    with raises(ValueError):
        await translator.translate(*args)


@pytest.mark.asyncio
async def test_dest_in_special_cases(translator):
    args = ('hello', 'ee', 'en')

    result = await translator.translate(*args)

    assert result.text == 'Tere'


@pytest.mark.asyncio
async def test_dest_not_in_supported_languages(translator):
    args = ('Hello', 'zzz', 'en')

    with raises(ValueError):
        await translator.translate(*args)
