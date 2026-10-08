from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from app.core.config import settings
from app.infrastructure.db.session import get_db
from app.infrastructure.db.models import Operator, Role
from sqlalchemy.orm import joinedload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_operator(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Operator:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    user = db.query(Operator).options(joinedload(Operator.roles).joinedload(Role.permissions)).filter(Operator.id == user_id).first()
    if user is None or not user.active:
        raise credentials_exception
    return user

class RequirePermission:
    def __init__(self, permission: str):
        self.permission = permission

    def __call__(self, current_operator: Operator = Depends(get_current_operator)):
        for role in current_operator.roles:
            for perm in role.permissions:
                if perm.name == self.permission or perm.name == "admin:manage":
                    return current_operator
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
