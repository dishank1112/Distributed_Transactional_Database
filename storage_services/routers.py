from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from common.schemas import TxRequest, Vote
from .db import SessionLocal, store, TxLog

router = APIRouter()
@router.post("/prepare", response_model=Vote)
def prepare(tx: TxRequest):
    db: Session = SessionLocal()
    try:
        item = db.query(store).filter_by(is_reserved=False).first()
        if not item:
            return Vote(vote="no")

        item.is_reserved = True
        item.order_id = tx.orderId

        tx_log = TxLog(tx_id=tx.transactionId, item_id=item.id)
        db.add(tx_log)
        db.commit()

        return Vote(vote="yes")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"No Food Items Available: {e}")
    finally:
        db.close()



@router.post("/commit")
def commit(tx: TxRequest):
    """
    Phase‑2 “commit” step:
    - No extra DB changes needed; reservation is already in place.
    - Delete the TxLog entry to clean up.
    """
    db: Session = SessionLocal()
    try:
        # Find the log entry
        log = db.query(TxLog).get(tx.transactionId)
        if log:
            db.delete(log)
            db.commit()
        return {"status": "committed"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Commit failed: {e}")
    finally:
        db.close()

@router.post("/rollback")
def rollback(tx: TxRequest):
    db: Session = SessionLocal()
    try:
        log = db.query(TxLog).get(tx.transactionId)
        if log:
            item = db.query(store).get(log.item_id)
            if item:
                item.is_reserved = False
                item.order_id = None
            db.delete(log)
            db.commit()
        return {"status": "rolled back"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Rollback failed: {e}")
    finally:
        db.close()
