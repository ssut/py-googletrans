from pytest import fixture


@fixture(scope="session")
def translator():
    from pygoogletrans import Translator

    return Translator()
