
from tinydb import Query
from datetime import datetime
from typing import Dict, Any, Optional
import json, httpx
from .database import details_table, events_table, lineups_table, stats_table
from .config import MATCHES_BASE_URL, TEAMS_BASE_URL, COMPETITIONS_BASE_URL, REQUEST_TIMEOUT

class DetailRepository:
    def _ser(self, d: Dict[str, Any]): return json.loads(json.dumps(d, default=str, ensure_ascii=False))
    def upsert_meta(self, doc: Dict[str, Any]):
        q = Query()
        if details_table.search(q.id == doc["id"]): details_table.update(self._ser(doc), q.id == doc["id"])
        else: details_table.insert(self._ser(doc))
    def get_meta(self, mid: str):
        r = details_table.search(Query().id == mid)
        return r[0] if r else None
    def add_event(self, mid: str, ev: Dict[str, Any]):
        evd = dict(ev, matchId=mid, id=ev.get("id") or f"EVT_{int(datetime.utcnow().timestamp()*1000)}")
        events_table.insert(self._ser(evd)); return evd
    def list_events(self, mid: str): return sorted(events_table.search(Query().matchId == mid), key=lambda e:e.get("minute",0))
    def get_lineups(self, mid: str):
        r = lineups_table.search(Query().matchId == mid); return r[0] if r else {"home":[],"away":[]}
    def get_stats(self, mid: str):
        r = stats_table.search(Query().matchId == mid); return r[0] if r else {"home":{"score":0},"away":{"score":0},"players":[]}
    async def _safe(self, url):
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as c:
                r = await c.get(url)
                if r.status_code==200: return r.json()
        except: return None
    async def get_detail(self, mid: str):
        meta = self.get_meta(mid) or {"id":mid,"status":"SCHEDULED"}
        if MATCHES_BASE_URL: meta = await self._safe(f"{MATCHES_BASE_URL}/api/v1/matches/{mid}") or meta
        home = await self._safe(f"{TEAMS_BASE_URL}/api/v1/teams/{meta.get('homeTeamId')}") if TEAMS_BASE_URL and meta.get("homeTeamId") else None
        away = await self._safe(f"{TEAMS_BASE_URL}/api/v1/teams/{meta.get('awayTeamId')}") if TEAMS_BASE_URL and meta.get("awayTeamId") else None
        comp = await self._safe(f"{COMPETITIONS_BASE_URL}/api/v1/competitions/{meta.get('competitionId')}") if COMPETITIONS_BASE_URL and meta.get("competitionId") else None
        return {"match":meta,"homeTeam":home,"awayTeam":away,"competition":comp,
                "events":self.list_events(mid),"lineups":self.get_lineups(mid),"stats":self.get_stats(mid)}
