# Agent Runtime

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

Export variable with your keys. Check `.env.example`.

### Setp-4

Run the FastAPI application

```bash
uvicorn app.main:app --reload --port 9000
```

### Step-5

Test the server from the terminal

```sh
curl -X POST http://localhost:9000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo-1",
    "input": "Lemme test you, remember what im aksing?",
    "model": "gpt-5-nano"
  }'
```
