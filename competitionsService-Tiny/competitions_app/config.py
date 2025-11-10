from dotenv import load_dotenv
import os

load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
DB_PATH = os.getenv("DB_PATH", "data/competitions.json")
SERVICE_NAME = os.getenv("SERVICE_NAME", "competitionsService - TinyDB")
TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
MATCHES_BASE_URL = os.getenv("MATCHES_BASE_URL", "http://localhost:8003")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PORT = int(os.getenv("PORT", 8002))
