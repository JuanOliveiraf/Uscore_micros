from fastapi import APIRouter, HTTPException, status
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone

import httpx

from .models import MatchIn, MatchOut
from .repository import MatchesRepository
from .config import TEAMS_BASE_URL, COMPETITIONS_BASE_URL, REQUEST_TIMEOUT

router = APIRouter()
repo = MatchesRepository()


@router.get("/", summary="Service info")
async def root():
    return {"service": "matchesService", "status": "ok"}


async def _check_team_exists(team_id: str):
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        r = await client.get(f"{TEAMS_BASE_URL}/api/v1/teams/{team_id}")
    if r.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Team '{team_id}' not found in teamsService"
        )


async def _check_competition_exists(competition_id: str):
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        r = await client.get(f"{COMPETITIONS_BASE_URL}/api/v1/competitions/{competition_id}")
    if r.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Competition '{competition_id}' not found in competitionsService"
        )


@router.post("/api/v1/matches", response_model=MatchOut, status_code=status.HTTP_201_CREATED)
async def create_match(match: MatchIn):
    # 1) valida se times e competição existem em outros micros
    try:
        await _check_team_exists(match.homeTeamId)
        await _check_team_exists(match.awayTeamId)
        await _check_competition_exists(match.competitionId)
    except httpx.RequestError:
        # algum micro está offline
        raise HTTPException(
            status_code=503,
            detail="Dependency service unavailable (teamsService or competitionsService)"
        )

    # 2) gera doc e salva no TinyDB
    doc = match.model_dump()
    doc["id"] = f"MATCH_{uuid4().hex[:8].upper()}"
    doc["createdAt"] = datetime.now(timezone.utc).isoformat()
    return repo.insert(doc)

@router.get("/api/v1/matches/{match_id}", response_model=MatchOut, summary="Get a match by ID")
async def get_match(match_id: str):
    match = repo.get_by_id(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/api/v1/matches", summary="List matches")
async def list_matches(
    competitionId: Optional[str] = None,
    teamId: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    res = repo.list(competitionId=competitionId, teamId=teamId, limit=limit, offset=offset)
    return {
        "data": res["items"],
        "meta": {
            "total": res["total"],
            "limit": limit,
            "offset": offset,
            "hasMore": (offset + limit) < res["total"],
        },
    }
