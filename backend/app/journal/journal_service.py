from typing import Dict, Any, Optional
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

class JournalService:
    @staticmethod
    def create_entry(user_id: int, entry_text: str, entry_date: Optional[str] = None) -> Dict[str, Any]:
        if not entry_text or not entry_text.strip():
            raise ValueError("entry_text is required.")

        analysis = analyze_entry(entry_text)
        foods = analysis.get("foods", [])
        emotions = analysis.get("emotions", [])

        nutrients = analyze_foods(foods)
        feedback = generate_feedback(foods, emotions, nutrients)

        entry = JournalEntry(
            user_id=user_id,
            entry_text=entry_text.strip(),
            entry_date=_parse_date(entry_date),
            detected_foods=dumps(foods),
            detected_emotions=dumps(emotions),
            nutrients=dumps(nutrients),
            feedback=feedback
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
            "created_at": entry.created_at.isoformat()
        }

    @staticmethod
    def get_entry(user_id: int, entry_id: int) -> Dict[str, Any]:
        entry = JournalRepository.get_by_id(entry_id, user_id)
        if not entry:
            raise ValueError("Entry not found.")
        return JournalService.to_dict(entry)

    @staticmethod
    def list_entries(user_id: int, limit: int = 50, offset: int = 0):
        entries = JournalRepository.list(user_id, limit=limit, offset=offset)
        return [JournalService.to_dict(e) for e in entries]

    @staticmethod
    def delete_entry(user_id: int, entry_id: int):
        entry = JournalRepository.get_by_id(entry_id, user_id)
        if not entry:
            raise ValueError("Entry not found.")
        JournalRepository.delete(entry)
