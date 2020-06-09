# -*- coding: utf-8 -*-
from pytest import raises
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout

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


def test_pronunciation_issue_175(translator):
    result = translator.translate('Hello', src='en', dest='ru')

    assert result.pronunciation is not None


def test_latin_to_english(translator):
    result = translator.translate('veritas lux mea', src='la', dest='en')
    assert result.text == 'The truth is my light'


def test_unicode(translator):
    result = translator.translate(u'안녕하세요.', src='ko', dest='ja')
    assert result.text == u'こんにちは。'


def test_emoji(translator):
    result = translator.translate('😀')
    assert result.text == u'😀'


def test_language_name(translator):
    result = translator.translate(u'Hello', src='ENGLISH', dest='iRiSh')
    assert result.text == u'Dia dhuit'


def test_language_name_with_space(translator):
    result = translator.translate(u'Hello', src='en', dest='chinese (simplified)')
    assert result.dest == 'zh-cn'


def test_language_rfc1766(translator):
    result = translator.translate(u'luna', src='it_ch@euro', dest='en')
    assert result.text == u'moon'


def test_special_chars(translator):
    text = u"©×《》"

    result = translator.translate(text, src='en', dest='en')
    assert result.text == text


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

    assert result.text in ('Hello', 'Hi,')


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


def test_connection_timeout():
    # Requests library specifies two timeouts: connection and read

    with raises((ConnectionError, ReadTimeout)):
        """If a number is passed to timeout parameter, both connection
           and read timeouts will be set to it.
           Firstly, the connection timeout will fail.
        """
        translator = Translator(timeout=0.00001)
        translator.translate('안녕하세요.')


def test_read_timeout():

    with raises(ReadTimeout):
        translator = Translator(timeout=(10, 0.00001))
        translator.translate('안녕하세요.')
