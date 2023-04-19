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


def test_pronunciation_issue_175(translator):
    result = translator.translate('Hello', src='en', dest='ru')
    assert result.pronunciation is not None


def test_emoji(translator):
    result = translator.translate('😀')
    assert result.text == u'😀'


def test_language_name_with_space(translator):
    result = translator.translate(
        u'Hello', src='en', dest='chinese (simplified)')
    assert result.dest == 'zh-cn'


def test_special_chars(translator):
    text = u"©×《》"

    result = translator.translate(text, src='en', dest='en')
    assert result.text == text


def test_src_not_in_supported_languages(translator):
    args = ('Hello', 'en', 'zzz')

    with raises(ValueError):
        translator.translate(*args)


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
