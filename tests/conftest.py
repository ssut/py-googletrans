from pytest import fixture


@fixture
def translator():
    from googletrans import Translator
    return Translator()