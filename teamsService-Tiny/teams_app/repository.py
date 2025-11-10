from typing import Optional, Dict, Any
import json
from tinydb import Query
from .database import teams_table

class TeamsRepository:
    def __init__(self):
        self.table = teams_table

    def insert(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        # TinyDB uses json.dumps under the hood which fails on non-serializable
        # types (e.g. pydantic Url objects, datetimes). Convert the document to
        # a JSON-serializable structure by round-tripping through json with
        # default=str so those objects become strings.
        serializable = json.loads(json.dumps(doc, default=str, ensure_ascii=False))
        self.table.insert(serializable)
        return serializable

    def get(self, team_id: str) -> Optional[Dict[str, Any]]:
        res = self.table.search(Query().id == team_id)
        return res[0] if res else None

    def update(self, team_id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.get(team_id):
            return None
        # Ensure patch is JSON-serializable (same reason as in insert)
        serializable_patch = json.loads(json.dumps(patch, default=str, ensure_ascii=False))
        self.table.update(serializable_patch, Query().id == team_id)
        return self.get(team_id)

    def remove(self, team_id: str) -> bool:
        return bool(self.table.remove(Query().id == team_id))

    def list(self, filters: Dict[str, Any], q: Optional[str], limit: int, offset: int):
        items = self.table.all()

        def matches(it: Dict[str, Any]) -> bool:
            if filters.get("university") and (it.get("university") != filters["university"]):
                return False
            if filters.get("sport") and (it.get("sport") != filters["sport"]):
                return False
            if filters.get("competitionId") and (it.get("competitionId") != filters["competitionId"]):
                return False
            if q and (q.lower() not in it.get("name", "").lower()):
                return False
            return True

        items = [it for it in items if matches(it)]
        total = len(items)
        items = items[offset: offset + limit]
        return {"items": items, "total": total}
