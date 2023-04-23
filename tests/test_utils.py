import unittest
from googletrans import utils

class TestUtils(unittest.TestCase):
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

    def test_build_params_with_override(self):
        params = utils.build_params(
            query='',
            src='',
            dest='',
            token='',
            override={
                'otf': '3',
            },
        )

        self.assertEqual(params['otf'], '3')

if __name__ == '__main__':
    unittest.main()
