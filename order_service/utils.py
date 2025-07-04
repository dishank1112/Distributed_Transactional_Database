import uuid

def generate_transaction_id() -> str:
    return f"tx-{uuid.uuid4().hex[:8]}"
