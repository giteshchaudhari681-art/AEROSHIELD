from app.repositories.base import BaseRepository
from app.infrastructure.db.models import RestrictedZone

class RestrictedZoneRepository(BaseRepository[RestrictedZone]):
    def __init__(self):
        super().__init__(RestrictedZone)



    def find_containing_point(self, db, lat: float, lon: float):
        from sqlalchemy import func
        point = f"SRID=4326;POINT({lon} {lat})"
        return db.query(self.model).filter(
            func.ST_Contains(self.model.boundary, func.ST_GeomFromText(point, 4326))
        ).all()

zones_repo = RestrictedZoneRepository()
