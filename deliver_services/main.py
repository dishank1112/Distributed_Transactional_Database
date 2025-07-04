
from fastapi import FastAPI
from .routers import router as tx_router

app = FastAPI()
app.include_router(tx_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("deliver_services.main:app", host="127.0.0.1", port=8001, reload=True)
