from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, update
from datetime import datetime, timezone, timedelta
import uuid

from app.infrastructure.db.models import EventOutbox, OutboxStatus
from app.repositories.base import BaseRepository

class EventOutboxRepository(BaseRepository[EventOutbox]):
    def __init__(self):
        super().__init__(EventOutbox)
        
    def create_event(self, db: Session, event_data: dict) -> EventOutbox:
        """Create an event outbox entry"""
        db_obj = EventOutbox(
            id=str(uuid.uuid4()),
            event_id=event_data["event_id"],
            event_type=event_data["event_type"],
            schema_version=event_data["schema_version"],
            aggregate_type=event_data["aggregate_type"],
            aggregate_id=event_data["aggregate_id"],
            correlation_id=event_data.get("correlation_id"),
            occurred_at=event_data["occurred_at"],
            payload=event_data["payload"],
            status=OutboxStatus.PENDING,
            available_at=datetime.now(timezone.utc)
        )
        db.add(db_obj)
        # Flush to get the ID and ensure it's written in the transaction
        db.flush()
        return db_obj

    def claim_pending_events(self, db: Session, batch_size: int = 100) -> List[EventOutbox]:
        """Claim a batch of pending events for processing using SELECT FOR UPDATE"""
        now = datetime.now(timezone.utc)
        
        # We need to execute a raw SQL or use SQLAlchemy 2.0 update/returning
        # For simplicity and broad compatibility, we will select for update skip locked
        
        stmt = (
            select(EventOutbox)
            .where(
                and_(
                    EventOutbox.status == OutboxStatus.PENDING,
                    EventOutbox.available_at <= now
                )
            )
            .limit(batch_size)
            .with_for_update(skip_locked=True)
        )
        
        events = db.execute(stmt).scalars().all()
        
        for event in events:
            event.status = OutboxStatus.PROCESSING
            event.updated_at = now
            
        db.flush()
        return list(events)

    def mark_published(self, db: Session, event_id: str) -> None:
        """Mark an event as successfully published"""
        now = datetime.now(timezone.utc)
        stmt = (
            update(EventOutbox)
            .where(EventOutbox.event_id == event_id)
            .values(status=OutboxStatus.PUBLISHED, published_at=now, updated_at=now)
        )
        db.execute(stmt)
        db.flush()

    def mark_failed(self, db: Session, event_id: str, error: str, max_attempts: int, retry_delay_seconds: int) -> None:
        """Mark an event as failed and schedule retry if below max attempts"""
        event = db.execute(select(EventOutbox).where(EventOutbox.event_id == event_id)).scalar_one_or_none()
        if not event:
            return
            
        now = datetime.now(timezone.utc)
        event.attempts += 1
        event.last_error = error
        event.updated_at = now
        
        if event.attempts >= max_attempts:
            event.status = OutboxStatus.FAILED
        else:
            event.status = OutboxStatus.PENDING
            # Exponential backoff
            backoff = retry_delay_seconds * (2 ** (event.attempts - 1))
            event.available_at = now + timedelta(seconds=backoff)
            
        db.flush()

outbox_repo = EventOutboxRepository()
