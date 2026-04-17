import asyncio
import time

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport

from api_pagamentos import app


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize("num_requisicoes", [5, 20, 50])
async def test_performance_pagamentos(async_client, num_requisicoes):
    async def requisitar():
        return await async_client.get("/processar")

    inicio = time.monotonic()
    respostas = await asyncio.gather(
        *[requisitar() for _ in range(num_requisicoes)]
    )
    tempo_total = time.monotonic() - inicio

    assert all(resposta.status_code == 200 for resposta in respostas)
    assert all(
        resposta.json() == {"status": "pagamento_aprovado"}
        for resposta in respostas
    )
    assert tempo_total < 3.5, (
        f"Tempo total ({tempo_total:.2f}s) excedeu 3.5s "
        f"com {num_requisicoes} requisicoes simultaneas."
    )
