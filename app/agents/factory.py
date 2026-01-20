import os
import logging

logger = logging.getLogger(__name__)


def get_agent(router, memory):
    framework = os.getenv("FRAMEWORK", "langgraph").lower()
    
    logger.info(f"Creating agent with framework: {framework}")
    
    if framework == "langgraph":
        from app.agents.langgraph_agent import LangGraphAgent
        return LangGraphAgent(router=router, memory=memory)
    
    elif framework == "crewai":
        from app.agents.crewai_agent import CrewAIAgent
        return CrewAIAgent(router=router, memory=memory)
    
    else:
        raise ValueError(
            f"Unknown framework: {framework}. "
            f"Supported: langgraph, crewai"
        )
