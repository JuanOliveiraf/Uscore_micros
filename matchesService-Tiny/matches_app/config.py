from dotenv import load_dotenv
import os

# 🔹 Carrega variáveis do .env
load_dotenv()

# 🌍 CORS — divide por vírgula se tiver múltiplas origens
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# 📦 Caminho do banco TinyDB
DB_PATH = os.getenv("DB_PATH", "data/matches.json")

# 🧱 Nome do serviço
SERVICE_NAME = os.getenv("SERVICE_NAME", "matchesService - TinyDB")

# 🔗 Integrações com outros micros
TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
COMPETITIONS_BASE_URL = os.getenv("COMPETITIONS_BASE_URL", "http://localhost:8002")

# 🌐 Prefixo base e porta
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
PORT = int(os.getenv("PORT", 8003))
