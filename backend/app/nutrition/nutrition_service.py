from typing import List, Dict, Any
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

def analyze_foods(foods: List[str]) -> Dict[str, Any]:
    # Prefer Edamam if configured, else mock.
    app_id = getattr(current_app.config, "EDAMAM_APP_ID", "") or current_app.config.get("EDAMAM_APP_ID", "")
    app_key = getattr(current_app.config, "EDAMAM_APP_KEY", "") or current_app.config.get("EDAMAM_APP_KEY", "")

    client = NutritionApiClient(app_id, app_key)

    if client.enabled and foods:
        # Very simple ingredient text; you can improve by adding quantities.
        ingredients_text = " ".join(foods)
        resp = client.edamam_analyze(ingredients_text)
        if resp:
            return parse_edamam(resp)

    return _mock_nutrients(foods)
