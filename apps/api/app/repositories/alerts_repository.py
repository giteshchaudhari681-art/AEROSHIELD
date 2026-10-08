from app.repositories.base import BaseRepository
from app.infrastructure.db.models import Alert

class AlertRepository(BaseRepository[Alert]):
    def __init__(self):
        super().__init__(Alert)

alerts_repo = AlertRepository()
