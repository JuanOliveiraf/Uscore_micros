from fastapi import APIRouter, HTTPException, Query, status
from uuid import uuid4
from datetime import datetime, timezone
from typing import Optional
from .models import CompetitionIn, CompetitionOut
from .repository import CompetitionsRepository

router = APIRouter()
repo = CompetitionsRepository()

@router.get("/", summary="Service info")
def root():
    return {"service": "competitionsService", "status": "ok"}

@router.post("/api/v1/competitions", response_model=CompetitionOut, status_code=status.HTTP_201_CREATED)
async def create_competition(comp: CompetitionIn):
    doc = comp.model_dump()
    doc["id"] = f"COMP_{uuid4().hex[:8].upper()}"
    doc["createdAt"] = datetime.now(timezone.utc).isoformat()
    return repo.insert(doc)

@router.get("/api/v1/competitions", summary="List competitions")
async def list_competitions(
    q: Optional[str] = Query(default=None, description="Search by name"),
    sport: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    res = repo.list(q, sport, limit, offset)
    return {
        "data": res["items"],
        "meta": {"total": res["total"], "limit": limit, "offset": offset, "hasMore": (offset + limit) < res["total"]}
    }

@router.get("/api/v1/competitions/{comp_id}", response_model=CompetitionOut)
async def get_competition(comp_id: str):
    doc = repo.get(comp_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Competition not found")
    return doc

@router.put("/api/v1/competitions/{comp_id}", response_model=CompetitionOut)
async def update_competition(comp_id: str, comp: CompetitionIn):
    patch = comp.model_dump()
    updated = repo.update(comp_id, {**patch, "id": comp_id})
    if not updated:
        raise HTTPException(status_code=404, detail="Competition not found")
    return updated

@router.delete("/api/v1/competitions/{comp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competition(comp_id: str):
    ok = repo.remove(comp_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Competition not found")
    return
