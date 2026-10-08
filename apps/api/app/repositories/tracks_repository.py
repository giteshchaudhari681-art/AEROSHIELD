from app.repositories.base import BaseRepository
from app.infrastructure.db.models import AerialTrack

class AerialTrackRepository(BaseRepository[AerialTrack]):
    def __init__(self):
        super().__init__(AerialTrack)

tracks_repo = AerialTrackRepository()
