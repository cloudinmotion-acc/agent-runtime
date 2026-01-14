from .base import BaseAgent

class SimpleChatAgent(BaseAgent):
    async def run(self, session_id: str, input_text: str, model: str):
        state = self.memory.get_state(session_id)

        history = state.get("history", [])
        history.append({"role": "user", "content": input_text})

        response = await self.router.generate(
            prompt=input_text,
            model=model,
            state={"history": history}
        )

        history.append({"role": "assistant", "content": response["text"]})

        self.memory.save_state(session_id, {"history": history})

        return response["text"]
