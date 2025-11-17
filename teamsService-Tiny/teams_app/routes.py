import httpx
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone

from .models import TeamIn, TeamOut
from .repository import TeamsRepository
from .config import COMPETITIONS_BASE_URL

router = APIRouter()
repo = TeamsRepository()

VALID_SPORTS = [
    "futsal", "basquete", "volei",
    "handebol", "futebol", "rugby"
]

VALID_UNIVERSITIES = [
    "mackenzie", "unip", "puc", "ufabc", "usp", "fmu",
    "sao_judas", "uninove", "senac", "etec", "anhanguera"
]

async def fetch_competition(competition_id: str):
    async with httpx.AsyncClient(timeout=3.0) as client:
        r = await client.get(f"{COMPETITIONS_BASE_URL}/api/v1/competitions/{competition_id}")
        if r.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Competition '{competition_id}' not found"
            )
        return r.json()


@router.get("/", summary="Service info")
async def root():
    return {"service": "teamsService", "status": "ok"}


@router.post("/api/v1/teams", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamIn):

    # 1. Validar sport
    if team.sport not in VALID_SPORTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sport '{team.sport}'. Valid sports: {VALID_SPORTS}"
        )

    # 2. Validar universidade (opcional, melhora consistência)
    if team.university not in VALID_UNIVERSITIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid university '{team.university}'. Valid: {VALID_UNIVERSITIES}"
        )

    # 3. Validar competição
    competition = await fetch_competition(team.competitionId)

    # 4. Validar se o esporte do time combina com o esporte da competição
    if competition["sport"] != team.sport:
        raise HTTPException(
            status_code=400,
            detail=f"Team sport '{team.sport}' does not match competition sport '{competition['sport']}'"
        )

    # 5. Validar nome único dentro da universidade
    existing = repo.find_by_name_and_university(team.name, team.university)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A team with this name already exists for this university"
        )

    # 6. Criar documento
    doc = team.model_dump()
    doc["id"] = f"TEAM_{uuid4().hex[:8].upper()}"
    doc["createdAt"] = datetime.now(timezone.utc).isoformat()

    return repo.insert(doc)


@router.get("/api/v1/teams")
async def list_teams(
    university: Optional[str] = None,
    sport: Optional[str] = None,
    competitionId: Optional[str] = None,
    q: Optional[str] = Query(default=None, description="Search by name"),
    limit: int = 20,
    offset: int = 0,
):
    filters = {"university": university, "sport": sport, "competitionId": competitionId}
    res = repo.list(filters, q, limit, offset)
    return {
        "data": res["items"],
        "meta": {
            "total": res["total"],
            "limit": limit,
            "offset": offset,
            "hasMore": (offset + limit) < res["total"],
        },
    }


@router.get("/api/v1/teams/{team_id}", response_model=TeamOut)
async def get_team(team_id: str):
    doc = repo.get(team_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Team not found")
    return doc


@router.put("/api/v1/teams/{team_id}", response_model=TeamOut)
async def update_team(team_id: str, team: TeamIn):

    # → mesmas validações do create (boa prática)
    competition = await fetch_competition(team.competitionId)

    if competition["sport"] != team.sport:
        raise HTTPException(
            status_code=400,
            detail=f"Team sport '{team.sport}' does not match competition sport '{competition['sport']}'"
        )

    patch = team.model_dump()
    patch["id"] = team_id

    updated = repo.update(team_id, patch)
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")

    return updated


@router.delete("/api/v1/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: str):
    ok = repo.remove(team_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Team not found")
    return
