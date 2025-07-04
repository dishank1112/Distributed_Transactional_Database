
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from common.schemas import TxRequest, Vote
from .db import SessionLocal, Agent, TxLog

router = APIRouter()

@router.post("/prepare", response_model=Vote)
def prepare(tx: TxRequest):
    """
    Phase‑1 “prepare” step:
    - Find the first free Agent.
    - Tentatively reserve it (is_reserved=True, order_id=…).
    - Record the tx in TxLog for later commit/rollback.
    - Return Vote(vote="yes") if reserved, else Vote(vote="no").
    """
    db: Session = SessionLocal()
    try:
        # 1) Grab one free agent
        agent = db.query(Agent).filter_by(is_reserved=False).first()
        if not agent:
            return Vote(vote="no")

        # 2) Tentatively reserve
        agent.is_reserved = True
        agent.order_id    = tx.orderId

        # 3) Log the transaction
        tx_log = TxLog(tx_id=tx.transactionId, agent_id=agent.id)
        db.add(tx_log)
        
        # 4) Commit the local DB changes
        db.commit()
        return Vote(vote="yes")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"No Delivery Services Available: {e}")
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
    """
    Phase‑2 “rollback” step:
    - Look up which agent was reserved in TxLog.
    - Undo the tentative reservation.
    - Delete the TxLog entry.
    """
    db: Session = SessionLocal()
    try:
        log = db.query(TxLog).get(tx.transactionId)
        if log:
            # Undo reservation
            agent = db.query(Agent).get(log.agent_id)
            if agent:
                agent.is_reserved = False
                agent.order_id    = None
            # Remove the log
            db.delete(log)
            db.commit()

        return {"status": "rolled back"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Rollback failed: {e}")

    finally:
        db.close()