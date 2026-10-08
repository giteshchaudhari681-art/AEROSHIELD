from app.repositories.base import BaseRepository
from app.infrastructure.db.models import BehaviourEvent

class BehaviourEventRepository(BaseRepository[BehaviourEvent]):
    def __init__(self):
        super().__init__(BehaviourEvent)

behaviours_repo = BehaviourEventRepository()
