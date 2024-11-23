from typing import Any, Callable

import pytest

from googletrans import gtoken


@pytest.mark.asyncio
async def test_acquire_token(acquirer: gtoken.TokenAcquirer) -> None:
    text: str = "test"

    result: str = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_acquire_token_ascii_less_than_2048(
    acquirer: gtoken.TokenAcquirer,
) -> None:
    text: str = "Ѐ"

    result: str = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_acquire_token_ascii_matches_special_condition(
    acquirer: gtoken.TokenAcquirer,
) -> None:
    def unichar(i: int) -> str:
        return chr(i)

    text: str = unichar(55296) + unichar(56320)

    result: str = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_acquire_token_ascii_else(acquirer: gtoken.TokenAcquirer) -> None:
    text: str = "가"

    result: str = await acquirer.do(text)

    assert result


@pytest.mark.asyncio
async def test_reuse_valid_token(acquirer: gtoken.TokenAcquirer) -> None:
    text: str = "test"

    first: str = await acquirer.do(text)
    second: str = await acquirer.do(text)

    assert first == second


def test_map_lazy_return(acquirer: gtoken.TokenAcquirer) -> None:
    value: bool = True

    func: Callable[[], Any] = acquirer._lazy(value)

    assert callable(func)
    assert func() == value
