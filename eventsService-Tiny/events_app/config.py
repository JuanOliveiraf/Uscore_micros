import os
from dotenv import load_dotenv

load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
DB_PATH = os.getenv("DB_PATH", "data/events.json")
SERVICE_NAME = os.getenv("SERVICE_NAME", "eventsService - TinyDB")
MATCH_DETAIL_BASE_URL = os.getenv("MATCH_DETAIL_BASE_URL", "http://localhost:8004")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3.0"))
PORT = int(os.getenv("PORT", 8006))
BROADCAST_PATH = os.getenv("BROADCAST_PATH", "/broadcast/event.created")
