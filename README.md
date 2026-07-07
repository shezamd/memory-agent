# Memory Agent

A CLI conversational assistant with **persistent long-term memory** across sessions, built with LangGraph and mem0.

The agent remembers facts you've shared in previous conversations — your preferences, background, past topics — and uses them to personalize future responses. Memory is stored locally using vector search (Qdrant) and automatically extracted from conversations via mem0.

## Architecture

Each user message flows through a 3-node LangGraph pipeline:

```
User Input
    │
    ▼
┌─────────────────────┐
│  retrieve_memories   │  ← search mem0 for relevant past context
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  generate_response   │  ← call Claude with memories in system prompt
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   store_memories     │  ← save conversation turn, auto-extract facts
└─────────────────────┘
```

**Memory extraction is automatic** — mem0 identifies discrete facts from each conversation turn (e.g. "user is from Leicester", "user prefers Python") and stores them as separate embeddings for precise retrieval later.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent framework | [LangGraph](https://github.com/langchain-ai/langgraph) (StateGraph) |
| LLM | Claude Sonnet via [langchain-anthropic](https://github.com/langchain-ai/langchain) |
| Memory layer | [mem0](https://github.com/mem0ai/mem0) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (runs locally) |
| Vector store | [Qdrant](https://qdrant.tech/) (local file-based, no server needed) |
| Package manager | [uv](https://github.com/astral-sh/uv) |

## Project Structure

```
memory_agent/
├── main.py       # CLI entry point — chat loop and user commands
├── graph.py      # LangGraph StateGraph definition and node functions
├── memory.py     # mem0 wrapper — search, add, get_all, delete_all
├── config.py     # mem0 config (LLM, embedder, vector store) and model constants
├── pyproject.toml
└── data/         # local Qdrant storage (gitignored)
```

## Setup

```bash
# Clone the repo
git clone https://github.com/shezamd/memory-agent.git
cd memory-agent

# Install dependencies
uv sync

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run
uv run main.py
```

## Usage

```
$ uv run main.py
Memory Agent — remembers across sessions
Commands: 'memories' | 'forget' | 'quit'

What's your name? shehryar

Hey shehryar! Start chatting.

You: I'm a software engineer working mostly in Python and TypeScript
Assistant: Nice to meet you! I'll remember that you're a software engineer...

You: memories
--- 2 memories ---
  - User is a software engineer
  - User works mostly in Python and TypeScript

You: quit
Bye!
```

The next time you start a session with the same name, the agent will recall what you've told it.

## CLI Commands

| Command | Description |
|---------|-------------|
| `memories` | Show all stored memories for the current user |
| `forget` | Clear all memories for the current user |
| `quit` / `exit` | End the session |

## How It Works

1. **Retrieve** — On each message, mem0 performs a vector similarity search over stored memory embeddings to find facts relevant to the current input.

2. **Generate** — Retrieved memories are injected into Claude's system prompt as context. Claude uses them to personalize its response without explicit prompting.

3. **Store** — The full conversation turn (user + assistant messages) is passed to mem0, which uses an LLM to extract atomic facts and stores each as a separate vector embedding.

Memory is scoped per user (by name), so multiple people can use the same instance with isolated memory stores.

## License

MIT
