from pydantic import BaseModel, HttpUrl, constr, Field
from typing import Optional, List

class TeamIn(BaseModel):
    id: str = Field(..., description="Unique team ID")
    name: str
    university: str
    sport: str
    competitionId: Optional[str] = None
    colors: List[str] = []
    logoUrl: Optional[str] = None
    createdAt: Optional[str] = None


class TeamOut(TeamIn):
    id: str
    createdAt: str
