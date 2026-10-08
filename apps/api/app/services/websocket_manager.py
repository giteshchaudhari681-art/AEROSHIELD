import json
import logging
from typing import Dict, Set, Any
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class Connection:
    def __init__(self, websocket: WebSocket, operator_id: str):
        self.websocket = websocket
        self.operator_id = operator_id
        # Simple subscription filters
        self.filters: Dict[str, Any] = {}

    async def send_json(self, data: dict):
        try:
            await self.websocket.send_json(data)
        except Exception as e:
            logger.error(f"Error sending message to {self.operator_id}: {e}")

class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: Set[Connection] = set()

    async def connect(self, websocket: WebSocket, operator_id: str) -> Connection:
        await websocket.accept()
        conn = Connection(websocket, operator_id)
        self.active_connections.add(conn)
        
        # Send ready
        await conn.send_json({
            "type": "connection.ready",
            "schema_version": 1
        })
        
        return conn

    def disconnect(self, conn: Connection):
        if conn in self.active_connections:
            self.active_connections.remove(conn)

    async def broadcast(self, event: dict):
        event_type = event.get("event_type")
        payload = event.get("payload", {})
        
        for conn in list(self.active_connections):
            # Check filters
            if not self._matches_filters(conn.filters, payload):
                continue
                
            await conn.send_json(event)
            
    def _matches_filters(self, filters: dict, payload: dict) -> bool:
        if not filters:
            return True
            
        if "site_id" in filters and payload.get("site_id") != filters["site_id"]:
            # Note: payload currently doesn't have site_id directly on observations in Prompt 06,
            # but this is how we would check it if it did.
            # Assuming sensor_id or observation_type
            pass
            
        if "sensor_id" in filters and filters["sensor_id"]:
            if payload.get("sensor_id") != filters["sensor_id"]:
                return False
                
        if "observation_type" in filters and filters["observation_type"]:
            if payload.get("observation_type") != filters["observation_type"]:
                return False
                
        return True

ws_manager = WebSocketConnectionManager()
