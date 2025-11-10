from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models import PlayerCreate, PlayerUpdate, PlayerResponse
from app.repository import player_repository

router = APIRouter(prefix="/api/players", tags=["players"])


@router.post("/", response_model=PlayerResponse, status_code=201)
async def create_player(player: PlayerCreate):
    """
    Create a new player
    """
    created_player = await player_repository.create_player(player)
    return PlayerResponse(
        id=created_player.id,
        name=created_player.name,
        email=created_player.email,
        age=created_player.age,
        position=created_player.position,
        team=created_player.team,
        active=created_player.active,
        created_at=created_player.created_at,
        updated_at=created_player.updated_at
    )


@router.get("/", response_model=List[PlayerResponse])
async def get_all_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    Get all players with pagination
    """
    players = await player_repository.get_all_players(skip=skip, limit=limit)
    return [
        PlayerResponse(
            id=p.id,
            name=p.name,
            email=p.email,
            age=p.age,
            position=p.position,
            team=p.team,
            active=p.active,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in players
    ]


@router.get("/search", response_model=List[PlayerResponse])
async def search_players(q: str = Query(..., min_length=1)):
    """
    Search players by name, email, team, or position
    """
    players = await player_repository.search_players(q)
    return [
        PlayerResponse(
            id=p.id,
            name=p.name,
            email=p.email,
            age=p.age,
            position=p.position,
            team=p.team,
            active=p.active,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in players
    ]


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str):
    """
    Get a specific player by ID
    """
    player = await player_repository.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return PlayerResponse(
        id=player.id,
        name=player.name,
        email=player.email,
        age=player.age,
        position=player.position,
        team=player.team,
        active=player.active,
        created_at=player.created_at,
        updated_at=player.updated_at
    )


@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(player_id: str, player_update: PlayerUpdate):
    """
    Update a player
    """
    updated_player = await player_repository.update_player(player_id, player_update)
    if not updated_player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return PlayerResponse(
        id=updated_player.id,
        name=updated_player.name,
        email=updated_player.email,
        age=updated_player.age,
        position=updated_player.position,
        team=updated_player.team,
        active=updated_player.active,
        created_at=updated_player.created_at,
        updated_at=updated_player.updated_at
    )


@router.delete("/{player_id}", status_code=204)
async def delete_player(player_id: str):
    """
    Delete a player
    """
    deleted = await player_repository.delete_player(player_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Player not found")
    return None
