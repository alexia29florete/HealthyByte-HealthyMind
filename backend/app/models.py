from datetime import datetime, date
from sqlalchemy import func
from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    dietary_preferences = db.Column(db.Text, nullable=True)  # JSON as string
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    entries = db.relationship("JournalEntry", back_populates="user", cascade="all, delete-orphan")

class JournalEntry(db.Model):
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    entry_text = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)

    detected_foods = db.Column(db.Text, nullable=True)       # JSON string
    detected_emotions = db.Column(db.Text, nullable=True)    # JSON string
    nutrients = db.Column(db.Text, nullable=True)            # JSON string
    feedback = db.Column(db.Text, nullable=True)             # generated

    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    user = db.relationship("User", back_populates="entries")
