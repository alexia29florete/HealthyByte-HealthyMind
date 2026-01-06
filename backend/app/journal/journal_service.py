from typing import Dict, Any, Optional, List
from datetime import date, datetime

from ..models import JournalEntry
from ..utils.json_utils import dumps, loads
from ..ai.nlp_processor import analyze_entry
from ..ai.feedback_engine import generate_feedback
from ..nutrition.nutrition_service import analyze_foods
from .journal_repository import JournalRepository


def _parse_date(d: Optional[str]) -> date:
    if not d:
        return date.today()
    try:
        return datetime.fromisoformat(d).date()
    except Exception:
        return date.today()


def _unique_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _collect_food_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect food items from the UI payload.

    Expected UI shape:
      main_meals: { breakfast: [{food, quantity_g}, ...], lunch: [...], dinner: [...] }
      snacks: { snack1: [...], snack2: [...], snack3: [...] }
    """
    items: List[Dict[str, Any]] = []

    mm = payload.get("main_meals") or {}
    snacks = payload.get("snacks") or {}

    def add_list(lst):
        if not isinstance(lst, list):
            return
        for x in lst:
            if not isinstance(x, dict):
                continue
            food = (x.get("food") or "").strip()
            qty = x.get("quantity_g")
            if food:
                items.append({"food": food, "quantity_g": qty})

    # main meals
    if isinstance(mm, dict):
        add_list(mm.get("breakfast"))
        add_list(mm.get("lunch"))
        add_list(mm.get("dinner"))

    # snacks
    if isinstance(snacks, dict):
        add_list(snacks.get("snack1"))
        add_list(snacks.get("snack2"))
        add_list(snacks.get("snack3"))

    return items


def _build_entry_text(payload: Dict[str, Any]) -> str:
    """Create a readable text from structured fields (useful for feedback/NLP)."""
    lines: List[str] = []

    # Foods with quantities
    for it in _collect_food_items(payload):
        food = it.get("food")
        qty = it.get("quantity_g")
        if isinstance(qty, (int, float)):
            lines.append(f"{food} {int(qty)}g")
        else:
            lines.append(str(food))

    # Optional free-text notes (if frontend sends it)
    notes = (payload.get("entry_text") or "").strip()
    if notes:
        lines.append("Notes: " + notes)

    # Wellness
    w = payload.get("wellness") or {}
    if isinstance(w, dict):
        for key in ("mood", "energy", "focus"):
            if w.get(key) is not None:
                lines.append(f"{key.capitalize()}: {w.get(key)}/10")

    # Rest
    r = payload.get("rest") or {}
    if isinstance(r, dict):
        if r.get("sleep_hours") is not None:
            lines.append(f"Sleep hours: {r.get('sleep_hours')}")
        if r.get("sleep_interval"):
            lines.append(f"Sleep interval: {r.get('sleep_interval')}")  # e.g. "22-6"

    # Fitness
    f = payload.get("fitness") or []
    if isinstance(f, list):
        for ex in f:
            if not isinstance(ex, dict):
                continue
            name = (ex.get("exercise") or "").strip()
            t = ex.get("time_min")
            if name and t is not None:
                lines.append(f"Exercise: {name} ({t} min)")

    return "\n".join([x for x in lines if x]).strip()


def _emotions_from_wellness(wellness: Any) -> List[str]:
    """Derive a simple emotions list from wellness sliders (1..10)."""
    if not isinstance(wellness, dict):
        return []

    emotions: List[str] = []
    mood = wellness.get("mood")
    energy = wellness.get("energy")
    focus = wellness.get("focus")

    # Mood
    if isinstance(mood, (int, float)):
        if mood <= 3:
            emotions.append("sad")
        elif mood >= 8:
            emotions.append("happy")

    # Energy
    if isinstance(energy, (int, float)):
        if energy <= 3:
            emotions.append("tired")
        elif energy >= 8:
            emotions.append("energized")

    # Focus
    if isinstance(focus, (int, float)):
        if focus <= 3:
            emotions.append("distracted")
        elif focus >= 8:
            emotions.append("focused")

    return emotions


class JournalService:
    @staticmethod
    def create_entry(user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        # 1) Build text representation (for NLP/feedback)
        entry_text = _build_entry_text(payload)
        if not entry_text:
            raise ValueError("Journal payload is empty.")

        # 2) Foods come from structured UI (more reliable than NLP)
        food_items = _collect_food_items(payload)
        food_names = [it.get("food") for it in food_items if isinstance(it, dict) and it.get("food")]
        food_names = _unique_preserve_order([str(x).strip().lower() for x in food_names if str(x).strip()])

        # 3) Emotions: from wellness sliders + (optional) NLP from notes
        wellness = payload.get("wellness") or {}
        emotions = _emotions_from_wellness(wellness)

        notes = (payload.get("entry_text") or "").strip()
        if notes:
            analysis = analyze_entry(notes)
            emotions += analysis.get("emotions", [])

        emotions = _unique_preserve_order([str(x).strip().lower() for x in emotions if str(x).strip()])

        # 4) Nutrition uses quantities (quantity_g) if available
        nutrients = analyze_foods(food_items)

        # 5) Feedback (foods + emotions + nutrients)
        feedback = generate_feedback(food_names, emotions, nutrients)

        # 6) Scalars
        w = wellness if isinstance(wellness, dict) else {}
        rest = payload.get("rest") or {}
        r = rest if isinstance(rest, dict) else {}

        entry = JournalEntry(
            user_id=user_id,
            entry_text=entry_text,
            entry_date=_parse_date(payload.get("date")),

            detected_foods=dumps(food_names),
            detected_emotions=dumps(emotions),
            nutrients=dumps(nutrients),
            feedback=feedback,

            # store structured payload as JSON string
            main_meals=dumps(payload.get("main_meals")) if payload.get("main_meals") is not None else None,
            snacks=dumps(payload.get("snacks")) if payload.get("snacks") is not None else None,
            wellness=dumps(payload.get("wellness")) if payload.get("wellness") is not None else None,
            rest=dumps(payload.get("rest")) if payload.get("rest") is not None else None,
            fitness=dumps(payload.get("fitness")) if payload.get("fitness") is not None else None,

            # scalar copies
            mood=w.get("mood") if w.get("mood") is not None else None,
            energy=w.get("energy") if w.get("energy") is not None else None,
            focus=w.get("focus") if w.get("focus") is not None else None,
            sleep_hours=r.get("sleep_hours") if r.get("sleep_hours") is not None else None,
            sleep_interval=r.get("sleep_interval") if r.get("sleep_interval") else None,
        )

        JournalRepository.create(entry)
        return JournalService.to_dict(entry)

    @staticmethod
    def to_dict(entry: JournalEntry) -> Dict[str, Any]:
        return {
            "id": entry.id,
            "user_id": entry.user_id,
            "entry_text": entry.entry_text,
            "date": entry.entry_date.isoformat(),

            "detected_foods": loads(entry.detected_foods, []),
            "detected_emotions": loads(entry.detected_emotions, []),
            "nutrients": loads(entry.nutrients, {}),
            "feedback": entry.feedback,

            # structured payload returned to frontend
            "main_meals": loads(entry.main_meals, None),
            "snacks": loads(entry.snacks, None),
            "wellness": loads(entry.wellness, None),
            "rest": loads(entry.rest, None),
            "fitness": loads(entry.fitness, None),

            # scalar convenience fields
            "mood": entry.mood,
            "energy": entry.energy,
            "focus": entry.focus,
            "sleep_hours": entry.sleep_hours,
            "sleep_interval": entry.sleep_interval,

            "created_at": entry.created_at.isoformat()
        }

    @staticmethod
    def get_entry(user_id: int, entry_id: int) -> Dict[str, Any]:
        entry = JournalRepository.get_by_id(entry_id, user_id)
        if not entry:
            raise ValueError("Entry not found.")
        return JournalService.to_dict(entry)

    @staticmethod
    def list_entries(user_id: int, limit: int = 50, offset: int = 0, entry_date: Optional[str] = None):
        d = _parse_date(entry_date) if entry_date else None
        entries = JournalRepository.list(user_id, limit=limit, offset=offset, entry_date=d)
        return [JournalService.to_dict(e) for e in entries]

    @staticmethod
    def delete_entry(user_id: int, entry_id: int):
        entry = JournalRepository.get_by_id(entry_id, user_id)
        if not entry:
            raise ValueError("Entry not found.")
        JournalRepository.delete(entry)
