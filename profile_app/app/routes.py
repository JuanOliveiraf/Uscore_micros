from fastapi import APIRouter, HTTPException, status
from typing import Optional
import httpx

from app.models import Profile
from app.repository import ProfileRepository
from app.config import TEAMS_BASE_URL, COMPETITIONS_BASE_URL, REQUEST_TIMEOUT

router = APIRouter()
repo = ProfileRepository()


@router.get("/")
async def root():
    return {"service": "profileService", "status": "ok"}


async def _check_team_exists(team_id: str):
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        r = await client.get(f"{TEAMS_BASE_URL}/api/v1/teams/{team_id}")
    if r.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Favorite team '{team_id}' not found"
        )


async def _check_competition_exists(competition_id: str):
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        r = await client.get(f"{COMPETITIONS_BASE_URL}/api/v1/competitions/{competition_id}")
    if r.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Favorite competition '{competition_id}' not found"
        )


async def _validate_profile_references(profile: Profile):
    try:
        for team_id in profile.favorite_teams:
            await _check_team_exists(team_id)

        for comp_id in profile.favorite_competitions:
            await _check_competition_exists(comp_id)
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Dependency service unavailable (teamsService or competitionsService)"
        )


@router.post("/api/profiles/", status_code=status.HTTP_201_CREATED)
async def create_profile(profile: Profile):
    # valida favoritos chamando outros micros
    await _validate_profile_references(profile)

    try:
        return repo.create(profile)
    except ValueError as e:
        # ex: profile com user_id já existe
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/api/profiles/{user_id}")
async def get_profile(user_id: str):
    doc = repo.get_by_user_id(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


@router.put("/api/profiles/{user_id}")
async def update_profile(user_id: str, profile: Profile):
    if user_id != profile.user_id:
        raise HTTPException(status_code=400, detail="user_id mismatch")

    await _validate_profile_references(profile)

    updated = repo.update(user_id, profile.model_dump(mode="json"))
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated


@router.get("/api/profiles/{user_id}/favorites")
async def list_favorites(user_id: str):
    doc = repo.get_by_user_id(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "favorite_teams_id": doc.get("favorite_teams", []),
        "favorite_competitions_id": doc.get("favorite_competitions", []),
    }


@router.post("/api/profiles/{user_id}/favorites/teams/{team_id}")
async def add_fav_team(user_id: str, team_id: str):
    await _check_team_exists(team_id)
    doc = repo.add_favorite(user_id, "favorite_teams", team_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


@router.delete("/api/profiles/{user_id}/favorites/teams/{team_id}")
async def remove_fav_team(user_id: str, team_id: str):
    doc = repo.remove_favorite(user_id, "favorite_teams", team_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


@router.post("/api/profiles/{user_id}/favorites/competitions/{competition_id}")
async def add_fav_comp(user_id: str, competition_id: str):
    await _check_competition_exists(competition_id)
    doc = repo.add_favorite(user_id, "favorite_competitions", competition_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


@router.delete("/api/profiles/{user_id}/favorites/competitions/{competition_id}")
async def remove_fav_comp(user_id: str, competition_id: str):
    doc = repo.remove_favorite(user_id, "favorite_competitions", competition_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc
