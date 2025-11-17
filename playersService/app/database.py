from tinydb import TinyDB
from .config import DB_PATH

# TinyDB database (single-file storage)
db = TinyDB(DB_PATH)


def get_database():
    """Return the TinyDB database instance (compat API)."""
    return db


# No-op async functions to keep compatibility with app.main lifecycle
async def connect_to_mongo():
    """Compatibility stub for startup; TinyDB requires no connection."""
    return None


async def close_mongo_connection():
    """Compatibility stub for shutdown; TinyDB requires no teardown."""
    return None
