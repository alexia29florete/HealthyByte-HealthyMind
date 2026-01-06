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

    main_meals = db.Column(db.Text, nullable=True)   # JSON string
    snacks = db.Column(db.Text, nullable=True)       # JSON string

    # Wellness: {mood, energy, focus} (JSON string)
    wellness = db.Column(db.Text, nullable=True)     # JSON string

    # Rest: {sleep_hours, sleep_interval} (JSON string)
    rest = db.Column(db.Text, nullable=True)         # JSON string

    # Fitness: list[{exercise, time_min}] (JSON string)
    fitness = db.Column(db.Text, nullable=True)      # JSON string

    # Scalars (handy for stats / filtering)
    mood = db.Column(db.Integer, nullable=True)
    energy = db.Column(db.Integer, nullable=True)
    focus = db.Column(db.Integer, nullable=True)

    sleep_hours = db.Column(db.Integer, nullable=True)
    sleep_interval = db.Column(db.String(32), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    user = db.relationship("User", back_populates="entries")
