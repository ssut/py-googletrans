from pytest import fixture


@fixture
def translator():
    from aiogoogletrans import Translator
    return Translator()
