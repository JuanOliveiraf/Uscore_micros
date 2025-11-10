from tinydb import TinyDB, Query
from app.config import settings
import os

db = None


async def connect_to_mongo():
    global db
    # TinyDB armazena dados em um arquivo local
    db_path = "./data"
    
    # Criar diretório se não existir
    os.makedirs(db_path, exist_ok=True)
    
    # Inicializar banco de dados
    db_file = os.path.join(db_path, f"{settings.database_name}.json")
    db = TinyDB(db_file, indent=2, ensure_ascii=False)
    
    print(f"Connected to TinyDB database at {db_file}")


async def close_mongo_connection():
    global db
    if db:
        db.close()
        print("Closed TinyDB connection")


def get_database():
    """Retorna o banco de dados TinyDB"""
    return db
