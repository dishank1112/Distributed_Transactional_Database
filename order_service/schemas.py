# order_service/schemas.py

from pydantic import BaseModel

class TxRequest(BaseModel):
    transactionId: str
    orderId: int

class Vote(BaseModel):
    vote: str 
