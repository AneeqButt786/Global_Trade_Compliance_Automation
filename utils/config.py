"""Configuration and environment variable handling."""

import os
from dotenv import load_dotenv

load_dotenv()


def get_config():
    """Load and validate configuration from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your API key."
        )
    return {
        "openai_api_key": api_key,
        "model_name": os.environ.get("MODEL_NAME", "gpt-4o-mini"),
    }
