import json
from typing import List, Dict, Any
from tinydb import Query

from .database import events_table

class EventsRepository:
    def __init__(self):
        self._table = events_table

    def _serialize(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        return json.loads(json.dumps(doc, default=str, ensure_ascii=False))

    def insert(self, event: Dict[str, Any]) -> Dict[str, Any]:
        serialized = self._serialize(event)
        self._table.insert(serialized)
        return serialized

    def list_by_match(self, match_id: str) -> List[Dict[str, Any]]:
        results = self._table.search(Query().matchId == match_id)
        return [self._serialize(doc) for doc in results]

repo = EventsRepository()
