from dotenv import load_dotenv
import os

# 🔹 Carrega o .env
load_dotenv()

# 🌍 CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# 📦 Banco
DB_PATH = os.getenv("DB_PATH", "data/teams.json")

# 🧱 Identificação do serviço
SERVICE_NAME = os.getenv("SERVICE_NAME", "teamsService - TinyDB")

# 🔗 Prefixo da API
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

# 🔗 Integração externa — AGORA SIM IMPORTANTE!
COMPETITIONS_BASE_URL = os.getenv("COMPETITIONS_BASE_URL", "http://localhost:8002")

# 🔌 Porta
PORT = int(os.getenv("PORT", 8001))

# Config extra opcional
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3.0"))
