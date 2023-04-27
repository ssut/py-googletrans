import unittest
from googletrans import utils


class TestUtils(unittest.TestCase):
    """
    tests utilities used throught the package
    """
    def test_format_json(self):
        text = '[,,"en",,,,0.96954316,,[["en"],,[0.96954316]]]'
        result = utils.format_json(text)
        self.assertEqual(result, [
            None,
            None,
            'en',
            None,
            None,
            None,
            0.96954316,
            None,
            [['en'], None, [0.96954316]]
        ])

    def test_format_malformed_json(self):
        text = '[,,"en",,,,0.96954316,,[["en"],,0.96954316]]]'
        with self.assertRaises(ValueError):
            utils.format_json(text)

    def test_rshift(self):
        value, n = 1000, 3
        result = utils.rshift(value, n)
        self.assertEqual(result, 125)


if __name__ == '__main__':
    unittest.main()
