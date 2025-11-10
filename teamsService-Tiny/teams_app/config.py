from dotenv import load_dotenv
import os

# 🔹 Carrega o .env
load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
DB_PATH = os.getenv("DB_PATH", "data/teams.json")
SERVICE_NAME = os.getenv("SERVICE_NAME", "teamsService - TinyDB")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PORT = int(os.getenv("PORT", 8001))
