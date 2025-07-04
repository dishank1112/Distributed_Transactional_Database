
import httpx
from .schemas import TxRequest, Vote

DELIVERY_SERVICE_URL = "http://localhost:8001"
STORAGE_SERVICE_URL  = "http://localhost:8002"

async def send_prepare(service_url: str, tx: TxRequest) -> Vote:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{service_url}/prepare", json=tx.dict())
        resp.raise_for_status()
        return Vote(**resp.json())

async def send_commit(service_url: str, tx: TxRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{service_url}/commit", json=tx.dict())
        resp.raise_for_status()

async def send_rollback(service_url: str, tx: TxRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{service_url}/rollback", json=tx.dict())
        resp.raise_for_status()
