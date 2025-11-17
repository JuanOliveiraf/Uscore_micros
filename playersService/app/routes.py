from fastapi import APIRouter, HTTPException, Query
from typing import List
import httpx

from app.models import PlayerCreate, PlayerUpdate, PlayerResponse
from app.repository import player_repository
from app.config import TEAMS_BASE_URL, REQUEST_TIMEOUT

router = APIRouter(prefix="/api/v1/players", tags=["players"])


# ----------------------------------------------------------
# 🧩 Validação externa: verifica se o time existe
# ----------------------------------------------------------
async def validate_team_exists(team_id: str):
    if not team_id:
        return

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        r = await client.get(f"{TEAMS_BASE_URL}/api/v1/teams/{team_id}")

    if r.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Team '{team_id}' does not exist in teamsService."
        )


# ----------------------------------------------------------
# POST: criar jogador
# ----------------------------------------------------------
@router.post("/", response_model=PlayerResponse, status_code=201)
async def create_player(player: PlayerCreate):
    await validate_team_exists(player.team)

    created = await player_repository.create_player(player)
    return PlayerResponse(**created.model_dump())


# ----------------------------------------------------------
# GET: listar jogadores
# ----------------------------------------------------------
@router.get("/", response_model=List[PlayerResponse])
async def get_all_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    players = await player_repository.get_all_players(skip=skip, limit=limit)
    return [PlayerResponse(**p.model_dump()) for p in players]


# ----------------------------------------------------------
# GET: buscar por texto
# ----------------------------------------------------------
@router.get("/search", response_model=List[PlayerResponse])
async def search_players(q: str = Query(..., min_length=1)):
    players = await player_repository.search_players(q)
    return [PlayerResponse(**p.model_dump()) for p in players]


# ----------------------------------------------------------
# GET: obter um jogador
# ----------------------------------------------------------
@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str):
    player = await player_repository.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerResponse(**player.model_dump())


# ----------------------------------------------------------
# PUT: atualizar jogador
# ----------------------------------------------------------
@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(player_id: str, player_update: PlayerUpdate):

    if player_update.team:
        await validate_team_exists(player_update.team)

    updated = await player_repository.update_player(player_id, player_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Player not found")

    return PlayerResponse(**updated.model_dump())


# ----------------------------------------------------------
# DELETE: remover jogador
# ----------------------------------------------------------
@router.delete("/{player_id}", status_code=204)
async def delete_player(player_id: str):
    deleted = await player_repository.delete_player(player_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Player not found")
    return None
