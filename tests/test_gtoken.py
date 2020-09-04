# -*- coding: utf-8 -*-
import httpx

from googletrans import gtoken
from pytest import fixture


@fixture(scope='session')
def acquirer():
    client = httpx.Client(http2=True)
    return gtoken.TokenAcquirer(client=client)


def test_acquire_token(acquirer):
    text = 'test'

    result = acquirer.do(text)

    assert result


def test_acquire_token_ascii_less_than_2048(acquirer):
    text = u'Ѐ'

    result = acquirer.do(text)

    assert result


def test_acquire_token_ascii_matches_special_condition(acquirer):
    def unichar(i):
        try:
            return unichr(i)
        except NameError:
            return chr(i)
    text = unichar(55296) + unichar(56320)

    result = acquirer.do(text)

    assert result


def test_acquire_token_ascii_else(acquirer):
    text = u'가'

    result = acquirer.do(text)

    assert result


def test_reuse_valid_token(acquirer):
    text = 'test'

    first = acquirer.do(text)
    second = acquirer.do(text)

    assert first == second


def test_map_lazy_return(acquirer):
    value = True

    func = acquirer._lazy(value)

    assert callable(func)
    assert func() == value
