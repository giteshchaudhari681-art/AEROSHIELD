import os
import sys

def add_models():
    models_path = "app/infrastructure/db/models.py"
    with open(models_path, "r") as f:
        content = f.read()

    if "EventOutbox" not in content:
        outbox_code = """
class OutboxStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

class EventOutbox(Base):
    __tablename__ = "event_outbox"

    id = Column(String, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    schema_version = Column(Integer, nullable=False, default=1)
    aggregate_type = Column(String, nullable=False)
    aggregate_id = Column(String, nullable=False)
    correlation_id = Column(String, nullable=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    
    payload = Column(JSON, nullable=False)
    
    status = Column(SQLEnum(OutboxStatus), nullable=False, default=OutboxStatus.PENDING, index=True)
    attempts = Column(Integer, nullable=False, default=0)
    available_at = Column(DateTime(timezone=True), nullable=False, index=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
"""
        with open(models_path, "a") as f:
            f.write(outbox_code)
        print("Models added.")
    else:
        print("Models already exist.")

if __name__ == "__main__":
    add_models()
