import asyncio
import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, status
from sqlalchemy.orm import Session, joinedload
from app.core.config import settings
from app.infrastructure.db.session import SessionLocal, get_db
from app.infrastructure.db.models import Operator, Role
from app.services.websocket_manager import ws_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def _authenticate_ws(token: str, db: Session) -> Operator:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
        
    user = db.query(Operator).options(joinedload(Operator.roles).joinedload(Role.permissions)).filter(Operator.id == user_id).first()
    if user is None or not user.active:
        raise ValueError("User not found or inactive")
        
    return user

def _check_permission(user: Operator, required_permission: str) -> bool:
    for role in user.roles:
        for perm in role.permissions:
            if perm.name == required_permission or perm.name == "admin:manage":
                return True
    return False

@router.websocket("/ws/observations")
async def websocket_observations(websocket: WebSocket, token: str = Query(...)):
    db = SessionLocal()
    try:
        user = _authenticate_ws(token, db)
        if not _check_permission(user, "observation:read"):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except ValueError as e:
        logger.warning(f"WebSocket auth failed: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    finally:
        db.close()

    conn = await ws_manager.connect(websocket, user.id)
    try:
        while True:
            data = await websocket.receive_json()
            # Handle client commands like subscribe/unsubscribe
            action = data.get("action")
            if action == "subscribe":
                filters = data.get("filters", {})
                conn.filters = filters
                await conn.send_json({"type": "subscription.ack", "status": "subscribed"})
            elif action == "unsubscribe":
                conn.filters = {}
                await conn.send_json({"type": "subscription.ack", "status": "unsubscribed"})
            elif action == "ping":
                pass
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        ws_manager.disconnect(conn)
