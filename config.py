import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEM0_CONFIG = {
    "custom_instructions": "Always extract atomic facts. Never combine multiple facts into one memory. For example, 'User is Sikh and was born in Leicester on 27th April 1999' should be 3 separate memories: religion, birthplace, and birthday.",
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-6",
            "temperature": 0.1,
            "max_tokens": 2048,
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "all-MiniLM-L6-v2",
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": os.path.join(BASE_DIR, "data", "qdrant"),
            "embedding_model_dims": 384,
        },
    },
}

CLAUDE_MODEL = "claude-sonnet-4-6"
