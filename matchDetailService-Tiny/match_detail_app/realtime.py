"""Realtime helpers: Channel manager + Redis Pub/Sub broadcaster."""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from typing import Dict, Set

from fastapi import WebSocket
from redis.asyncio import Redis


@dataclass(eq=False)
class WSClient:
    websocket: WebSocket
    match_id: str

    def __hash__(self):
        return hash(id(self.websocket))


@dataclass(eq=False)
class SSEClient:
    match_id: str
    queue: asyncio.Queue[str] = field(default_factory=asyncio.Queue)

    def __hash__(self):
        return hash(id(self.queue))


class ChannelManager:
    def __init__(self):
        self._ws: Dict[str, Set[WSClient]] = {}
        self._sse: Dict[str, Set[SSEClient]] = {}
        self._lock = asyncio.Lock()

    async def register_ws(self, client: WSClient):
        await self._add(self._ws, client.match_id, client)

    async def unregister_ws(self, client: WSClient):
        await self._remove(self._ws, client.match_id, client)

    async def register_sse(self, client: SSEClient):
        await self._add(self._sse, client.match_id, client)

    async def unregister_sse(self, client: SSEClient):
        await self._remove(self._sse, client.match_id, client)

    async def broadcast(self, message: dict):
        match_id = message["matchId"]
        data = json.dumps(message)
        for client in list(self._ws.get(match_id, set())):
            await client.websocket.send_text(data)
        for client in list(self._sse.get(match_id, set())):
            await client.queue.put(data)

    async def _add(self, bucket, key, client):
        async with self._lock:
            bucket.setdefault(key, set()).add(client)

    async def _remove(self, bucket, key, client):
        async with self._lock:
            if key in bucket:
                bucket[key].discard(client)
                if not bucket[key]:
                    bucket.pop(key)


class RedisBroadcaster:
    """Publishes/consumes realtime messages using a shared Redis channel."""

    def __init__(self, redis_url: str, channel: str = "match-detail-updates"):
        self._redis = Redis.from_url(redis_url, decode_responses=True)
        self._channel = channel
        self._task: asyncio.Task | None = None
        self._manager: ChannelManager | None = None

    async def start(self, manager: ChannelManager):
        self._manager = manager
        self._task = asyncio.create_task(self._listen())

    async def stop(self):
        if self._task:
            self._task.cancel()
        await self._redis.close()

    async def publish(self, message: dict):
        await self._redis.publish(self._channel, json.dumps(message))

    async def _listen(self):
        pubsub = self._redis.pubsub()
        await pubsub.subscribe(self._channel)
        async for msg in pubsub.listen():
            if msg["type"] != "message":
                continue
            payload = json.loads(msg["data"])
            if self._manager:
                await self._manager.broadcast(payload)
