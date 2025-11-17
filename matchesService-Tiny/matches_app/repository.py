from tinydb import Query
from datetime import datetime, timezone, date
import json
from .database import matches_table

class MatchesRepository:
    def __init__(self):
        # use a private attribute for the underlying table
        self._table = matches_table

    def _serialize(self, doc):
        """Prepare a document for storage/return (convert datetimes, etc.)."""
        return json.loads(json.dumps(doc, default=str, ensure_ascii=False))

    def insert(self, match):
        serialized = self._serialize(match)
        self._table.insert(serialized)
        return serialized

    def get_by_id(self, match_id):
        results = self._table.search(Query().id == match_id)
        return results[0] if results else None

    # backward-compatible alias
    def get(self, id):
        return self.get_by_id(id)

    def update_by_id(self, match_id, patch):
        if not self.get_by_id(match_id):
            return None
        serialized = self._serialize(patch)
        self._table.update(serialized, Query().id == match_id)
        return self.get_by_id(match_id)

    # backward-compatible alias
    def update(self, id, patch):
        return self.update_by_id(id, patch)

    def delete_by_id(self, match_id):
        return bool(self._table.remove(Query().id == match_id))

    # backward-compatible alias
    def remove(self, id):
        return self.delete_by_id(id)

    def list_matches(self, filters=None, limit=100, offset=0, **kwargs):
        """Return a paginated list of matches applying simple filters.

        Supports two calling styles:
        - list_matches(filters={...}, limit=.., offset=..)
        - list_matches(competitionId=..., teamId=..., status=..., sport=..., upcoming=True, limit=.., offset=..)
        Route currently invokes: repo.list(competitionId=..., teamId=..., limit=..., offset=...)
        """
        filters = (filters or {}).copy()
        # Merge direct keyword filters (backward compatibility with current router usage)
        for key in ["status", "sport", "competitionId", "teamId", "upcoming"]:
            if key in kwargs and kwargs[key] is not None:
                filters[key] = kwargs[key]
        all_items = self._table.all()

        def _parse_datetime(dt):
            try:
                if isinstance(dt, str) and dt.endswith('Z'):
                    dt = dt.replace('Z', '+00:00')
                return datetime.fromisoformat(dt)
            except Exception:
                return None

        def _filter_match(item):
            # status filter
            if filters.get('status') and item.get('status') != filters['status']:
                return False
            # sport filter
            if filters.get('sport') and item.get('sport') != filters['sport']:
                return False
            # competition filter (note: underlying data keys kept as-is)
            if filters.get('competitionId') and item.get('competitionId') != filters['competitionId']:
                return False
            # team filter: either home or away
            if filters.get('teamId') and item.get('homeTeamId') != filters['teamId'] and item.get('awayTeamId') != filters['teamId']:
                return False
            # upcoming filter uses scheduledAt
            dt = _parse_datetime(item.get('scheduledAt'))
            if filters.get('upcoming'):
                now = datetime.now(timezone.utc)
                if not dt or not (item.get('status') == 'SCHEDULED' and dt >= now):
                    return False
            return True

        filtered_items = [i for i in all_items if _filter_match(i)]
        total = len(filtered_items)
        return {'items': filtered_items[offset:offset+limit], 'total': total}

    # backward-compatible alias (routes call repo.list(...))
    list = list_matches
