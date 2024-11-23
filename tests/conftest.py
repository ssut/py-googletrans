import httpx
import pytest

from googletrans import Translator, gtoken


@pytest.fixture(scope="function")
async def translator():
    async with Translator() as t:
        yield t


@pytest.fixture(scope="function")
async def acquirer():
    async with httpx.AsyncClient(http2=True) as client:
        yield gtoken.TokenAcquirer(client=client)
