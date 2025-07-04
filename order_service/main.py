from fastapi import FastAPI
from .routers import router as order_router

app = FastAPI()
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("order_service.main:app", host="127.0.0.1", port=8000, reload=True)