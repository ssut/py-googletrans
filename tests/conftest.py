from pytest import fixture


@fixture(scope='session')
def translator():
    from googletrans import Translator
    return Translator()
