import pytest
import datetime
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import EventOutbox, Sensor, SensorStatus, Site
from app.services.observations_service import observations_service

def test_observation_creates_event_outbox():
    db = SessionLocal()
    
    import uuid
    site_id = str(uuid.uuid4())
    site = Site(
        id=site_id,
        name="Test Site",
        site_type="DEFENCE_INSTALLATION",
        status="ACTIVE",
        location="SRID=4326;POINT(-115.123 35.123)"
    )
    db.add(site)

    sensor = Sensor(
        id=str(uuid.uuid4()),
        name="Test Sensor",
        sensor_type="RADAR",
        operational_status=SensorStatus.ACTIVE,
        is_enabled=True,
        site_id=site_id,
        location="SRID=4326;POINT(-115.123 35.123)"
    )
    db.add(sensor)
    db.commit()
    
    # Ingest a raw observation
    raw_payload = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "lat": 35.123,
        "lon": -115.123,
        "alt": 100.0,
        "velocity": 15.0,
        "heading": 90.0,
        "type": "drone",
        "confidence": 0.95
    }
    
    observations = observations_service.ingest_raw(
        db=db,
        sensor_id=sensor.id,
        raw_payload=raw_payload,
        correlation_id="test_corr_id"
    )
    
    assert len(observations) > 0
    obs = observations[0]
    
    # Check outbox
    events = db.query(EventOutbox).filter(EventOutbox.aggregate_id == obs.id).all()
    assert len(events) == 1
    
    event = events[0]
    assert event.event_type == "observation.created"
    assert event.aggregate_type == "sensor_observation"
    assert event.payload["observation_id"] == obs.id
    assert event.status.value == "PENDING"
    
    db.close()
