from dotenv import load_dotenv
import os
from typing import List

# 🔹 Carrega variáveis do .env
load_dotenv()

# 🌍 CORS — divide por vírgula se houver múltiplas origens
_CORS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")

# 📦 Caminho do banco TinyDB
_DB_PATH = os.getenv("DB_PATH", "data/players.json")

# 🧱 Nome do serviço
_SERVICE_NAME = os.getenv("SERVICE_NAME", "playersService - TinyDB")

# 🔗 Integrações futuras
_TEAMS_BASE_URL = os.getenv("TEAMS_BASE_URL", "http://localhost:8001")
_MATCHES_BASE_URL = os.getenv("MATCHES_BASE_URL", "http://localhost:8003")

# 🌐 Prefixo da API e porta
_API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
_PORT = int(os.getenv("PORT", 8005))


class Settings:
	"""Objeto de configuração usado pelo app.

	Expondo atributos em minúsculas (por exemplo, `port`, `database_name`) para
	compatibilidade com o restante do código que importa `settings`.
	"""

	def __init__(self):
		# valores simples
		self.cors_origins: List[str] = [s.strip() for s in _CORS.split(",") if s.strip()]
		self.db_path: str = _DB_PATH
		self.service_name: str = _SERVICE_NAME
		self.teams_base_url: str = _TEAMS_BASE_URL
		self.matches_base_url: str = _MATCHES_BASE_URL
		self.api_prefix: str = _API_PREFIX
		self.port: int = _PORT

		# Extrai o nome do banco (sem extensão) a partir de DB_PATH, para compatibilidade
		# com o código que usa `settings.database_name` e cria um arquivo em `./data`.
		base = os.path.basename(self.db_path)
		self.database_name: str = os.path.splitext(base)[0] if base else "players"


# Instância pública esperada pelo código: `from app.config import settings`
settings = Settings()

__all__ = ["settings"]
