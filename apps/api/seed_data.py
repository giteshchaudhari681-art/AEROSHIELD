import asyncio
import uuid
from sqlalchemy.orm import Session
from app.infrastructure.db.session import engine, SessionLocal
from app.infrastructure.db.models import (
    Site, CriticalAsset, RestrictedZone, Sensor,
    SiteType, AssetCriticality, ZoneSeverity,
    AerialTrack, TrackStatus, ThreatAssessment, ThreatLevel
)

def seed_db():
    db: Session = SessionLocal()
    
    # Check if site exists
    if db.query(Site).first():
        print("Database already seeded.")
        return
        
    print("Seeding database...")
    
    # 1. Site
    site_id = "site-test-01"
    site = Site(
        id=site_id,
        name="Delta Power Generation Facility",
        description="Fictional critical power generation facility for testing.",
        site_type=SiteType.POWER_PLANT,
        location="SRID=4326;POINT(-122.4194 37.7749)",
        boundary="SRID=4326;POLYGON((-122.4200 37.7750, -122.4180 37.7750, -122.4180 37.7730, -122.4200 37.7730, -122.4200 37.7750))"
    )
    db.add(site)
    
    # 2. Assets
    asset1 = CriticalAsset(
        id=f"asset-{uuid.uuid4()}",
        site_id=site_id,
        name="Generator Unit Alpha",
        asset_type="GENERATOR",
        criticality=AssetCriticality.CRITICAL,
        location="SRID=4326;POINT(-122.4190 37.7745)",
        protection_radius=50.0
    )
    asset2 = CriticalAsset(
        id=f"asset-{uuid.uuid4()}",
        site_id=site_id,
        name="Cooling Tower 1",
        asset_type="COOLING_SYSTEM",
        criticality=AssetCriticality.HIGH,
        location="SRID=4326;POINT(-122.4185 37.7740)",
        protection_radius=30.0
    )
    db.add_all([asset1, asset2])
    
    # 3. Zones
    zone1 = RestrictedZone(
        id=f"zone-{uuid.uuid4()}",
        site_id=site_id,
        name="Inner Core No-Fly Zone",
        zone_type="NO_FLY",
        boundary="SRID=4326;POLYGON((-122.4195 37.7748, -122.4185 37.7748, -122.4185 37.7738, -122.4195 37.7738, -122.4195 37.7748))",
        severity=ZoneSeverity.CRITICAL
    )
    db.add(zone1)
    
    # 4. Sensors
    sensor1 = Sensor(
        id=f"sensor-{uuid.uuid4()}",
        site_id=site_id,
        name="Primary Radar Alpha",
        sensor_type="RADAR",
        location="SRID=4326;POINT(-122.4194 37.7749)"
    )
    sensor2 = Sensor(
        id=f"sensor-{uuid.uuid4()}",
        site_id=site_id,
        name="RF Scanner 1",
        sensor_type="RF",
        location="SRID=4326;POINT(-122.4190 37.7749)"
    )
    db.add_all([sensor1, sensor2])
    
    db.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    seed_db()
