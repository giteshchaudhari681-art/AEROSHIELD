from app.repositories.base import BaseRepository
from app.infrastructure.db.models import SensorObservation

class SensorObservationRepository(BaseRepository[SensorObservation]):
    def __init__(self):
        super().__init__(SensorObservation)

observations_repo = SensorObservationRepository()
