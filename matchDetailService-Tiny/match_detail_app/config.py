import os
from dotenv import load_dotenv

load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
DB_PATH = os.getenv("DB_PATH", "data/match_details.json")
SERVICE_NAME = os.getenv("SERVICE_NAME", "matchDetailService - TinyDB")

MATCHES_BASE_URL = os.getenv("MATCHES_BASE_URL", "http://localhost:8003")
TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
COMPETITIONS_BASE_URL = os.getenv("COMPETITIONS_BASE_URL", "http://localhost:8002")
PLAYERS_BASE_URL = os.getenv("PLAYERS_BASE_URL", "http://localhost:8005")

REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3.0"))
PORT = int(os.getenv("PORT", 8004))
