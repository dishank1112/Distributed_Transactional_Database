
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from common.schemas import TxRequest, Vote
from .db import SessionLocal, Agent, TxLog

router = APIRouter()

@router.post("/prepare", response_model=Vote)
def prepare(tx: TxRequest):
    db: Session = SessionLocal()
    try:
        agent = db.query(Agent).filter_by(is_reserved=False).first()
        if not agent:
            return Vote(vote="no")

        agent.is_reserved = True
        agent.order_id    = tx.orderId

        tx_log = TxLog(tx_id=tx.transactionId, agent_id=agent.id)
        db.add(tx_log)

        db.commit()
        return Vote(vote="yes")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"No Delivery Services Available: {e}")
    finally:
        db.close()


@router.post("/commit")
def commit(tx: TxRequest):
 
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