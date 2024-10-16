from httpcore import TimeoutException
from httpcore._exceptions import ConnectError
from httpx import Timeout, Client, ConnectTimeout
from unittest.mock import patch
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

def test_api_service_urls():
    service_urls = ['translate.googleapis.com']

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
    assert result.text == 'truth is my light'


def test_unicode(translator):
    result = translator.translate(u'안녕하세요.', src='ko', dest='ja')
    assert result.text == u'こんにちは。'


def test_emoji(translator):
    result = translator.translate('😀')
    assert result.text == u'😀'


def test_language_name(translator):
    result = translator.translate(u'Hello', src='ENGLISH', dest='iRiSh')
    assert result.text == u'Dia duit'


def test_language_name_with_space(translator):
    result = translator.translate(
        u'Hello', src='en', dest='chinese (simplified)')
    assert result.dest == 'zh-cn'


def test_language_rfc1766(translator):
    result = translator.translate(u'luna', src='it_ch@euro', dest='en')
    assert result.text == u'moon'


def test_special_chars(translator):
    text = u"©×《》"

    result = translator.translate(text, src='en', dest='en')
    assert result.text == text


def test_translate_list(translator):
    args = (['test', 'exam', 'exam paper'], 'ko', 'en')
    translations = translator.translate(*args)

    assert translations[0].text == u'시험'
    assert translations[1].text == u'시험'
    assert translations[2].text == u'시험지'


def test_detect_language(translator):
    ko = translator.detect(u'한국어')
    en = translator.detect('English')
    rubg = translator.detect('тест')
    russ = translator.detect('привет')

    assert ko.lang == 'ko'
    assert en.lang == 'en'
    assert rubg.lang == 'mk'
    assert russ.lang == 'ru'
    #'bg']


def test_detect_list(translator):
    items = [u'한국어', ' English', 'тест', 'привет']

    result = translator.detect(items)

    assert result[0].lang == 'ko'
    assert result[1].lang == 'en'
    assert result[2].lang == 'mk'
    assert result[3].lang == 'ru'


def test_src_in_special_cases(translator):
    args = ('tere', 'en', 'ee')

    result = translator.translate(*args)

    assert result.text in ('hello', 'hi,')


def test_src_not_in_supported_languages(translator):
    args = ('Hello', 'en', 'zzz')

    with raises(ValueError):
        translator.translate(*args)


def test_dest_in_special_cases(translator):
    args = ('hello', 'ee', 'en')

    result = translator.translate(*args)

    assert result.text == 'tere'


def test_dest_not_in_supported_languages(translator):
    args = ('Hello', 'zzz', 'en')

    with raises(ValueError):
        translator.translate(*args)


def test_timeout():
    # httpx will raise ConnectError in some conditions
    with raises((TimeoutException, ConnectError, ConnectTimeout)):
        translator = Translator(timeout=Timeout(0.0001))
        translator.translate('안녕하세요.')


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = 'tkk:\'translation\''


@patch.object(Client, 'get', return_value=MockResponse('403'))
def test_403_error(session_mock):
    translator = Translator()
    assert translator.translate('test', dest='ko')
