import threading
import time
import json
import redis
from typing import Optional
import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.db.session import SessionLocal
from app.repositories.event_outbox_repository import outbox_repo

logger = logging.getLogger(__name__)

class EventPublisherService:
    def __init__(self):
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        # Initialize synchronous redis client for publisher thread
        self.redis_client = redis.from_url(settings.REDIS_URL)
        
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("EventPublisherService started")
        
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        logger.info("EventPublisherService stopped")
            
    def _run_loop(self):
        while not self._stop_event.is_set():
            try:
                self._process_batch()
            except Exception as e:
                logger.error(f"Error in EventPublisherService run loop: {e}")
            time.sleep(0.5) # Poll interval
            
    def _process_batch(self):
        db: Session = SessionLocal()
        try:
            events = outbox_repo.claim_pending_events(db, batch_size=50)
            if not events:
                return
                
            for event in events:
                try:
                    # Construct envelope to publish
                    envelope = {
                        "event_id": event.event_id,
                        "event_type": event.event_type,
                        "schema_version": event.schema_version,
                        "occurred_at": event.occurred_at.isoformat(),
                        "correlation_id": event.correlation_id,
                        "aggregate_type": event.aggregate_type,
                        "aggregate_id": event.aggregate_id,
                        "payload": event.payload
                    }
                    
                    # Channel design: aeroshield:events:{event_type}
                    channel = f"aeroshield:events:{event.event_type}"
                    
                    # Publish to redis
                    self.redis_client.publish(channel, json.dumps(envelope))
                    
                    # Mark published
                    outbox_repo.mark_published(db, event.event_id)
                except Exception as e:
                    logger.error(f"Failed to publish event {event.event_id}: {e}")
                    outbox_repo.mark_failed(db, event.event_id, str(e), max_attempts=5, retry_delay_seconds=2)
            
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

event_publisher = EventPublisherService()
