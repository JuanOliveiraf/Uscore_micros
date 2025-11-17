from typing import List, Optional
from datetime import datetime
from tinydb import Query
from app.database import get_database
from app.models import PlayerCreate, PlayerUpdate, PlayerInDB
import re


class PlayerRepository:
    def __init__(self):
        self.table_name = "players"

    def get_table(self):
        db = get_database()
        return db.table(self.table_name)

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    async def create_player(self, player: PlayerCreate) -> PlayerInDB:
        table = self.get_table()
        now = datetime.utcnow().isoformat()

        data = player.model_dump()
        data["created_at"] = now
        data["updated_at"] = now

        # Insert → TinyDB generates numeric doc_id
        doc_id = table.insert(data)

        created = table.get(doc_id=doc_id)
        created["id"] = str(doc_id)

        return PlayerInDB(**created)

    # ----------------------------------------------------------
    # GET by ID
    # ----------------------------------------------------------
    async def get_player(self, player_id: str) -> Optional[PlayerInDB]:
        table = self.get_table()

        try:
            doc_id = int(player_id)
        except ValueError:
            return None

        doc = table.get(doc_id=doc_id)
        if not doc:
            return None

        doc["id"] = str(doc_id)
        return PlayerInDB(**doc)

    # ----------------------------------------------------------
    # LIST with pagination
    # ----------------------------------------------------------
    async def get_all_players(self, skip: int = 0, limit: int = 50) -> List[PlayerInDB]:
        table = self.get_table()
        docs = table.all()

        sliced = docs[skip: skip + limit]

        players = []
        for d in sliced:
            d["id"] = str(d.doc_id)
            players.append(PlayerInDB(**d))

        return players

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------
    async def update_player(self, player_id: str, updates: PlayerUpdate) -> Optional[PlayerInDB]:
        table = self.get_table()

        try:
            doc_id = int(player_id)
        except ValueError:
            return None

        if not table.get(doc_id=doc_id):
            return None

        update_data = updates.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()

        table.update(update_data, doc_ids=[doc_id])

        updated = table.get(doc_id=doc_id)
        updated["id"] = str(doc_id)

        return PlayerInDB(**updated)

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------
    async def delete_player(self, player_id: str) -> bool:
        table = self.get_table()

        try:
            doc_id = int(player_id)
        except ValueError:
            return False

        removed = table.remove(doc_ids=[doc_id])
        return len(removed) > 0

    # ----------------------------------------------------------
    # SEARCH
    # ----------------------------------------------------------
    async def search_players(self, query: str) -> List[PlayerInDB]:
        table = self.get_table()
        docs = table.all()
        pattern = re.compile(query, re.IGNORECASE)

        results = []

        for d in docs:
            if (
                pattern.search(d.get("name", "")) or
                pattern.search(d.get("email", "")) or
                pattern.search(d.get("team", "")) or
                pattern.search(d.get("position", ""))
            ):
                d["id"] = str(d.doc_id)
                results.append(PlayerInDB(**d))

        return results


# instance used in routes
player_repository = PlayerRepository()
