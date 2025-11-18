import logging
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

import httpx
from fastapi import APIRouter, status

from .config import MATCH_DETAIL_BASE_URL, REQUEST_TIMEOUT, BROADCAST_PATH
from .models import EventCreate, EventOut
from .repository import repo

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", summary="Service info")
async def root():
    return {"service": "eventsService", "status": "ok"}


async def _notify_match_detail(event_payload: dict):
    url = f"{MATCH_DETAIL_BASE_URL.rstrip('/')}{BROADCAST_PATH}"
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(url, json=event_payload)
            if response.status_code >= 400:
                logger.warning("matchDetailService broadcast responded with %s: %s", response.status_code, response.text)
    except httpx.RequestError as exc:
        logger.warning("Could not notify matchDetailService: %s", exc)


@router.post(
    "/api/v1/matches/{match_id}/events",
    response_model=EventOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a match event",
)
async def create_event(match_id: str, payload: EventCreate):
    doc = payload.model_dump()
    doc["id"] = str(uuid4())
    doc["matchId"] = match_id
    doc["createdAt"] = datetime.now(timezone.utc)
    saved = repo.insert(doc)
    await _notify_match_detail(saved)
    return saved


@router.get(
    "/api/v1/matches/{match_id}/events",
    response_model=List[EventOut],
    summary="List events for a match",
)
async def list_events(match_id: str):
    return repo.list_by_match(match_id)
