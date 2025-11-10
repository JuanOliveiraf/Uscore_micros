
from fastapi import APIRouter, HTTPException
from .models import MatchDetailOut
from .repository import DetailRepository
router = APIRouter()
repo = DetailRepository()
@router.get("/")
def root(): return {"service":"matchDetailService","status":"ok"}
@router.get("/api/v1/match-details/{match_id}", response_model=MatchDetailOut)
async def get_detail(match_id:str):
    d = await repo.get_detail(match_id)
    if not d.get("match"): raise HTTPException(404,"Match not found")
    return d
