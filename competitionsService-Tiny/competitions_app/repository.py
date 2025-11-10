import json
from tinydb import Query
from typing import Dict, Any, Optional
from .database import competitions_table

class CompetitionsRepository:
    def __init__(self):
        self.table = competitions_table

    def insert(self, doc: Dict[str, Any]):
        serializable = json.loads(json.dumps(doc, default=str))
        self.table.insert(serializable)
        return serializable

    def get(self, comp_id: str) -> Optional[Dict[str, Any]]:
        res = self.table.search(Query().id == comp_id)
        return res[0] if res else None

    def update(self, comp_id: str, patch: Dict[str, Any]):
        if not self.get(comp_id):
            return None
        serializable_patch = json.loads(json.dumps(patch, default=str))
        self.table.update(serializable_patch, Query().id == comp_id)
        return self.get(comp_id)

    def remove(self, comp_id: str) -> bool:
        return bool(self.table.remove(Query().id == comp_id))

    def list(self, q: Optional[str], sport: Optional[str], limit: int, offset: int):
        items = self.table.all()

        def matches(it: Dict[str, Any]):
            if q and q.lower() not in it.get("name", "").lower():
                return False
            if sport and it.get("sport") != sport:
                return False
            return True

        items = [it for it in items if matches(it)]
        total = len(items)
        return {"items": items[offset:offset + limit], "total": total}
