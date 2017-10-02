from googletrans import utils
from pytest import raises


def test_format_json():
    text = '[,,"en",,,,0.96954316,,[["en"],,[0.96954316]]]'

    result = utils.legacy_format_json(text)

    assert result == [None, None, 'en', None, None, None, 0.96954316, None,
                      [['en'], None, [0.96954316]]]

def test_format_malformed_json():
    text = '[,,"en",,,,0.96954316,,[["en"],,0.96954316]]]'

    with raises(ValueError):
        utils.legacy_format_json(text)

def test_rshift():
    value, n = 1000, 3

    result = utils.rshift(value, n)

    assert result == 125
