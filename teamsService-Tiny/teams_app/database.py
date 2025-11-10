from tinydb import TinyDB
from .config import DB_PATH

db = TinyDB(DB_PATH)
teams_table = db.table("teams")
