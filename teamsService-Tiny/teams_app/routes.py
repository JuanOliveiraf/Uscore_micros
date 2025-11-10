from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone

from .models import TeamIn, TeamOut
from .repository import TeamsRepository

router = APIRouter()
repo = TeamsRepository()

@router.get("/", summary="Service info")
def root():
    return {"service": "teamsService", "status": "ok"}

@router.post("/api/v1/teams", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamIn):
    doc = team.model_dump()
    doc["id"] = f"TEAM_{uuid4().hex[:8].upper()}"
    doc["createdAt"] = datetime.now(timezone.utc).isoformat()
    return repo.insert(doc)

@router.get("/api/v1/teams", summary="List teams with filters")
async def list_teams(
    university: Optional[str] = None,
    sport: Optional[str] = None,
    competitionId: Optional[str] = None,
    q: Optional[str] = Query(default=None, description="Search by name"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    filters = {"university": university, "sport": sport, "competitionId": competitionId}
    res = repo.list(filters, q, limit, offset)
    return {
        "data": res["items"],
        "meta": {"total": res["total"], "limit": limit, "offset": offset, "hasMore": (offset + limit) < res["total"]}
    }

@router.get("/api/v1/teams/{team_id}", response_model=TeamOut)
async def get_team(team_id: str):
    doc = repo.get(team_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Team not found")
    return doc

@router.put("/api/v1/teams/{team_id}", response_model=TeamOut)
async def update_team(team_id: str, team: TeamIn):
    patch = team.model_dump()
    updated = repo.update(team_id, {**patch, "id": team_id})
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated

@router.delete("/api/v1/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: str):
    ok = repo.remove(team_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Team not found")
    return
