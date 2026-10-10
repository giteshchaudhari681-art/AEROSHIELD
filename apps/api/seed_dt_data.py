import os
import sys
import json
import logging
from sqlalchemy.orm import Session
from shapely.geometry import Point, Polygon
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import Site, CriticalAsset, RestrictedZone, SiteType, AssetCriticality, ZoneSeverity, OperationalStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_dt():
    db = SessionLocal()
    try:
        # 1. Site
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
            logger.info("Created Demo Site")

        # 2. Assets
        assets = [
            ("asset-001", "Main Control Center", "CTRL", "COMMAND_CENTER", AssetCriticality.CRITICAL, OperationalStatus.OPERATIONAL, -122.415, 37.775, 50),
            ("asset-002", "Power Substation", "PWR", "SUBSTATION", AssetCriticality.HIGH, OperationalStatus.OPERATIONAL, -122.416, 37.776, 30),
            ("asset-003", "Communication Tower", "COM", "COMMUNICATION_TOWER", AssetCriticality.MEDIUM, OperationalStatus.DEGRADED, -122.414, 37.774, 20),
            ("asset-004", "Fuel Storage Area", "FUEL", "FUEL_STORAGE", AssetCriticality.HIGH, OperationalStatus.MAINTENANCE, -122.417, 37.777, 40),
            ("asset-005", "Operations Building", "OPS", "BUILDING", AssetCriticality.LOW, OperationalStatus.OPERATIONAL, -122.418, 37.772, 25),
            ("asset-006", "Secondary Substation", "PWR-2", "SUBSTATION", AssetCriticality.HIGH, OperationalStatus.OPERATIONAL, -122.411, 37.776, 30),
            ("asset-007", "Security Checkpoint Alpha", "SEC-A", "BUILDING", AssetCriticality.MEDIUM, OperationalStatus.OPERATIONAL, -122.413, 37.778, 15),
            ("asset-008", "Security Checkpoint Beta", "SEC-B", "BUILDING", AssetCriticality.MEDIUM, OperationalStatus.OPERATIONAL, -122.419, 37.771, 15),
            ("asset-009", "Water Pump Station", "WTR", "INFRASTRUCTURE", AssetCriticality.LOW, OperationalStatus.OFFLINE, -122.412, 37.772, 20),
            ("asset-010", "Backup Generator", "GEN", "INFRASTRUCTURE", AssetCriticality.CRITICAL, OperationalStatus.OPERATIONAL, -122.416, 37.774, 20)
        ]
        
        for aid, name, code, atype, crit, op_status, lon, lat, rad in assets:
            a = db.query(CriticalAsset).filter(CriticalAsset.id == aid).first()
            if not a:
                a = CriticalAsset(
                    id=aid,
                    site_id=site_id,
                    name=name,
                    asset_code=code,
                    asset_type=atype,
                    description=f"{name} at {site.name}",
                    criticality=crit,
                    operational_status=op_status,
                    location=f"SRID=4326;POINT({lon} {lat})",
                    protection_radius=rad,
                    status="ACTIVE"
                )
                db.add(a)
        
        db.commit()
        logger.info("Created Demo Assets")

        # 3. Zones
        zones = [
            ("zone-001", "Inner Restricted Zone", "INNER", "RESTRICTED", ZoneSeverity.CRITICAL, -122.416, 37.776, 0.002),
            ("zone-002", "Outer Perimeter Zone", "OUTER", "PERIMETER", ZoneSeverity.MEDIUM, -122.415, 37.775, 0.005),
            ("zone-003", "Temporary Sensitive Zone", "TEMP", "SENSITIVE", ZoneSeverity.HIGH, -122.417, 37.777, 0.001)
        ]
        
        for zid, name, code, ztype, sev, clon, clat, offset in zones:
            z = db.query(RestrictedZone).filter(RestrictedZone.id == zid).first()
            if not z:
                # Create a square polygon around center
                poly = f"SRID=4326;POLYGON(({clon-offset} {clat-offset}, {clon+offset} {clat-offset}, {clon+offset} {clat+offset}, {clon-offset} {clat+offset}, {clon-offset} {clat-offset}))"
                z = RestrictedZone(
                    id=zid,
                    site_id=site_id,
                    name=name,
                    zone_code=code,
                    description=f"{name} covering area",
                    zone_type=ztype,
                    severity=sev,
                    boundary=poly,
                    active=True
                )
                db.add(z)
                
        db.commit()
        logger.info("Created Demo Zones")

    finally:
        db.close()

if __name__ == "__main__":
    seed_dt()
