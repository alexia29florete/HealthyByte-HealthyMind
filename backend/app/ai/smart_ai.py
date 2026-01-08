from __future__ import annotations

from typing import Optional
import os
import sys
import asyncio
import contextlib
import io
import importlib.util
from flask import current_app

def _load_smart_analyzer_module() -> Optional[object]:
    """
    Load ../ai/smart_analyzer.py dynamically without requiring it to be a Python package.
    Returns the loaded module or None.
    """
    # Repo layout: <repo>/backend/app/ai/smart_ai.py
    # smart_analyzer.py lives at: <repo>/ai/smart_analyzer.py
    here = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", "..", "..", ".."))
    candidate = os.path.join(repo_root, "ai", "smart_analyzer.py")
    if not os.path.exists(candidate):
        return None

    spec = importlib.util.spec_from_file_location("hbhm_smart_analyzer", candidate)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module

def _run_async(coro):
    """
    Run an async coroutine from sync Flask context, safely.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # When already in an event loop, create a new one in a separate thread-like context:
        # For simplicity in Flask dev, we fallback to asyncio.run via a new loop.
        new_loop = asyncio.new_event_loop()
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
    else:
        return asyncio.run(coro)

def generate_ai_feedback(user_text: str) -> Optional[str]:
    """
    Uses the team's AI module (ai/smart_analyzer.py) if configured.
    Returns feedback text or None if AI is disabled/unavailable.
    """
    if not current_app.config.get("AI_ENABLED"):
        return None

    if not current_app.config.get("OPENAI_API_KEY"):
        return None

    # The AI module itself expects these env vars:
    # - OPENAI_API_KEY
    # - MCP_OPENNUTRITION_PATH (optional but required for full MCP run)
    # - NODE_PATH (optional)
    os.environ.setdefault("OPENAI_API_KEY", current_app.config.get("OPENAI_API_KEY", ""))
    os.environ.setdefault("NODE_PATH", current_app.config.get("NODE_PATH", "node"))
    mcp_path = current_app.config.get("MCP_OPENNUTRITION_PATH") or ""
    if mcp_path:
        os.environ.setdefault("MCP_OPENNUTRITION_PATH", mcp_path)

    module = _load_smart_analyzer_module()
    if module is None:
        return None

    SmartFoodAnalyzer = getattr(module, "SmartFoodAnalyzer", None)
    if SmartFoodAnalyzer is None:
        return None

    try:
        analyzer = SmartFoodAnalyzer()

        # analyze_complete is async and prints to stdout; suppress prints for API responses
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            text = _run_async(analyzer.analyze_complete(user_text))
        text = (text or "").strip()
        return text or None
    except Exception:
        return None
