from typing import Dict, Any

def parse_edamam(resp: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize to minimal fields for the app.
    # Edamam returns calories + totalNutrients.
    nutrients = resp.get("totalNutrients", {}) if isinstance(resp, dict) else {}
    def _v(key: str):
        v = nutrients.get(key, {})
        return v.get("quantity", 0) if isinstance(v, dict) else 0

    return {
        "calories": resp.get("calories", 0),
        "protein_g": _v("PROCNT"),
        "carbs_g": _v("CHOCDF"),
        "fat_g": _v("FAT"),
        "fiber_g": _v("FIBTG"),
        "source": "edamam"
    }
