from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

KNOWLEDGE_DIR = ROOT_DIR / "knowledge_base"
VECTOR_STORE_DIR = ROOT_DIR / "vector_store"
MCP_SERVER_PATH = ROOT_DIR / "src" / "mcp_server.py"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
EMBEDDING_MODEL = "BAAI/bge-m3"


def require_api_key() -> str:
    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("replace_"):
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Copy .env.example to .env and add your key."
        )
    return GEMINI_API_KEY
