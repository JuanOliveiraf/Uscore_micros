import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


def _csv(value: str, default: str = ""):
	raw = value or default
	return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
	def __init__(self):
		self.cors_origins = _csv(os.getenv("CORS_ORIGINS"), "http://localhost:5173,http://localhost:3000")
		self.db_path = os.getenv("DB_PATH", "data/match_details.json")
		self.service_name = os.getenv("SERVICE_NAME", "matchDetailService - TinyDB")
		self.matches_base_url = os.getenv("MATCHES_BASE_URL", "http://localhost:8003")
		self.teams_base_url = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
		self.competitions_base_url = os.getenv("COMPETITIONS_BASE_URL", "http://localhost:8002")
		self.players_base_url = os.getenv("PLAYERS_BASE_URL", "http://localhost:8005")
		self.request_timeout = float(os.getenv("REQUEST_TIMEOUT", "3.0"))
		self.port = int(os.getenv("PORT", 8004))
		self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
		self.jwt_secret = os.getenv("JWT_SECRET", "change-me")
		self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
		self.api_keys = _csv(os.getenv("API_KEYS", "local-dev-key"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	return Settings()


settings = get_settings()

# Backwards compatible constants
CORS_ORIGINS = settings.cors_origins
DB_PATH = settings.db_path
SERVICE_NAME = settings.service_name

MATCHES_BASE_URL = settings.matches_base_url
TEAMS_BASE_URL = settings.teams_base_url
COMPETITIONS_BASE_URL = settings.competitions_base_url
PLAYERS_BASE_URL = settings.players_base_url

REQUEST_TIMEOUT = settings.request_timeout
PORT = settings.port
