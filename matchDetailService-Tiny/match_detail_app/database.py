
from tinydb import TinyDB
from .config import DB_PATH

db = TinyDB(DB_PATH)
details_table = db.table("details")
events_table = db.table("events")
lineups_table = db.table("lineups")
stats_table = db.table("stats")
