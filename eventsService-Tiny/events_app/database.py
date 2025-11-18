from tinydb import TinyDB
from .config import DB_PATH

db = TinyDB(DB_PATH)
events_table = db.table("events")
