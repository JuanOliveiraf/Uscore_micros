from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

Status = Literal['SCHEDULED', 'LIVE', 'FINISHED']

class Venue(BaseModel):
    name: str
    city: Optional[str] = None

class Score(BaseModel):
    home: int = 0
    away: int = 0

class MatchIn(BaseModel):
    competitionId: str
    homeTeamId: str
    awayTeamId: str
    sport: str
    scheduledAt: datetime
    status: Status = "SCHEDULED"
    venue: Venue
    score: Optional[Score] = Score()

class MatchOut(MatchIn):
    id: str
    createdAt: datetime
