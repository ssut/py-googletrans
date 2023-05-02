import unittest
from httpcore import TimeoutException
from httpcore._exceptions import ConnectError
from httpx import Timeout, Client, ConnectTimeout
from unittest.mock import patch
from googletrans import Translator
import contextlib


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = 'tkk:\'translation\''


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.translator = Translator

    def test_en_es_translate(self):
        TEST_QUERY = 'i want you to tell me'
        EXPECTED_TRANSLATION = 'quiero que me digas'
        translator = Translator().translate(TEST_QUERY, src='en', dest='es')
        test_translation = translator.text.lower()
        self.assertEqual(test_translation, EXPECTED_TRANSLATION)

    def test_no_doctype_text(self):
        """
        tests that the translator can handle text with doctype text
        ... error text should not be raised
        """
        TEST_TEXT = "<!DOCTYPE html><html lang="
        translator = Translator()

        with contextlib.nullcontext():
            test_text = translator.translate(TEST_TEXT, dest='es')

    def test_bind_multiple_service_urls(self):
        service_urls = [
            'translate.google.com',
            'translate.google.co.kr',
        ]

        translator = Translator(service_urls=service_urls)
        self.assertEqual(translator.service_urls, service_urls)

        self.assertIsNotNone(translator.translate('test', dest='ko'))
        self.assertIsNotNone(translator.detect('Hello'))

    def test_pronunciation_issue_175(self):
        trans = self.translator()
        result = trans.translate('Hello', src='en', dest='ru')
        self.assertIsNotNone(result.pronunciation)

    def test_emoji(self):
        trans = self.translator()
        result = trans.translate('😀')
        self.assertEqual(result.text, u'😀')

    def test_language_name_with_space(self):
        trans = self.translator()
        result = trans.translate(
            u'Hello', src='en', dest='chinese (simplified)')
        self.assertEqual(result.dest, 'zh-cn')

    def test_special_chars(self):
        trans = self.translator()
        text = u"©×《》"

        result = trans.translate(text, src='en', dest='en')
        self.assertEqual(result.text, text)

    def test_src_not_in_supported_languages(self):
        trans = self.translator()
        args = ('Hello', 'en', 'zzz')

        with self.assertRaises(ValueError):
            trans.translate(*args)

    def test_dest_not_in_supported_languages(self):
        trans = self.translator()
        args = ('Hello', 'zzz', 'en')

        with self.assertRaises(ValueError):
            trans.translate(*args)

    def test_timeout(self):
        with self.assertRaises((TimeoutException, ConnectError, ConnectTimeout)):
            translator = Translator(timeout=Timeout(0.0001))
            translator.translate('안녕하세요.')

    @patch.object(Client, 'get', return_value=MockResponse('403'))
    def test_403_error(self, session_mock):
        translator = self.translator()
        self.assertIsNotNone(translator.translate('test', dest='ko'))

if __name__ == '__main__':
    unittest.main()
