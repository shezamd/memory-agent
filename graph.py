from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

import memory
from config import CLAUDE_MODEL


class AgentState(TypedDict):
    user_input: str
    memories: str
    response: str
    user_id: str


llm = ChatAnthropic(model=CLAUDE_MODEL)


def retrieve_memories(state: AgentState) -> dict:
    """Search mem0 for memories relevant to the user's input."""
    memories = memory.search(state["user_input"], state["user_id"])
    return {"memories": memories}


def generate_response(state: AgentState) -> dict:
    """Call Claude with retrieved memories as context."""
    system_parts = [
        "You are a helpful assistant with long-term memory.",
        "You remember things the user has told you in previous conversations.",
        "Use the memories below to personalize your responses.",
        "If memories are empty, that's fine — just respond normally.",
    ]
    if state["memories"]:
        system_parts.append(f"\nRelevant memories:\n{state['memories']}")

    messages = [
        SystemMessage(content="\n".join(system_parts)),
        HumanMessage(content=state["user_input"]),
    ]
    result = llm.invoke(messages)
    return {"response": result.content}


def store_memories(state: AgentState) -> dict:
    """Store the conversation turn in mem0."""
    memory.add(state["user_input"], state["response"], state["user_id"])
    return {}


# Build the graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node("retrieve_memories", retrieve_memories)
graph_builder.add_node("generate_response", generate_response)
graph_builder.add_node("store_memories", store_memories)

graph_builder.add_edge(START, "retrieve_memories")
graph_builder.add_edge("retrieve_memories", "generate_response")
graph_builder.add_edge("generate_response", "store_memories")
graph_builder.add_edge("store_memories", END)

agent = graph_builder.compile()
