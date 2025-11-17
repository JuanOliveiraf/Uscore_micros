import httpx
from fastapi import APIRouter, HTTPException, Query, status
from uuid import uuid4
from datetime import datetime, timezone
from typing import Optional

from .models import CompetitionIn, CompetitionOut
from .repository import CompetitionsRepository
from .config import TEAMS_BASE_URL

router = APIRouter()
repo = CompetitionsRepository()

VALID_SPORTS = ["futsal", "basquete", "volei", "handebol", "futebol"]


async def check_team_exists(team_id: str):
    async with httpx.AsyncClient(timeout=3.0) as client:
        r = await client.get(f"{TEAMS_BASE_URL}/api/v1/teams/{team_id}")
    if r.status_code != 200:
        raise HTTPException(400, f"Team '{team_id}' not found")


@router.post("/api/v1/competitions", response_model=CompetitionOut, status_code=status.HTTP_201_CREATED)
async def create_competition(comp: CompetitionIn):

    # --- 1) Validar modalidade ---
    if comp.sport not in VALID_SPORTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sport '{comp.sport}'. Valid options: {VALID_SPORTS}"
        )

    # --- 2) Validar times participantes (se quiser usar futuramente) ---
    # if hasattr(comp, "teams"):
    #     for team in comp.teams:
    #         await check_team_exists(team)

    # --- 3) Criar competição ---
    doc = comp.model_dump()
    doc["id"] = f"COMP_{uuid4().hex[:8].upper()}"
    doc["createdAt"] = datetime.now(timezone.utc).isoformat()

    return repo.insert(doc)

@router.get("/api/v1/competitions/{comp_id}", response_model=CompetitionOut)
async def get_competition(comp_id: str):
    comp = repo.get(comp_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Competition not found")
    return comp
@router.get("/api/v1/competitions", response_model=list[CompetitionOut])
async def list_competitions(sport: Optional[str] = Query(None, description="Filter by sport")):
    if sport and sport not in VALID_SPORTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sport '{sport}'. Valid options: {VALID_SPORTS}"
        )
    return repo.list(sport=sport)