from typing import List, Dict, Any
from .smart_ai import generate_ai_feedback


def generate_feedback(foods: List[str], emotions: List[str], nutrients: Dict[str, Any], user_text: str = "") -> str:
    """
    AI-only feedback. If AI fails, raise error.
    """
    ai_text = generate_ai_feedback(user_text or "")
    if not ai_text:
        raise ValueError("AI feedback failed: check OPENAI_API_KEY / MCP config.")
    return ai_text
