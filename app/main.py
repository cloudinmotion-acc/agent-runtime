from fastapi import FastAPI
from app.schemas import AgentRequest, AgentResponse
from app.graph.simple_agent import build_graph

app = FastAPI(title="Agent Runtime")

agent_graph = build_graph()

@app.post("/agent/run", response_model=AgentResponse)
def run_agent(req: AgentRequest):
    result = agent_graph.invoke({
        "user_id": req.user_id,
        "input": req.input
    })
    return AgentResponse(output=result["output"])
