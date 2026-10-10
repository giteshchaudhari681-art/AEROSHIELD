import os
import sys
import json
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import (
    Site, CriticalAsset, RestrictedZone, Sensor, AerialTrack, SensorObservation,
    ThreatAssessment, Alert, Incident, Operator, Role, Permission,
    SiteType, AssetCriticality, ZoneSeverity, OperationalStatus,
    SensorStatus, SensorHealthStatus, TrackStatus, ThreatLevel,
    AlertStatus, IncidentStatus, ObservationType
)
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_demo_data():
    db = SessionLocal()
    try:
        # 1. Operators & Roles
        admin_email = "testadmin@aeroshield.com"
        viewer_email = "viewer@aeroshield.com"
        
        admin_op = db.query(Operator).filter(Operator.email == admin_email).first()
        if not admin_op:
            admin_op = Operator(
                id="op-admin-001",
                name="Admin User",
                email=admin_email,
                password_hash=get_password_hash("password"),
                active=True
            )
            db.add(admin_op)
            
        viewer_op = db.query(Operator).filter(Operator.email == viewer_email).first()
        if not viewer_op:
            viewer_op = Operator(
                id="op-viewer-001",
                name="Demo Viewer",
                email=viewer_email,
                password_hash=get_password_hash("viewer"),
                active=True
            )
            db.add(viewer_op)
            
        db.commit()
        logger.info("Demo operators created/verified.")

        # 2. Site
        site_id = "site-demo-dt-001"
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            site = Site(
                id=site_id,
                name="Demo Industrial Security Site",
                site_code="IND-001",
                description="Synthetic infrastructure for AEROSHIELD testing",
                site_type=SiteType.OTHER,
                status="ACTIVE",
                location="SRID=4326;POINT(-122.4194 37.7749)",
                boundary="SRID=4326;POLYGON((-122.42 37.77, -122.41 37.77, -122.41 37.78, -122.42 37.78, -122.42 37.77))"
            )
            db.add(site)
            db.commit()

        # 2.5 Assets & Zones
        asset_id = "asset-002"
        asset = db.query(CriticalAsset).filter(CriticalAsset.id == asset_id).first()
        if not asset:
            asset = CriticalAsset(
                id=asset_id,
                site_id=site_id,
                name="Power Substation",
                asset_code="SUB-01",
                asset_type="INFRASTRUCTURE",
                criticality=AssetCriticality.HIGH,
                operational_status="ACTIVE",
                location="SRID=4326;POINT(-122.417 37.776)",
                protection_radius=100.0,
                status="ACTIVE"
            )
            db.add(asset)
            
        zone_id = "zone-001"
        zone = db.query(RestrictedZone).filter(RestrictedZone.id == zone_id).first()
        if not zone:
            zone = RestrictedZone(
                id=zone_id,
                site_id=site_id,
                name="Inner Restricted Zone",
                zone_code="IRZ-01",
                zone_type="NO_FLY",
                boundary="SRID=4326;POLYGON((-122.418 37.775, -122.416 37.775, -122.416 37.777, -122.418 37.777, -122.418 37.775))",
                severity=ZoneSeverity.CRITICAL,
                active=True
            )
            db.add(zone)
            
        db.commit()
        logger.info("Demo assets and zones created.")

        # 3. Sensors
        sensors = [
            ("sensor-radar-001", "Primary Air Search Radar", "RADAR-01", "RADAR", SensorStatus.ACTIVE, SensorHealthStatus.HEALTHY, -122.419, 37.775),
            ("sensor-rf-001", "RF Direction Finder Alpha", "RF-01", "RF", SensorStatus.ACTIVE, SensorHealthStatus.HEALTHY, -122.415, 37.773),
            ("sensor-eoir-001", "PTZ Electro-Optical Camera", "EOIR-01", "EO_IR", SensorStatus.DEGRADED, SensorHealthStatus.WARNING, -122.417, 37.777),
            ("sensor-acoustic-001", "Acoustic Array Beta", "ACST-01", "ACOUSTIC", SensorStatus.OFFLINE, SensorHealthStatus.CRITICAL, -122.416, 37.772)
        ]
        
        for sid, name, code, stype, op_status, h_status, lon, lat in sensors:
            s = db.query(Sensor).filter(Sensor.id == sid).first()
            if not s:
                s = Sensor(
                    id=sid,
                    site_id=site_id,
                    name=name,
                    sensor_code=code,
                    sensor_type=stype,
                    operational_status=op_status,
                    health_status=h_status,
                    location=f"SRID=4326;POINT({lon} {lat})",
                    manufacturer="Simulated Defense Corp",
                    model="SimulScan 2000"
                )
                db.add(s)
        db.commit()
        logger.info("Demo sensors created.")

        # 4. Tracks & Observations
        now = datetime.now(timezone.utc)
        
        track_id = "track-demo-001"
        track = db.query(AerialTrack).filter(AerialTrack.id == track_id).first()
        if not track:
            track = AerialTrack(
                id=track_id,
                track_identifier="TRK-9982",
                site_id=site_id,
                classification="UAV_ROTARY",
                identification_status="UNKNOWN",
                first_seen_at=now - timedelta(minutes=15),
                last_seen_at=now,
                current_location="SRID=4326;POINT(-122.416 37.775)",
                current_altitude=120.5,
                current_speed=15.2,
                current_heading=45.0,
                confidence=0.85,
                status=TrackStatus.ACTIVE
            )
            db.add(track)
            
            obs = SensorObservation(
                id="obs-demo-001",
                sensor_id="sensor-radar-001",
                track_id=track_id,
                observation_type=ObservationType.POSITION,
                observed_at=now,
                received_at=now,
                sensor_type="RADAR",
                location="SRID=4326;POINT(-122.416 37.775)",
                altitude=120.5,
                speed=15.2,
                heading=45.0,
                confidence=0.9,
                observation_metadata={"synthetic_demo": True}
            )
            db.add(obs)
            
            db.commit()
            logger.info("Demo tracks & observations created.")

        # 5. Threat Assessments & Alerts
        threat_id = "threat-demo-001"
        threat = db.query(ThreatAssessment).filter(ThreatAssessment.id == threat_id).first()
        if not threat:
            threat = ThreatAssessment(
                id=threat_id,
                track_id=track_id,
                site_id=site_id,
                risk_score=85.0,
                threat_level=ThreatLevel.HIGH,
                confidence=0.9,
                reasoning="Unauthorized rotary UAV loitering near Power Substation (asset-002)",
                assessed_at=now
            )
            db.add(threat)
            
            alert = Alert(
                id="alert-demo-001",
                track_id=track_id,
                threat_assessment_id=threat_id,
                alert_type="ZONE_INTRUSION",
                severity=ThreatLevel.HIGH,
                title="Restricted Zone Intrusion",
                message="Unknown UAV entered Inner Restricted Zone (zone-001).",
                status=AlertStatus.OPEN
            )
            db.add(alert)
            db.commit()
            logger.info("Demo alerts created.")
            
        # 6. Incidents
        incident_id = "inc-demo-001"
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            incident = Incident(
                id=incident_id,
                site_id=site_id,
                title="Unauthorized Drone Overflight",
                description="Drone detected loitering above power substation.",
                severity=ThreatLevel.HIGH,
                status=IncidentStatus.INVESTIGATING,
                started_at=now - timedelta(minutes=10)
            )
            db.add(incident)
            
            alert = db.query(Alert).filter(Alert.id == "alert-demo-001").first()
            if alert:
                alert.incident_id = incident_id
                
            db.commit()
            logger.info("Demo incidents created.")
            
    except Exception as e:
        logger.error(f"Error seeding demo data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
