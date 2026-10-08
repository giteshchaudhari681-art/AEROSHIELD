import asyncio
import json
import logging
from redis.asyncio import Redis
from typing import Optional

from app.core.config import settings
from app.services.websocket_manager import ws_manager
from app.services.fusion_consumer import FusionConsumer

logger = logging.getLogger(__name__)

class RedisEventSubscriber:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self.pubsub = None
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        if self._task and not self._task.done():
            return
            
        self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe("aeroshield:events:observation.created")
        
        self._task = asyncio.create_task(self._listen_loop())
        logger.info("RedisEventSubscriber started")
        
    async def stop(self):
        if self._task:
            self._task.cancel()
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()
        logger.info("RedisEventSubscriber stopped")

    async def _listen_loop(self):
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        event = json.loads(message["data"])
                        # Route to fusion consumer in background thread
                        await asyncio.to_thread(FusionConsumer.handle_event, event)
                        # Route to WebSocket manager
                        await ws_manager.broadcast(event)
                    except json.JSONDecodeError:
                        logger.error("Failed to decode Redis message")
                    except Exception as e:
                        logger.error(f"Error broadcasting event: {e}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Redis listener error: {e}")

redis_subscriber = RedisEventSubscriber()
