from typing import Dict, Any, Optional
import requests

class NutritionApiClient:
    def __init__(self, edamam_app_id: str = "", edamam_app_key: str = "", timeout_s: int = 10):
        self.app_id = (edamam_app_id or "").strip()
        self.app_key = (edamam_app_key or "").strip()
        self.timeout_s = timeout_s

    @property
    def enabled(self) -> bool:
        return bool(self.app_id and self.app_key)

    def edamam_analyze(self, ingredients_text: str) -> Optional[Dict[str, Any]]:
        # Edamam Nutrition Analysis API expects JSON: {"ingr": ["1 apple", "2 eggs", ...]}
        url = "https://api.edamam.com/api/nutrition-details"
        params = {"app_id": self.app_id, "app_key": self.app_key}
        payload = {"ingr": [ingredients_text]}

        r = requests.post(url, params=params, json=payload, timeout=self.timeout_s)
        if r.status_code >= 400:
            return None
        return r.json()
