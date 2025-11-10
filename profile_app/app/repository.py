from tinydb import Query
from typing import Optional
from app.database import profiles_table
from app.models import Profile

class ProfileRepository:
    def __init__(self):
        self.table = profiles_table
        
    def create(self, profile: Profile):
        # Garante unicidade de user_id
        if self.table.search(Query().user_id == profile.user_id):
            raise ValueError("Profile already exists for this user_id")
        self.table.insert(profile.model_dump(mode='json'))
        return profile

    def get_by_user_id(self, user_id: str) -> Optional[dict]:
        res = self.table.search(Query().user_id == user_id)
        return res[0] if res else None

    def update(self, user_id: str, data: dict) -> Optional[dict]:
        if not self.get_by_user_id(user_id):
            return None
        self.table.update(data, Query().user_id == user_id)
        return self.get_by_user_id(user_id)

    def delete(self, user_id: str) -> bool:
        return bool(self.table.remove(Query().user_id == user_id))

    def list_all(self, q: Optional[str] = None, limit: int = 20, offset: int = 0):
        items = self.table.all()
        if q:
            q_lower = q.lower()
            items = [
                i for i in items
                if q_lower in i.get("display_name", "").lower()
                or q_lower in (i.get("bio") or "").lower()
                or q_lower in i.get("user_id", "").lower()
            ]
        total = len(items)
        paginated = items[offset:offset+limit]
        return {"items": paginated, "total": total}

    def add_favorite(self, user_id: str, field: str, item_id: str):
        doc = self.get_by_user_id(user_id)
        if not doc:
            return None
        if item_id not in doc[field]:
            doc[field].append(item_id)
        self.update(user_id, doc)
        return doc

    def remove_favorite(self, user_id: str, field: str, item_id: str):
        doc = self.get_by_user_id(user_id)
        if not doc:
            return None
        if item_id in doc[field]:
            doc[field].remove(item_id)
        self.update(user_id, doc)
        return doc
