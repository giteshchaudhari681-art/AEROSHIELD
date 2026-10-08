from pydantic import BaseModel, ConfigDict
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
