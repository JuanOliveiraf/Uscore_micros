from tinydb import TinyDB
db = TinyDB("data/competitions.json")
competitions_table = db.table("competitions")
