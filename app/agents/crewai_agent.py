import logging
from typing import Dict, List

from .base import BaseAgent

logger = logging.getLogger(__name__)


class CrewAIAgent(BaseAgent):
    """
    Agent implementation using CrewAI framework.
    
    Features:
    - Multi-agent collaboration (if extended)
    - Task-based conversation flow
    - Role-based agents
    - Integration with Model Router
    """
    
    def __init__(self, router, memory):
        super().__init__(router, memory)
        logger.info("CrewAIAgent initialized")
    
    async def run(self, session_id: str, input_text: str, model: str) -> str:
        """
        Execute chat in CrewAI agent.
        
        Args:
            session_id: Unique conversation session ID
            input_text: User input text
            model: Model to use for generation
            
        Returns:
            Assistant response text
        """
        try:
            # Retrieve existing conversation state
            state = self.memory.get_state(session_id)
            history: List[Dict[str, str]] = state.get("history", [])
            
            logger.info(f"CrewAI processing for session: {session_id}")
            
            # Add user message to history
            user_message = {"role": "user", "content": input_text}
            history.append(user_message)
            logger.debug(f"Added user message. History length: {len(history)}")
            
            # Generate response using Model Router
            response_data = await self.router.generate(
                prompt=input_text,
                model=model,
                state={"history": history}
            )
            
            response_text = response_data.get("text", "")
            logger.debug(f"Received response from Model Router: {response_text[:100]}...")
            
            # Add assistant message to history
            assistant_message = {"role": "assistant", "content": response_text}
            history.append(assistant_message)
            
            # Save updated state
            self.memory.save_state(session_id, {"history": history})
            logger.info(f"State saved for session {session_id}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error in CrewAIAgent.run: {e}")
            raise
