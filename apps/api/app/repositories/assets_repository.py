from app.repositories.base import BaseRepository
from app.infrastructure.db.models import CriticalAsset

class CriticalAssetRepository(BaseRepository[CriticalAsset]):
    def __init__(self):
        super().__init__(CriticalAsset)



    def find_within_radius(self, db, lat: float, lon: float, radius_m: float):
        from sqlalchemy import func
        point = f"SRID=4326;POINT({lon} {lat})"
        return db.query(self.model).filter(
            func.ST_DWithin(func.ST_GeographyFromText(func.ST_AsText(self.model.location)), 
                            func.ST_GeographyFromText(point), radius_m)
        ).all()
        
    def find_inside_zone(self, db, zone_boundary):
        from sqlalchemy import func
        return db.query(self.model).filter(
            func.ST_Contains(zone_boundary, self.model.location)
        ).all()

assets_repo = CriticalAssetRepository()
