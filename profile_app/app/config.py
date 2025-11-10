from dotenv import load_dotenv
import os

# 🔹 Carrega as variáveis do .env
load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

DB_PATH = os.getenv("DB_PATH", "data/profiles.json")

SERVICE_NAME = os.getenv("SERVICE_NAME", "profileService - TinyDB")

TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
COMPETITIONS_BASE_URL = os.getenv("COMPETITIONS_BASE_URL", "http://localhost:8002")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PORT = int(os.getenv("PORT", 8000))
