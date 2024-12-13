from unittest.mock import patch

import pytest
from httpcore import TimeoutException
from httpcore._exceptions import ConnectError
from httpx import Client, ConnectTimeout, Timeout
from pytest import raises

from googletrans import Translator


@pytest.mark.asyncio
async def test_bind_multiple_service_urls():
    service_urls = [
        "translate.google.com",
        "translate.google.co.kr",
    ]

    translator = Translator(service_urls=service_urls)
    assert translator.service_urls == service_urls

    assert await translator.translate("test", dest="ko")
    assert await translator.detect("Hello")


@pytest.mark.asyncio
async def test_api_service_urls():
    service_urls = ["translate.googleapis.com"]

    translator = Translator(service_urls=service_urls)
    assert translator.service_urls == service_urls

    assert await translator.translate("test", dest="ko")
    assert await translator.detect("Hello")


@pytest.mark.asyncio
async def test_source_language(translator: Translator):
    result = await translator.translate("안녕하세요.")
    assert result.src == "ko"


@pytest.mark.asyncio
async def test_pronunciation(translator: Translator):
    result = await translator.translate("안녕하세요.", dest="ja")
    assert result.pronunciation == "Kon'nichiwa."


@pytest.mark.asyncio
async def test_pronunciation_issue_175(translator: Translator):
    result = await translator.translate("Hello", src="en", dest="ru")
    assert result.pronunciation is not None


@pytest.mark.asyncio
async def test_latin_to_english(translator: Translator):
    result = await translator.translate("veritas lux mea", src="la", dest="en")
    assert result.text == "truth is my light"


@pytest.mark.asyncio
async def test_unicode(translator: Translator):
    result = await translator.translate("안녕하세요.", src="ko", dest="ja")
    assert result.text == "こんにちは。"


@pytest.mark.asyncio
async def test_emoji(translator: Translator):
    result = await translator.translate("😀")
    assert result.text == "😀"


@pytest.mark.asyncio
async def test_language_name(translator: Translator):
    result = await translator.translate("Hello", src="ENGLISH", dest="iRiSh")
    assert result.text == "Dia duit"


@pytest.mark.asyncio
async def test_language_name_with_space(translator: Translator):
    result = await translator.translate("Hello", src="en", dest="chinese (simplified)")
    assert result.dest == "zh-cn"


@pytest.mark.asyncio
async def test_language_rfc1766(translator: Translator):
    result = await translator.translate("luna", src="it_ch@euro", dest="en")
    assert result.text == "moon"


@pytest.mark.asyncio
async def test_special_chars(translator: Translator):
    text = "©×《》"
    result = await translator.translate(text, src="en", dest="en")
    assert result.text == text


@pytest.mark.asyncio
async def test_translate_list(translator: Translator):
    args = (["test", "exam", "exam paper"], "ko", "en")
    translations = await translator.translate(*args)
    assert translations[0].text == "시험"
    assert translations[1].text == "시험"
    assert translations[2].text == "시험지"


@pytest.mark.asyncio
async def test_detect_language(translator: Translator):
    ko = await translator.detect("한국어")
    en = await translator.detect("English")
    rubg = await translator.detect("летóво")
    russ = await translator.detect("привет")

    assert ko.lang == "ko"
    assert en.lang == "en"
    assert rubg.lang == "bg"
    assert russ.lang == "ru"


@pytest.mark.asyncio
async def test_detect_list(translator: Translator):
    items = ["한국어", " English", "летóво", "привет"]
    result = await translator.detect(items)

    assert result[0].lang == "ko"
    assert result[1].lang == "en"
    assert result[2].lang == "bg"
    assert result[3].lang == "ru"


@pytest.mark.asyncio
async def test_src_in_special_cases(translator: Translator):
    args = ("tere", "en", "ee")
    result = await translator.translate(*args)
    assert result.text in ("hello", "hi,")


@pytest.mark.asyncio
async def test_src_not_in_supported_languages(translator: Translator):
    args = ("Hello", "en", "zzz")
    with raises(ValueError):
        await translator.translate(*args)


@pytest.mark.asyncio
async def test_dest_in_special_cases(translator: Translator):
    args = ("hello", "ee", "en")
    result = await translator.translate(*args)
    assert result.text == "tere"


@pytest.mark.asyncio
async def test_dest_not_in_supported_languages(translator: Translator):
    args = ("Hello", "zzz", "en")
    with raises(ValueError):
        await translator.translate(*args)


@pytest.mark.asyncio
async def test_timeout():
    # httpx will raise ConnectError in some conditions
    with raises((TimeoutException, ConnectError, ConnectTimeout)):
        translator = Translator(timeout=Timeout(0.0001))
        await translator.translate("안녕하세요.")


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = "tkk:'translation'"


@pytest.mark.asyncio
@patch.object(Client, "get", return_value=MockResponse("403"))
async def test_403_error(session_mock):
    translator = Translator()
    assert await translator.translate("test", dest="ko")
