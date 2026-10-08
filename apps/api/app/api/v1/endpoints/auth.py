from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.schemas.auth import Token, LoginRequest, OperatorRead
from app.services.auth_service import auth_service
from app.core.security import create_access_token
from app.core.config import settings
from app.infrastructure.db.session import get_db
from app.api.dependencies.auth import get_current_operator
from app.infrastructure.db.models import Operator
from app.services.audit_service import audit_service

router = APIRouter()

@router.post("/login", response_model=Token)
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    operator = auth_service.authenticate(db, email=login_data.username, password=login_data.password)
    ip = request.client.host if request.client else None
    if not operator:
        audit_service.log(db, actor_id="unknown", action="LOGIN_FAILURE", metadata_json={"username": login_data.username}, ip_address=ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=operator.id)
    audit_service.log(db, actor_id=operator.id, action="LOGIN_SUCCESS", ip_address=ip)
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
