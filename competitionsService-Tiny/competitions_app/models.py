from pydantic import BaseModel
from typing import Optional

class CompetitionIn(BaseModel):
    name: str
    sport: str
    season: Optional[str] = None
    university_scope: Optional[str] = None
    description: Optional[str] = None

class CompetitionOut(CompetitionIn):
    id: str
    createdAt: str
