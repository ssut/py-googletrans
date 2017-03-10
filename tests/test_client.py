# -*- coding: utf-8 -*-
from pytest import raises


def test_latin_to_english(translator):
    result = translator.translate('veritas lux mea', src='la', dest='en')
    assert result.text == 'The truth is my light'


def test_unicode(translator):
    result = translator.translate(u'안녕하세요.', src='ko', dest='ja')
    assert result.text == u'こんにちは。'


def test_translate_list(translator):
    args = (['test', 'exam'], 'ko', 'en')
    translations = translator.translate(*args)

    assert translations[0].text == u'테스트'
    assert translations[1].text == u'시험'


def test_detect_language(translator):
    ko = translator.detect('한국어')
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