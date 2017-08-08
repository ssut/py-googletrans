# -*- coding: utf-8 -*-
from pytest import raises

from googletrans import Translator


def test_bind_multiple_service_urls():
    service_urls = [
        'translate.google.com',
        'translate.google.co.kr',
    ]

    translator = Translator(service_urls=service_urls)
    assert translator.service_urls == service_urls

    assert translator.translate('test', dest='ko')
    assert translator.detect('Hello')


def test_source_language(translator):
    result = translator.translate('안녕하세요.')
    assert result.src == 'ko'


def test_pronunciation(translator):
    result = translator.translate('안녕하세요.', dest='ja')
    assert result.pronunciation == 'Kon\'nichiwa.'


def test_latin_to_english(translator):
    result = translator.translate('veritas lux mea', src='la', dest='en')
    assert result.text == 'The truth is my light'


def test_unicode(translator):
    result = translator.translate(u'안녕하세요.', src='ko', dest='ja')
    assert result.text == u'こんにちは。'


def test_language_name(translator):
    result = translator.translate(u'Hello', src='ENGLISH', dest='iRiSh')
    assert result.text == u'Dia dhuit'


def test_language_rfc1766(translator):
    result = translator.translate(u'luna', src='it_ch@euro', dest='en')
    assert result.text == u'moon'


def test_special_chars(translator):
    text = u"©×《》"

    result = translator.translate(text, src='en', dest='en')
    assert result.text == text


def test_multiple_sentences(translator):
    text = u"""Architecturally, the school has a Catholic character.
Atop the Main Building's gold dome is a golden statue of the Virgin Mary.
Immediately in front of the Main Building and facing it,
is a copper statue of Christ with arms upraised with the legend Venite Ad Me Omnes."""

    result = translator.translate(text, src='en', dest='es')
    assert result.text == u"""Arquitectónicamente, la escuela tiene un carácter católico.
Encima de la cúpula de oro del edificio principal es una estatua de oro de la Virgen María.
Inmediatamente frente al edificio principal y frente a él,
Es una estatua de cobre de Cristo con los brazos levantados con la leyenda Venite Ad Me Omnes."""


def test_translate_list(translator):
    args = (['test', 'exam'], 'ko', 'en')
    translations = translator.translate(*args)

    assert translations[0].text == u'테스트'
    assert translations[1].text == u'시험'


def test_detect_language(translator):
    ko = translator.detect(u'한국어')
    en = translator.detect('English')

    assert ko.lang == 'ko'
    assert en.lang == 'en'


def test_detect_list(translator):
    items = [u'한국어', ' English']

    result = translator.detect(items)

    assert result[0].lang == 'ko'
    assert result[1].lang == 'en'


def test_src_in_special_cases(translator):
    args = ('Tere', 'en', 'ee')

    result = translator.translate(*args)

    assert result.text == 'Hello'


def test_src_not_in_supported_languages(translator):
    args = ('Hello', 'en', 'zzz')

    with raises(ValueError):
        translator.translate(*args)


def test_dest_in_special_cases(translator):
    args = ('hello', 'ee', 'en')

    result = translator.translate(*args)

    assert result.text == 'Tere'


def test_dest_not_in_supported_languages(translator):
    args = ('Hello', 'zzz', 'en')

    with raises(ValueError):
        translator.translate(*args)
