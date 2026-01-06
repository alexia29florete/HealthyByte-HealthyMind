from typing import List, Optional
from ..extensions import db
from ..models import JournalEntry

class JournalRepository:
    @staticmethod
    def create(entry: JournalEntry) -> JournalEntry:
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_by_id(entry_id: int, user_id: int) -> Optional[JournalEntry]:
        return JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()

    @staticmethod
    def list(user_id: int, limit: int = 50, offset: int = 0) -> List[JournalEntry]:
        return (JournalEntry.query
                .filter_by(user_id=user_id)
                .order_by(JournalEntry.entry_date.desc(), JournalEntry.id.desc())
                .offset(offset)
                .limit(limit)
                .all())

    @staticmethod
    def delete(entry: JournalEntry) -> None:
        db.session.delete(entry)
        db.session.commit()
