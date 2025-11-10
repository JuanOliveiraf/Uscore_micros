from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone
from .models import MatchIn, MatchOut
from .repository import MatchesRepository

router = APIRouter()
repo = MatchesRepository()

@router.get('/')
def root():
    return {'service': 'matchesService', 'status': 'ok'}

@router.post('/api/v1/matches', response_model=MatchOut, status_code=status.HTTP_201_CREATED)
async def create_match(m: MatchIn):
    d = m.model_dump(mode='json')
    d['id'] = f'MATCH_{uuid4().hex[:8].upper()}'
    d['createdAt'] = datetime.now(timezone.utc).isoformat()
    return repo.insert(d)

@router.get('/api/v1/matches')
async def list_matches(
    sport: Optional[str] = None,
    teamId: Optional[str] = None,
    competitionId: Optional[str] = None,
    status: Optional[str] = Query(None, regex='^(SCHEDULED|LIVE|FINISHED)$'),
    upcoming: Optional[bool] = False,
    limit: int = 20,
    offset: int = 0,
):
    f = {'sport': sport, 'teamId': teamId, 'competitionId': competitionId, 'status': status, 'upcoming': upcoming}
    rsl = repo.list(f, limit, offset)
    return {'data': rsl['items'], 'meta': {'total': rsl['total'], 'limit': limit, 'offset': offset, 'hasMore': (offset + limit) < rsl['total']}}

@router.get('/api/v1/matches/{match_id}', response_model=MatchOut)
async def get_match(match_id: str):
    d = repo.get(match_id)
    if not d: raise HTTPException(status_code=404, detail='Match not found')
    return d

@router.delete('/api/v1/matches/{match_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(match_id: str):
    ok = repo.remove(match_id)
    if not ok: raise HTTPException(status_code=404, detail='Match not found')
    return
