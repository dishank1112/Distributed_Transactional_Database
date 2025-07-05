from db import SessionLocal, Agent

def test_connection():
    session = SessionLocal()
    try:
        cnt = session.query(Agent).count()
        print(f"Agents table has {cnt} rows.")
    finally:
        session.close()

if __name__ == "__main__":
    test_connection()
