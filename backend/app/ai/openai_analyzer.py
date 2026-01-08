import json
import os
import re
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Put it in backend/.env")
    return OpenAI(api_key=api_key)


def _safe_json_loads(text: str) -> Dict[str, Any]:
    text = (text or "").strip()

    # dacă modelul pune ```json ... ```
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except Exception:
        # fallback: încearcă să găsească un obiect JSON în text
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise


def analyze_day_with_openai(payload: Dict[str, Any], entry_text: str) -> Dict[str, Any]:
    """
    Returnează dict cu:
      nutrients: {calories, protein_g, carbs_g, fat_g, fiber_g, burned_calories?}
      feedback: string (EN)
      detected_foods: list[str]
      detected_emotions: list[str]
    """
    client = _get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    # trimitem payload structurat (meals/snacks/wellness/rest/fitness) + entry_text
    prompt = f"""
You are a nutrition & wellness assistant.

You will receive a JSON payload describing a user's day:
- meals/snacks: foods with quantities in grams (may be missing/unknown)
- wellness: mood/energy/focus (1-10)
- rest: sleep hours + sleep interval (e.g. "22-06")
- fitness: activities + duration minutes
- notes: free text summary

TASK:
1) Estimate TOTAL nutrients for the whole day: calories, protein_g, carbs_g, fat_g, fiber_g.
2) Detect a short list of foods (lowercase) and emotions (lowercase).
3) Provide empathetic personalized advice IN ENGLISH for the user, and a next meal idea.
4) Output STRICT JSON ONLY, no extra text.

OUTPUT JSON SCHEMA:
{{
  "nutrients": {{
    "calories": number,
    "protein_g": number,
    "carbs_g": number,
    "fat_g": number,
    "fiber_g": number
  }},
  "detected_foods": [string, ...],
  "detected_emotions": [string, ...],
  "feedback": "string in English (short paragraph)",
  "next_meal_idea": "string in English (one sentence)"
}}

INPUT JSON:
{json.dumps({"payload": payload, "notes": entry_text}, ensure_ascii=False)}
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    text = resp.choices[0].message.content or ""
    data = _safe_json_loads(text)

    # normalizează/curăță
    nutrients = data.get("nutrients") or {}
    out = {
        "nutrients": {
            "calories": float(nutrients.get("calories", 0) or 0),
            "protein_g": float(nutrients.get("protein_g", 0) or 0),
            "carbs_g": float(nutrients.get("carbs_g", 0) or 0),
            "fat_g": float(nutrients.get("fat_g", 0) or 0),
            "fiber_g": float(nutrients.get("fiber_g", 0) or 0),
            "source": "openai",
        },
        "detected_foods": [str(x).strip().lower() for x in (data.get("detected_foods") or []) if str(x).strip()],
        "detected_emotions": [str(x).strip().lower() for x in (data.get("detected_emotions") or []) if str(x).strip()],
        "feedback": (data.get("feedback") or "").strip(),
        "next_meal_idea": (data.get("next_meal_idea") or "").strip(),
    }
    return out
