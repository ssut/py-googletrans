# -*- coding: utf-8 -*-
from aiogoogletrans import gtoken
from pytest import fixture
import pytest

@fixture
def acquirer():
    return gtoken.TokenAcquirer()


@pytest.mark.asyncio
async def test_acquire_token(acquirer):
    text = 'test'

    result = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_acquire_token_ascii_less_than_2048(acquirer):
    text = u'Ѐ'

    result = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_acquire_token_ascii_matches_special_condition(acquirer):
    def unichar(i):
        try:
            return unichr(i)
        except NameError:
            return chr(i)
    text = unichar(55296) + unichar(56320)

    result = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_acquire_token_ascii_else(acquirer):
    text = u'가'

    result = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_reuse_valid_token(acquirer):
    text = 'test'

    first = await acquirer.do(text)
    second = await acquirer.do(text)

    assert first == second


def test_map_lazy_return(acquirer):
    value = True

    func = acquirer._lazy(value)

    assert callable(func)
    assert func() == value
