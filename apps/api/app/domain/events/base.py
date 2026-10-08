from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from typing import Any, Dict

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    schema_version: int = 1
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str | None = None
    aggregate_type: str
    aggregate_id: str
    payload: Dict[str, Any]
