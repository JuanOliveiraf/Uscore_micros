from tinydb import TinyDB
from app.config import DB_PATH

db = TinyDB(DB_PATH)
profiles_table = db.table("profiles")
