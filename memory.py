from mem0 import Memory
from config import MEM0_CONFIG


memory = Memory.from_config(MEM0_CONFIG)


def search(query: str, user_id: str, limit: int = 5) -> str:
    """Search mem0 for memories relevant to the query. Returns formatted string."""
    results = memory.search(query=query, filters={"user_id": user_id}, top_k=limit)
    if not results.get("results"):
        return ""
    memories = [r["memory"] for r in results["results"]]
    return "\n".join(f"- {m}" for m in memories)


def add(user_msg: str, assistant_msg: str, user_id: str) -> None:
    """Store a conversation turn in mem0."""
    memory.add(
        messages=[
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg},
        ],
        user_id=user_id,
    )


def get_all(user_id: str) -> list[dict]:
    """Return all memories for a user."""
    result = memory.get_all(filters={"user_id": user_id})
    return result.get("results", [])


def delete_all(user_id: str) -> None:
    """Delete all memories for a user."""
    memory.delete_all(user_id=user_id)
