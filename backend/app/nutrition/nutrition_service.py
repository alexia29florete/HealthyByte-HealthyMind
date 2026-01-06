from typing import List, Dict, Any, Union
import hashlib
from flask import current_app
from .api_client import NutritionApiClient
from .nutrient_parser import parse_edamam

def _mock_nutrients(foods: List[str]) -> Dict[str, Any]:
    # Deterministic mock based on hash for stable dev/testing.
    seed = int(hashlib.md5((",".join(foods)).encode("utf-8")).hexdigest()[:8], 16) if foods else 0
    calories = 250 + (seed % 550)
    protein = 10 + (seed % 30)
    carbs = 30 + (seed % 70)
    fat = 8 + (seed % 25)
    fiber = 3 + (seed % 15)
    return {
        "calories": calories,
        "protein_g": protein,
        "carbs_g": carbs,
        "fat_g": fat,
        "fiber_g": fiber,
        "source": "mock"
    }

def analyze_foods(foods: Union[List[str], List[Dict[str, Any]]]) -> Dict[str, Any]:
    # Prefer Edamam if configured, else mock.
    ingredient_lines: List[str] = []
    food_names: List[str] = []

    if foods and isinstance(foods, list) and isinstance(foods[0], dict):
        for it in foods:  # new format
            if not isinstance(it, dict):
                continue
            food = (it.get("food") or "").strip()
            qty = it.get("quantity_g")
            if not food:
                continue
            food_names.append(food)

            if isinstance(qty, (int, float)):
                ingredient_lines.append(f"{int(qty)} g {food}")
            else:
                ingredient_lines.append(food)
    else:
        # old format
        for f in (foods or []):
            s = str(f).strip()
            if s:
                food_names.append(s)
                ingredient_lines.append(s)

    app_id = getattr(current_app.config, "EDAMAM_APP_ID", "") or current_app.config.get("EDAMAM_APP_ID", "")
    app_key = getattr(current_app.config, "EDAMAM_APP_KEY", "") or current_app.config.get("EDAMAM_APP_KEY", "")

    client = NutritionApiClient(app_id, app_key)

    if client.enabled and ingredient_lines:
        # Very simple ingredient text; you can improve by adding quantities.
        ingredients_text = ", ".join(ingredient_lines)
        resp = client.edamam_analyze(ingredients_text)
        if resp:
            return parse_edamam(resp)

    return _mock_nutrients([x.lower() for x in food_names])