from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import pandas as pd
from datetime import timedelta
from ..models import JournalEntry
from ..utils.json_utils import loads


def _parse_date(d: Optional[str]) -> Optional[date]:
    if not d:
        return None
    try:
        return datetime.fromisoformat(d).date()
    except Exception:
        return None


def _last_7_days_labels():
    # etichetele sunt fixe în UI-ul vostru (Mo..Su), deci returnăm doar valori.
    # (dacă vrei, poți calcula din calendar real)
    return ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


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

        # 1) burned din nutrients (dacă există)
        burned = float(nutrients.get("burned_calories", 0) or 0)

        # 2) fallback: calculează burned din fitness dacă lipsește
        if burned == 0:
            fitness = loads(e.fitness, [])
            if isinstance(fitness, list):
                for ex in fitness:
                    if not isinstance(ex, dict):
                        continue
                    try:
                        mins = float(ex.get("time_min", 0) or 0)
                    except Exception:
                        mins = 0.0
                    burned += 7.0 * mins  # ~7 kcal/min

        rows.append({
            "date": e.entry_date.isoformat(),
            "consumed_calories": float(nutrients.get("calories", 0) or 0),
            "burned_calories": burned,
            "protein_g": float(nutrients.get("protein_g", 0) or 0),
            "carbs_g": float(nutrients.get("carbs_g", 0) or 0),
            "fat_g": float(nutrients.get("fat_g", 0) or 0),
            "fiber_g": float(nutrients.get("fiber_g", 0) or 0),
            "sleep_hours": float(e.sleep_hours or 0),
            "mood": float(e.mood or 0),
            "emotions": emotions,
        })



    if not rows:
        return {
            "calories_trend": [],
            "macros_totals": {"protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0},
            "emotions_frequency": {},
            "charts": {
                "labels": _last_7_days_labels(),
                "sleep_hours": [0, 0, 0, 0, 0, 0, 0],
                "burned_calories": [0, 0, 0, 0, 0, 0, 0],
                "consumed_calories": [0, 0, 0, 0, 0, 0, 0],
                "happiness": [0, 0, 0, 0, 0, 0, 0],
            }
        }

    df = pd.DataFrame(rows)

    # trend total calories per day (consumed)
    calories_trend = df.groupby("date", as_index=False)["consumed_calories"].sum()
    calories_trend = calories_trend.rename(columns={"consumed_calories": "calories"}).to_dict("records")

    macros = {
        "protein_g": float(df["protein_g"].sum()),
        "carbs_g": float(df["carbs_g"].sum()),
        "fat_g": float(df["fat_g"].sum()),
        "fiber_g": float(df["fiber_g"].sum()),
    }

    emo = df[["date", "emotions"]].explode("emotions")
    emo = emo[emo["emotions"].notna() & (emo["emotions"] != "")]
    emotions_frequency = emo["emotions"].value_counts().to_dict()

    # last 7 days series (calendar)
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]  # 7 zile
    day_keys = [d.isoformat() for d in days]

    per_day = df.groupby("date", as_index=False).agg({
        "sleep_hours": "max",
        "burned_calories": "sum",
        "consumed_calories": "sum",
        "mood": "max",
    })
    per_day_map = {r["date"]: r for r in per_day.to_dict("records")}

    sleep_vals = []
    burned_vals = []
    consumed_vals = []
    mood_vals = []

    for dk in day_keys:
        r = per_day_map.get(dk, {})
        sleep_vals.append(float(r.get("sleep_hours", 0) or 0))
        burned_vals.append(float(r.get("burned_calories", 0) or 0))
        consumed_vals.append(float(r.get("consumed_calories", 0) or 0))
        mood_vals.append(float(r.get("mood", 0) or 0))

    return {
        "calories_trend": calories_trend,
        "macros_totals": macros,
        "emotions_frequency": emotions_frequency,
        "charts": {
            "labels": _last_7_days_labels(),
            "sleep_hours": sleep_vals,
            "burned_calories": burned_vals,
            "consumed_calories": consumed_vals,
            "happiness": mood_vals,
        }
    }
