import unittest
import httpx
from googletrans import gtoken


def unichar(i):
    try:
        return unichr(i)
    except NameError:
        return chr(i)


class TestGtoken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = httpx.Client(http2=True)
        cls.acquirer = gtoken.TokenAcquirer(client=cls.client)

    def test_acquire_token(self):
        text = 'test'
        result = self.acquirer.do(text)
        self.assertIsNotNone(result)

    def test_acquire_token_ascii_less_than_2048(self):
        text = u'Ѐ'
        result = self.acquirer.do(text)
        self.assertIsNotNone(result)

    def test_acquire_token_ascii_matches_special_condition(self):
        text = unichar(55296) + unichar(56320)
        result = self.acquirer.do(text)
        self.assertIsNotNone(result)

    def test_acquire_token_ascii_else(self):
        text = u'가'
        result = self.acquirer.do(text)
        self.assertIsNotNone(result)

    def test_reuse_valid_token(self):
        text = 'test'
        first = self.acquirer.do(text)
        second = self.acquirer.do(text)
        self.assertEqual(first, second)

    def test_map_lazy_return(self):
        value = True
        func = self.acquirer._lazy(value)
        self.assertTrue(callable(func))
        self.assertEqual(func(), value)

if __name__ == '__main__':
    unittest.main()
