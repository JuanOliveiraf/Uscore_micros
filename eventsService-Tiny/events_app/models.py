from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class EventBase(BaseModel):
    type: str = Field(..., description="Tipo do evento (goal, foul, card, etc.)")
    teamId: Optional[str] = Field(None, description="ID do time relacionado")
    playerId: Optional[str] = Field(None, description="ID do jogador relacionado")
    minute: Optional[int] = Field(None, ge=0)
    period: Optional[int] = Field(None, ge=0)
    value: Optional[int] = Field(None, description="Valor numérico associado ao evento")
    meta: Optional[Dict[str, Any]] = Field(default_factory=dict)

class EventCreate(EventBase):
    pass

class EventOut(EventBase):
    id: str
    matchId: str
    createdAt: datetime
