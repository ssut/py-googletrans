# -*- coding: utf-8 -*-
import unittest
from googletrans import translator

class TranslateTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_latin_to_english(self):
        result = translator.translate('veritas lux mea', src='la', dest='en')
        assert result.text == 'The truth is my light'

    def test_unicode(self):
        result = translator.translate('안녕하세요.', src='ko', dest='ja')
        assert result.text == u'こんにちは。'

    def test_list_translation(self):
        translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'],
            src='en', dest='ko')

        assert translations[0].text == u'빠른 갈색 여우'
        assert translations[1].text == u'이상 점프'
        assert translations[2].text == u'게으른 개'

if __name__ == '__main__':
    unittest.main()
