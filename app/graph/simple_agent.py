from langgraph.graph import StateGraph
from typing import TypedDict

from app.memory.redis import get_context, set_context
from app.memory.postgres import persist_execution
from app.router_client import call_llm

class AgentState(TypedDict):
    user_id: str
    input: str
    context: str
    output: str

def build_graph():
    graph = StateGraph(AgentState)

    def input_node(state):
        state["context"] = get_context(state["user_id"])
        return state

    def llm_node(state):
        prompt = f"""
        Context:
        {state['context']}

        User input:
        {state['input']}
        """
        state["output"] = call_llm(prompt)
        return state

    def persistence_node(state):
        set_context(state["user_id"], state["output"])
        persist_execution(
            state["user_id"],
            state["input"],
            state["output"]
        )
        return state

    graph.add_node("input", input_node)
    graph.add_node("llm", llm_node)
    graph.add_node("persist", persistence_node)

    graph.set_entry_point("input")
    graph.add_edge("input", "llm")
    graph.add_edge("llm", "persist")
    graph.set_finish_point("persist")

    return graph.compile()
