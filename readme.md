# Distributed Transactional Database with 2-Phase Commit (2PC)

This project simulates a distributed transactional system using the **2-Phase Commit protocol** across microservices:
- `order_service` (Coordinator)
- `delivery_service`
- `storage_service`

## 🚀 Technologies Used
- FastAPI
- PostgreSQL
- SQLAlchemy
- Async HTTP (httpx)
- Python 3.10+

## 🧠 How It Works
- Each service runs independently on different ports.
- The coordinator sends `/prepare` requests to both services.
- If both vote "yes", it sends `/commit`; else `/rollback`.

## 🛠 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd Distributed_Transactional_Database


2. Create and activate virtual environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Create .env from .env.example
bash
Copy
Edit
copy .env.example .env  # Use correct DB URLs and passwords
5. Run all three services
bash
Copy
Edit
# In separate terminals:
uvicorn delivery_services.main:app --port 8001 --reload
uvicorn storage_services.main:app --port 8002 --reload
uvicorn order_service.main:app --port 8000 --reload
6. Simulate Orders
bash
Copy
Edit
python simulate_orders.py