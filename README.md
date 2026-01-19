# Agent Runtime

## -------------------- TBD -------------------- 

## Getting-Started

### Step-1

Create a virtual environment

```bash
python -m venv venv
# Activate venv
source venv/Scripts/activate # For Linux
# For Windows
.\venv\Scripts\activate
```

### Step-2

Install the dependencies

```bash
pip install -r requirements.txt
```

### Step-3

Create a `.env` file and copy the contents from `.env.example` and replace with your keys

### Setp-4

Run the FastAPI application

```bash
uvicorn app.main:app --reload
```

### Step-5

Test the server from the terminal

```sh
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo-1",
    "input": "Who are you?",
    "model": "gpt-4o"
  }'
```

Then:
```sh
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo-1",
    "input": "What did I just ask?",
    "model": "gpt-4o"
  }'
```
