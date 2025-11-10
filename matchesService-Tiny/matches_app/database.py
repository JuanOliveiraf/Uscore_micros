from tinydb import TinyDB
from .config import DB_PATH
db=TinyDB(DB_PATH)
matches_table=db.table('matches')
