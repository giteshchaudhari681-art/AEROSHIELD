from app.repositories.base import BaseRepository
from app.infrastructure.db.models import RestrictedZone

class RestrictedZoneRepository(BaseRepository[RestrictedZone]):
    def __init__(self):
        super().__init__(RestrictedZone)

zones_repo = RestrictedZoneRepository()
