# order_service/routers.py
from fastapi import APIRouter, HTTPException
from .schemas import TxRequest, Vote
from .utils import generate_transaction_id
from .services import send_prepare, send_commit, send_rollback

DELIVERY_SERVICE_URL = "http://localhost:8001"
STORAGE_SERVICE_URL  = "http://localhost:8002"


router = APIRouter()
@router.post("/order")
async def place_order(order_id: int):
    tx_id = generate_transaction_id()
    print(f"[OrderService] → Received order_id={order_id}, tx={tx_id}")

    tx = TxRequest(transactionId=tx_id, orderId=order_id)

    # Phase 1: Prepare both
    try:
        vote_storage  = await send_prepare(STORAGE_SERVICE_URL, tx)
        print(f"[OrderService]   storage voted {vote_storage.vote}")
        vote_delivery = await send_prepare(DELIVERY_SERVICE_URL, tx)
        print(f"[OrderService]   delivery voted {vote_delivery.vote}")
    except Exception as e:
        print(f"[OrderService]   ERROR during prepare: {e!r}")
        # rollback any partial
        await send_rollback(STORAGE_SERVICE_URL, tx)
        await send_rollback(DELIVERY_SERVICE_URL, tx)
        raise HTTPException(status_code=500, detail=f"Prepare phase failed: {e}")

    # Phase 2: Commit or Rollback
    if vote_storage.vote == "yes" and vote_delivery.vote == "yes":
        await send_commit(STORAGE_SERVICE_URL, tx)
        await send_commit(DELIVERY_SERVICE_URL, tx)
        print(f"[OrderService] → order {order_id} COMMITTED")
        return {"status": "order committed", "orderId": order_id}
    else:
        if vote_storage.vote  == "yes":
            await send_rollback(STORAGE_SERVICE_URL, tx)
        if vote_delivery.vote == "yes":
            await send_rollback(DELIVERY_SERVICE_URL, tx)
        print(f"[OrderService] → order {order_id} ROLLED BACK (storage={vote_storage.vote}, delivery={vote_delivery.vote})")
        return {
            "status": "order rolled back",
            "orderId": order_id,
            "votes": {"storage": vote_storage.vote, "delivery": vote_delivery.vote},
        }


# order_service/main.py
from fastapi import FastAPI
from .routers import router as order_router

app = FastAPI()
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("order_services_routines.main:app", host="127.0.0.1", port=8000, reload=True)
