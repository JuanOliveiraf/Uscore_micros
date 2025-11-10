from dotenv import load_dotenv
import os

# 🔹 Carrega as variáveis do .env
load_dotenv()

# 🌍 CORS — divide as origens por vírgula
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# 📦 Caminho do banco TinyDB
DB_PATH = os.getenv("DB_PATH", "data/match_details.json")

# 🧱 Nome do serviço
SERVICE_NAME = os.getenv("SERVICE_NAME", "matchDetailService - TinyDB")

# 🔗 Integrações com outros micros
MATCHES_BASE_URL = os.getenv("MATCHES_BASE_URL", "http://localhost:8003")
TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
COMPETITIONS_BASE_URL = os.getenv("COMPETITIONS_BASE_URL", "http://localhost:8002")
PLAYERS_BASE_URL = os.getenv("PLAYERS_BASE_URL", "http://localhost:8005")

# ⚙️ Timeout padrão para requisições HTTP
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3.0"))

# 🌐 Prefixo base e porta padrão
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PORT = int(os.getenv("PORT", 8004))
