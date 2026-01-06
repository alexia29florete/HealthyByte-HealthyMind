from typing import Dict, Any, List, Optional
from datetime import datetime, date
import pandas as pd
from ..models import JournalEntry
from ..utils.json_utils import loads

def _parse_date(d: Optional[str]) -> Optional[date]:
    if not d:
        return None
    try:
        return datetime.fromisoformat(d).date()
    except Exception:
        return None

def compute_summary(user_id: int, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Dict[str, Any]:
    d_from = _parse_date(date_from)
    d_to = _parse_date(date_to)

    q = JournalEntry.query.filter_by(user_id=user_id)
    if d_from:
        q = q.filter(JournalEntry.entry_date >= d_from)
    if d_to:
        q = q.filter(JournalEntry.entry_date <= d_to)

    entries: List[JournalEntry] = q.order_by(JournalEntry.entry_date.asc()).all()

    rows = []
    for e in entries:
        nutrients = loads(e.nutrients, {})
        emotions = loads(e.detected_emotions, [])
        rows.append({
            "date": e.entry_date.isoformat(),
            "calories": float(nutrients.get("calories", 0) or 0),
            "protein_g": float(nutrients.get("protein_g", 0) or 0),
            "carbs_g": float(nutrients.get("carbs_g", 0) or 0),
            "fat_g": float(nutrients.get("fat_g", 0) or 0),
            "fiber_g": float(nutrients.get("fiber_g", 0) or 0),
            "emotions": emotions
        })

    if not rows:
        return {
            "calories_trend": [],
            "macros_totals": {"protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0},
            "emotions_frequency": {}
        }

    df = pd.DataFrame(rows)
    calories_trend = df.groupby("date", as_index=False)["calories"].sum().to_dict("records")

    macros = {
        "protein_g": float(df["protein_g"].sum()),
        "carbs_g": float(df["carbs_g"].sum()),
        "fat_g": float(df["fat_g"].sum()),
        "fiber_g": float(df["fiber_g"].sum()),
    }

    # explode emotions
    emo = df[["date","emotions"]].explode("emotions")
    emo = emo[emo["emotions"].notna() & (emo["emotions"] != "")]
    emotions_frequency = emo["emotions"].value_counts().to_dict()

    return {
        "calories_trend": calories_trend,
        "macros_totals": macros,
        "emotions_frequency": emotions_frequency
    }
