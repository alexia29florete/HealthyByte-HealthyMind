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
      nutrients: {
        calories, protein_g, carbs_g, fat_g, fiber_g,
        iron_mg, potassium_mg, calcium_mg, vitamin_a_mcg, vitamin_c_mg, vitamin_d_mcg
      }
      feedback: string (EN)
      detected_foods: list[str]
      detected_emotions: list[str]
    """
    client = _get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    # trimitem payload structurat (meals/snacks/wellness/rest/fitness) + entry_text
    prompt = f"""
You are a professional and empathetic nutrition & wellness assistant.

You will receive a JSON payload describing a user's day:
- meals/snacks: foods with quantities in grams (may be missing/unknown)
- wellness: mood/energy/focus (1-10)
- rest: sleep hours + sleep interval (e.g. "22-06")
- fitness: activities + duration minutes
- notes: free text summary

TASK:
1) Estimate TOTAL nutrients for the whole day including both macronutrients and micronutrients:
   MACRONUTRIENTS: calories, protein_g, carbs_g, fat_g, fiber_g
   MICRONUTRIENTS: iron_mg, potassium_mg, calcium_mg, vitamin_a_mcg, vitamin_c_mg, vitamin_d_mcg
2) Detect a short list of foods (lowercase) and emotions (lowercase).
3) Generate a relevant "Quote of the Day" related to health, nutrition, wellbeing, or life balance based on user's mood and context. Include author if it's a known quote.
4) Provide DETAILED, empathetic personalized advice IN ENGLISH. Include:
   - Analysis of nutritional balance (what's good, what's missing, what's excessive)
   - Impact on emotional state and energy levels based on their wellness data
   - Practical suggestions for improvement
   - Empathetic feedback addressing their current mood/energy
   - A specific, detailed recommendation for the next meal
5) Output STRICT JSON ONLY, no extra text.

CRITICAL: The nutritional summary will be displayed separately. DO NOT repeat nutrient numbers in feedback.

OUTPUT JSON SCHEMA:
{{
  "nutrients": {{
    "calories": number,
    "protein_g": number,
    "carbs_g": number,
    "fat_g": number,
    "fiber_g": number,
    "iron_mg": number,
    "potassium_mg": number,
    "calcium_mg": number,
    "vitamin_a_mcg": number,
    "vitamin_c_mg": number,
    "vitamin_d_mcg": number
  }},
  "detected_foods": [string, ...],
  "detected_emotions": [string, ...],
  "quote_of_the_day": "string (inspirational quote relevant to health/nutrition/wellbeing)",
  "quote_author": "string (author name if known, empty string if not)",
  "feedback": "string in English (3-4 detailed paragraphs with comprehensive analysis, DO NOT include nutrient numbers)",
  "next_meal_idea": "string in English (detailed meal suggestion with rationale)"
}}

INPUT JSON:
{json.dumps({"payload": payload, "notes": entry_text}, ensure_ascii=False)}
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional, empathetic nutrition and wellness assistant. Provide comprehensive, detailed analysis and suggestions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    text = resp.choices[0].message.content or ""
    data = _safe_json_loads(text)

    # normalizează/curăță
    nutrients = data.get("nutrients") or {}
    
    # Build nutritional summary string
    nutritional_summary = f"""**NUTRITIONAL SUMMARY**

Macronutrients:
- Total Calories: {float(nutrients.get("calories", 0) or 0):.1f} kcal
- Protein: {float(nutrients.get("protein_g", 0) or 0):.1f} g
- Carbohydrates: {float(nutrients.get("carbs_g", 0) or 0):.1f} g
- Fat: {float(nutrients.get("fat_g", 0) or 0):.1f} g
- Fiber: {float(nutrients.get("fiber_g", 0) or 0):.1f} g

Micronutrients:
- Iron: {float(nutrients.get("iron_mg", 0) or 0):.1f} mg
- Potassium: {float(nutrients.get("potassium_mg", 0) or 0):.1f} mg
- Calcium: {float(nutrients.get("calcium_mg", 0) or 0):.1f} mg
- Vitamin A: {float(nutrients.get("vitamin_a_mcg", 0) or 0):.1f} µg
- Vitamin C: {float(nutrients.get("vitamin_c_mg", 0) or 0):.1f} mg
- Vitamin D: {float(nutrients.get("vitamin_d_mcg", 0) or 0):.1f} µg


"""
    
    # Build quote section
    quote_text = (data.get("quote_of_the_day") or "").strip()
    quote_author = (data.get("quote_author") or "").strip()
    quote_section = ""
    if quote_text:
        if quote_author:
            quote_section = f'**QUOTE OF THE DAY**\n"{quote_text}"\n— {quote_author}\n\n---\n\n'
        else:
            quote_section = f'**QUOTE OF THE DAY**\n"{quote_text}"\n\n---\n\n'
    
    # Combine everything
    feedback_text = (data.get("feedback") or "").strip()
    next_meal_text = (data.get("next_meal_idea") or "").strip()
    
    full_feedback = nutritional_summary + quote_section + feedback_text
    if next_meal_text:
        full_feedback += f"\n\n**Next meal idea:** {next_meal_text}"
    
    out = {
        "nutrients": {
            # Macronutrients
            "calories": float(nutrients.get("calories", 0) or 0),
            "protein_g": float(nutrients.get("protein_g", 0) or 0),
            "carbs_g": float(nutrients.get("carbs_g", 0) or 0),
            "fat_g": float(nutrients.get("fat_g", 0) or 0),
            "fiber_g": float(nutrients.get("fiber_g", 0) or 0),
            # Micronutrients
            "iron_mg": float(nutrients.get("iron_mg", 0) or 0),
            "potassium_mg": float(nutrients.get("potassium_mg", 0) or 0),
            "calcium_mg": float(nutrients.get("calcium_mg", 0) or 0),
            "vitamin_a_mcg": float(nutrients.get("vitamin_a_mcg", 0) or 0),
            "vitamin_c_mg": float(nutrients.get("vitamin_c_mg", 0) or 0),
            "vitamin_d_mcg": float(nutrients.get("vitamin_d_mcg", 0) or 0),
            "source": "openai",
        },
        "detected_foods": [str(x).strip().lower() for x in (data.get("detected_foods") or []) if str(x).strip()],
        "detected_emotions": [str(x).strip().lower() for x in (data.get("detected_emotions") or []) if str(x).strip()],
        "feedback": full_feedback,
        "next_meal_idea": "",  # Already included in feedback
    }
    return out
