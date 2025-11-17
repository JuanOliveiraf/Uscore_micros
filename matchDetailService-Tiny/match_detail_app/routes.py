from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Set

from .config import (
    MATCHES_BASE_URL,
    TEAMS_BASE_URL,
    COMPETITIONS_BASE_URL,
    PLAYERS_BASE_URL,
    REQUEST_TIMEOUT,
)
from .repository import MatchDetailRepository
from .models import MatchDetailOut, MatchMeta, Event, Lineups, Stats

router = APIRouter()
repo = MatchDetailRepository()

# In-memory websocket subscribers per match
_SUBSCRIBERS: Dict[str, Set[WebSocket]] = {}

async def _broadcast(match_id: str, message: Dict):
    conns = list(_SUBSCRIBERS.get(match_id, set()))
    for ws in conns:
        try:
            await ws.send_json(message)
        except Exception:
            try:
                await ws.close()
            except Exception:
                pass
            _SUBSCRIBERS.get(match_id, set()).discard(ws)


@router.get("/", summary="Service info")
async def root():
    return {"service": "matchDetailService", "status": "ok"}


# removed old _fetch_json helper; repository now aggregates data


@router.get("/api/v1/match-details/{match_id}", response_model=MatchDetailOut, summary="Get Match Details")
async def get_match_details_v2(match_id: str):
    return await repo.get_detail(match_id)

# Backward compatibility route
@router.get("/api/v1/matches/{match_id}/details", response_model=MatchDetailOut)
async def get_match_details_legacy(match_id: str):
    return await repo.get_detail(match_id)


# --- Write endpoints (optional, used by control panels or admins) ---
@router.patch("/api/v1/match-details/{match_id}/meta", summary="Upsert match meta")
async def upsert_meta(match_id: str, meta: MatchMeta):
    repo.upsert_meta(meta.model_dump())
    await _broadcast(match_id, {"type": "match.updated", "payload": meta.model_dump()})
    return {"ok": True}

@router.post("/api/v1/match-details/{match_id}/events", summary="Append event")
async def create_event(match_id: str, ev: Event):
    created = repo.add_event(match_id, ev.model_dump())
    await _broadcast(match_id, {"type": "event.created", "payload": created})
    return created

@router.put("/api/v1/match-details/{match_id}/lineups", summary="Replace lineups")
async def put_lineups(match_id: str, lineups: Lineups):
    saved = repo.set_lineups(match_id, lineups.model_dump())
    await _broadcast(match_id, {"type": "lineups.updated", "payload": saved})
    return saved

@router.put("/api/v1/match-details/{match_id}/stats", summary="Replace stats")
async def put_stats(match_id: str, stats: Stats):
    saved = repo.set_stats(match_id, stats.model_dump())
    await _broadcast(match_id, {"type": "stats.updated", "payload": saved})
    return saved


# --- WebSocket for live updates ---
@router.websocket("/ws/matches/{match_id}")
async def ws_match_updates(websocket: WebSocket, match_id: str):
    await websocket.accept()
    _SUBSCRIBERS.setdefault(match_id, set()).add(websocket)
    try:
        # On connect, send a hello and current snapshot
        await websocket.send_json({"type": "connected", "payload": {"matchId": match_id}})
        snapshot = await repo.get_detail(match_id)
        await websocket.send_json({"type": "snapshot", "payload": snapshot})
        # Keep connection alive; client may send pings we ignore
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        _SUBSCRIBERS.get(match_id, set()).discard(websocket)
