import os
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import Sensor, SensorStatus, SensorHealthStatus
import uuid

def seed_sensors():
    db = SessionLocal()
    site_id = "site-demo-dt-001"
    
    sensors = [
        Sensor(
            id="sensor-radar-001",
            site_id=site_id,
            name="Primary Long-Range Radar",
            sensor_code="RDR-L-01",
            sensor_type="RADAR",
            operational_status=SensorStatus.ACTIVE,
            health_status=SensorHealthStatus.HEALTHY,
            is_enabled=True,
            location="SRID=4326;POINT(-122.4194 37.7749)"
        ),
        Sensor(
            id="sensor-rf-001",
            site_id=site_id,
            name="Perimeter RF Scanner",
            sensor_code="RF-S-01",
            sensor_type="RF",
            operational_status=SensorStatus.ACTIVE,
            health_status=SensorHealthStatus.HEALTHY,
            is_enabled=True,
            location="SRID=4326;POINT(-122.4190 37.7750)"
        ),
        Sensor(
            id="sensor-eoir-001",
            site_id=site_id,
            name="PTZ Optical Camera",
            sensor_code="EO-C-01",
            sensor_type="EO_IR",
            operational_status=SensorStatus.ACTIVE,
            health_status=SensorHealthStatus.HEALTHY,
            is_enabled=True,
            location="SRID=4326;POINT(-122.4185 37.7755)"
        ),
        Sensor(
            id="sensor-acoustic-001",
            site_id=site_id,
            name="Microphone Array",
            sensor_code="AC-M-01",
            sensor_type="ACOUSTIC",
            operational_status=SensorStatus.ACTIVE,
            health_status=SensorHealthStatus.HEALTHY,
            is_enabled=True,
            location="SRID=4326;POINT(-122.4199 37.7745)"
        )
    ]
    
    for s in sensors:
        existing = db.query(Sensor).filter_by(id=s.id).first()
        if not existing:
            db.add(s)
    
    db.commit()
    print("Seeded sensors.")

if __name__ == "__main__":
    seed_sensors()
