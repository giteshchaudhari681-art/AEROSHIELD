from app.repositories.base import BaseRepository
from app.infrastructure.db.models import Sensor

class SensorRepository(BaseRepository[Sensor]):
    def __init__(self):
        super().__init__(Sensor)

sensors_repo = SensorRepository()
