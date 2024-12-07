from fastapi import status
from httpx import AsyncClient


async def test_greeting(client: AsyncClient) -> None:
    req = {"name": "Bob"}
    resp = await client.post(
        "/api/greeting",
        json=req,
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"message": "Hello, Bob"}
