
from pydantic import BaseModel
from typing import Optional, List, Dict, Literal
from datetime import datetime

Status = Literal["SCHEDULED", "LIVE", "FINISHED"]

class Venue(BaseModel):
    name: str
    city: Optional[str] = None

class MatchMeta(BaseModel):
    id: str
    competitionId: Optional[str] = None
    status: Status = "SCHEDULED"
    minute: Optional[int] = None
    scheduledAt: Optional[datetime] = None
    venue: Optional[Venue] = None
    sport: Optional[str] = None
    homeTeamId: Optional[str] = None
    awayTeamId: Optional[str] = None

class TeamInfo(BaseModel):
    id: str
    name: Optional[str] = None
    colors: Optional[List[str]] = None
    logoUrl: Optional[str] = None
    university: Optional[str] = None

class Event(BaseModel):
    id: str
    minute: int
    type: str
    playerId: Optional[str] = None
    teamId: Optional[str] = None
    meta: Dict[str, str] = {}

class LineupItem(BaseModel):
    playerId: str
    name: Optional[str] = None
    position: Optional[str] = None
    number: Optional[int] = None

class Lineups(BaseModel):
    home: List[LineupItem] = []
    away: List[LineupItem] = []

class TeamStats(BaseModel):
    score: int = 0
    shots: Optional[int] = None
    fouls: Optional[int] = None
    possession: Optional[int] = None

class PlayerStat(BaseModel):
    playerId: str
    minutes: Optional[int] = None
    points: Optional[int] = None
    goals: Optional[int] = None
    cardsYellow: Optional[int] = None
    cardsRed: Optional[int] = None

class Stats(BaseModel):
    home: TeamStats = TeamStats()
    away: TeamStats = TeamStats()
    players: List[PlayerStat] = []

class MatchDetailOut(BaseModel):
    match: MatchMeta
    homeTeam: Optional[TeamInfo] = None
    awayTeam: Optional[TeamInfo] = None
    competition: Optional[Dict] = None
    events: List[Event] = []
    lineups: Lineups = Lineups()
    stats: Stats = Stats()
