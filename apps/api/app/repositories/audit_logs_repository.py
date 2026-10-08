from app.repositories.base import BaseRepository
from app.infrastructure.db.models import AuditLog

class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

audit_logs_repo = AuditLogRepository()
