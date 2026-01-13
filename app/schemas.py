from pydantic import BaseModel

class AgentRequest(BaseModel):
    user_id: str
    input: str

class AgentResponse(BaseModel):
    output: str
