# Memory Agent

CLI conversational assistant with persistent memory across sessions. Built to learn how agents with memory work.

## Stack
- **Agent framework**: LangGraph (StateGraph with 3 nodes)
- **LLM**: Claude Sonnet via `langchain-anthropic` (`ChatAnthropic`)
- **Memory**: mem0 — stores, extracts, and retrieves facts from conversations
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (local, free)
- **Vector store**: Qdrant (local, default at `/tmp/qdrant`)
- **Package manager**: uv

## Architecture

The LangGraph StateGraph runs 3 nodes in sequence per user message:

```
retrieve_memories → generate_response → store_memories
```

1. **retrieve_memories** — searches mem0 for past context relevant to user input
2. **generate_response** — calls Claude with retrieved memories injected into system prompt
3. **store_memories** — saves the conversation turn to mem0 (auto-extracts facts)

## Files
- `config.py` — mem0 config (LLM provider, embedder, vector store) and Claude model constant
- `memory.py` — mem0 wrapper: `search()`, `add()`, `get_all()`, `delete_all()`
- `graph.py` — LangGraph StateGraph definition, node functions, compiled `agent`
- `main.py` — CLI entry point with chat loop and commands (`memories`, `forget`, `quit`)

## State Schema (graph.py)
```python
class AgentState(TypedDict):
    user_input: str    # current user message
    memories: str      # retrieved memories from mem0
    response: str      # Claude's response
    user_id: str       # scopes memories per user
```

## Running
```bash
export ANTHROPIC_API_KEY="..."
uv run main.py
```

## CLI Commands
- `memories` — show all stored memories for current user
- `forget` — clear all memories
- `quit` / `exit` — end session
