import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from typing import Dict

from .config import settings
from .repository import MatchDetailRepository
from .models import MatchDetailOut, MatchMeta, Event, Lineups, Stats
from .auth import require_auth
from .realtime import ChannelManager, RedisBroadcaster, WSClient, SSEClient

router = APIRouter()
repo = MatchDetailRepository()
manager = ChannelManager()
broadcaster = RedisBroadcaster(settings.redis_url)


async def _broadcast(message: Dict):
    message.setdefault("matchId", message.get("payload", {}).get("matchId"))
    await manager.broadcast(message)
    await broadcaster.publish(message)


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
@router.patch(
    "/api/v1/match-details/{match_id}/meta",
    response_model=MatchMeta,
    dependencies=[Depends(require_auth)],
)
async def upsert_meta(match_id: str, meta: MatchMeta):
    repo.upsert_meta(meta.model_dump())
    payload = meta.model_dump()
    payload["matchId"] = match_id
    await _broadcast({"type": "match.updated", "matchId": match_id, "payload": payload})
    return payload

@router.post(
    "/api/v1/match-details/{match_id}/events",
    status_code=201,
    response_model=Event,
    dependencies=[Depends(require_auth)],
)
async def create_event(match_id: str, ev: Event):
    created = repo.add_event(match_id, ev.model_dump())
    await _broadcast({"type": "event.created", "matchId": match_id, "payload": created})
    return created

@router.put(
    "/api/v1/match-details/{match_id}/lineups",
    response_model=Lineups,
    dependencies=[Depends(require_auth)],
)
async def put_lineups(match_id: str, lineups: Lineups):
    saved = repo.set_lineups(match_id, lineups.model_dump())
    await _broadcast({"type": "lineups.updated", "matchId": match_id, "payload": saved})
    return saved

@router.put(
    "/api/v1/match-details/{match_id}/stats",
    response_model=Stats,
    dependencies=[Depends(require_auth)],
)
async def put_stats(match_id: str, stats: Stats):
    saved = repo.set_stats(match_id, stats.model_dump())
    await _broadcast({"type": "stats.updated", "matchId": match_id, "payload": saved})
    return saved


# --- WebSocket for live updates ---
@router.websocket("/ws/matches/{match_id}")
async def ws_match_updates(websocket: WebSocket, match_id: str):
    await websocket.accept()
    client = WSClient(websocket=websocket, match_id=match_id)
    await manager.register_ws(client)
    snapshot = await repo.get_detail(match_id)
    await websocket.send_text(json.dumps({"type": "snapshot", "matchId": match_id, "payload": snapshot}))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await manager.unregister_ws(client)


@router.get("/sse/matches/{match_id}")
async def sse_match_updates(match_id: str):
    client = SSEClient(match_id)

    async def event_stream():
        await manager.register_sse(client)
        snapshot = await repo.get_detail(match_id)
        yield f"data: {json.dumps({'type': 'snapshot', 'matchId': match_id, 'payload': snapshot})}\n\n"
        try:
            while True:
                data = await client.queue.get()
                yield f"data: {data}\n\n"
        finally:
            await manager.unregister_sse(client)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
