from sqlalchemy import create_engine, Column, Integer, Boolean, String
from sqlalchemy.orm import declarative_base, sessionmaker

import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("STORAGE_URL") 

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,)

Base = declarative_base()

class store(Base):
    __tablename__ = "store"
    id          = Column(Integer, primary_key=True, index=True)
    is_reserved = Column(Boolean, default=False)
    order_id    = Column(Integer, nullable=True)

class TxLog(Base):
    __tablename__ = "tx_log"
    tx_id     = Column(String, primary_key=True, index=True)
    item_id  = Column(Integer)
