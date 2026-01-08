import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///healthybyte.db")
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.AI_LANGUAGE = os.getenv("AI_LANGUAGE", "en").lower()

        # Nutrition API keys (optional)
        self.EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID", "")
        self.EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY", "")

        # OpenAI (optional)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.AI_ENABLED = os.getenv("AI_ENABLED", "false").lower() == "true"

        # MCP OpenNutrition (optional)
        self.MCP_OPENNUTRITION_PATH = os.getenv("MCP_OPENNUTRITION_PATH", "")
        self.NODE_PATH = os.getenv("NODE_PATH", "node")
