from dotenv import load_dotenv
import os
from types import SimpleNamespace

load_dotenv()

# Basic configuration values (TinyDB-based service)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
DB_PATH = os.getenv("DB_PATH", "data/players.json")
SERVICE_NAME = os.getenv("SERVICE_NAME", "playersService - TinyDB")

TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
MATCHES_BASE_URL = os.getenv("MATCHES_BASE_URL", "http://localhost:8003")

API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PORT = int(os.getenv("PORT", 8005))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3.0"))


# Minimal settings object for compatibility with app.main and run.py
class Settings(SimpleNamespace):
	pass


# Exported instance expected by the application
settings = Settings(port=PORT)
