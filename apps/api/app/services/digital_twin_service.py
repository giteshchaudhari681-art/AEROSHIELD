from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.infrastructure.db.models import Site, CriticalAsset, RestrictedZone
from app.repositories.assets_repository import assets_repo
from app.repositories.zones_repository import zones_repo
from app.repositories.sites_repository import sites_repo

class DigitalTwinService:
    def get_site_context(self, db: Session, site_id: str) -> Optional[dict]:
        site = sites_repo.get(db, id=site_id)
        if not site:
            return None
            
        assets, _ = assets_repo.get_multi(db, site_id=site_id, limit=1000)
        zones, _ = zones_repo.get_multi(db, site_id=site_id, limit=1000)
        
        return {
            "site": site,
            "assets": assets,
            "restricted_zones": zones,
            "sensors": []
        }
        
    def find_assets_near_point(self, db: Session, latitude: float, longitude: float, radius_m: float) -> List[CriticalAsset]:
        return assets_repo.find_within_radius(db, latitude, longitude, radius_m)
        
    def find_zones_containing_point(self, db: Session, latitude: float, longitude: float) -> List[RestrictedZone]:
        return zones_repo.find_containing_point(db, latitude, longitude)
        
    def find_assets_inside_zone(self, db: Session, zone_id: str) -> List[CriticalAsset]:
        zone = zones_repo.get(db, id=zone_id)
        if not zone:
            return []
        return assets_repo.find_inside_zone(db, zone.boundary)

digital_twin_service = DigitalTwinService()
