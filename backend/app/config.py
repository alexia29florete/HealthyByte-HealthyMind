import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///healthybyte.db")
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Nutrition API keys (optional)
        self.EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID", "")
        self.EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY", "")
