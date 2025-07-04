import uuid, httpx

def new_tx_id() -> str:
    return str(uuid.uuid4())

async def post_json(url: str, body: dict, timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=body)
        resp.raise_for_status()
        return resp.json()
