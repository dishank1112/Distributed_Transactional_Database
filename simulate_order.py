import asyncio
import httpx

ORDER_URL = "http://localhost:8000/order"

timeout = httpx.Timeout(connect=30.0, read=90.0, write=20.0, pool=10.0)

async def place_one(i: int):
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.post(ORDER_URL, params={"order_id": i})
            resp.raise_for_status()
            data = resp.json()
            print(f"Order {i:02d} → {data['status']}")
        except Exception as e:
            print(f"Order {i:02d} → ERROR: {repr(e)}")

async def main():
    tasks = [place_one(i) for i in range(1, 20)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())



