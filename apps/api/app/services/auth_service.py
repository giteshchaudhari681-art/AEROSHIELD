from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.infrastructure.db.models import Operator, Role, Permission, OperatorRole, RefreshToken
from app.core.security import verify_password, get_password_hash, create_access_token
from typing import Optional
from datetime import datetime, timezone
import uuid

class AuthService:
    def authenticate(self, db: Session, email: str, password: str) -> Optional[Operator]:
        user = db.query(Operator).filter(Operator.email == email).first()
        if not user or not user.active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

auth_service = AuthService()
