# matchDetailService - Real-time Extensions

## Overview
This service aggregates match metadata from other micros (matches, teams, competitions) and combines it with locally stored events/stats in TinyDB. It now provides:

- Authenticated write endpoints for meta, events, lineups, stats
- Real-time delivery via WebSocket and SSE
- Redis Pub/Sub broadcasting so multiple instances stay in sync

## Environment variables
```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
MATCHES_BASE_URL=http://localhost:8003
TEAMS_BASE_URL=http://localhost:8001
COMPETITIONS_BASE_URL=http://localhost:8002
PLAYERS_BASE_URL=http://localhost:8005
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=change-me
JWT_ALGORITHM=HS256
API_KEYS=local-dev-key
```

## Running locally
```powershell
docker run -d --name redis-realtime -p 6379:6379 redis:7
cd matchDetailService-Tiny
pip install -r requirements.txt
python run.py
```

## Authentication
All write endpoints require either:
- `Authorization: Bearer <JWT>` (signed with `JWT_SECRET`), or
- `x-api-key: <value>` present in `API_KEYS`.

## HTTP API
- `GET /api/v1/match-details/{matchId}` → aggregated payload
- `PATCH /api/v1/match-details/{matchId}/meta`
- `POST /api/v1/match-details/{matchId}/events`
- `PUT /api/v1/match-details/{matchId}/lineups`
- `PUT /api/v1/match-details/{matchId}/stats`

All responses follow `{ "type": <event-type>, "matchId": <id>, "payload": { ... } }` when broadcast.

## Realtime
- WebSocket: `ws://host:port/ws/matches/{matchId}`
- SSE: `http://host:port/sse/matches/{matchId}`

Clients receive a `snapshot` message after connecting and every subsequent update published anywhere in the cluster.

## Scaling
Deploy multiple instances pointing to the same Redis. Each instance subscribes to the shared channel (`match-detail-updates`) and forwards messages to its connected clients.

## Front-end example
```js
const ws = new WebSocket("ws://localhost:8004/ws/matches/MATCH_123");
ws.onmessage = (evt) => console.log(JSON.parse(evt.data));

const es = new EventSource("http://localhost:8004/sse/matches/MATCH_123");
es.onmessage = (evt) => console.log(JSON.parse(evt.data));
```

## Why this architecture?

- **Consistent aggregation**: matchDetailService continua sendo o ponto único que junta match + teams + competition + dados locais, preservando o contrato já consumido pelo front.
- **Tempo real de verdade**: WebSocket e SSE entregam snapshot inicial e cada alteração subsequente, eliminando polling.
- **Escalável entre instâncias**: Redis Pub/Sub garante que qualquer pod que receba um update publique o evento e todos retransmitam para seus clientes.
- **Segurança pragmática**: aceitar JWT ou API Key cobre tanto automações quanto painéis internos.
- **Operação clara**: README documenta env vars, comandos e fluxos, facilitando troubleshooting e onboarding.
