import os

base_dir = "d:/SEVA/apps/api/app"

auth_schemas_content = """from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class LoginRequest(BaseModel):
    username: str
    password: str

class OperatorRead(BaseModel):
    id: str
    name: str
    email: str
    active: bool
    created_at: datetime
    roles: List[str]
    model_config = ConfigDict(from_attributes=True)
"""

auth_service_content = """from sqlalchemy.orm import Session
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
"""

auth_deps_content = """from fastapi import Depends, HTTPException, status
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
"""

auth_router_content = """from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import Token, LoginRequest, OperatorRead
from app.services.auth_service import auth_service
from app.core.security import create_access_token
from app.core.config import settings
from app.infrastructure.db.session import get_db
from app.api.dependencies.auth import get_current_operator
from app.infrastructure.db.models import Operator

router = APIRouter()

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    operator = auth_service.authenticate(db, email=request.username, password=request.password)
    if not operator:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=operator.id)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@router.get("/me", response_model=OperatorRead)
def read_users_me(current_operator: Operator = Depends(get_current_operator)):
    roles = [r.name for r in current_operator.roles]
    return OperatorRead(
        id=current_operator.id,
        name=current_operator.name,
        email=current_operator.email,
        active=current_operator.active,
        created_at=current_operator.created_at,
        roles=roles
    )
"""

os.makedirs(f"{base_dir}/schemas", exist_ok=True)
os.makedirs(f"{base_dir}/api/dependencies", exist_ok=True)
os.makedirs(f"{base_dir}/api/v1/endpoints", exist_ok=True)

with open(f"{base_dir}/schemas/auth.py", "w") as f: f.write(auth_schemas_content)
with open(f"{base_dir}/services/auth_service.py", "w") as f: f.write(auth_service_content)
with open(f"{base_dir}/api/dependencies/auth.py", "w") as f: f.write(auth_deps_content)
with open(f"{base_dir}/api/v1/endpoints/auth.py", "w") as f: f.write(auth_router_content)

print("Scaffolded auth structure.")
