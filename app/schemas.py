from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# --- Project & Client Schemas ---
# Forward declarations and basic versions for outputs

class ProjectCreate(BaseModel):
    project_name: str
    client_id: int
    users: List[int]

class ClientCreate(BaseModel):
    client_name: str

class ClientResponseSimple(BaseModel):
    id: int
    client_name: str
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: int
    project_name: str
    client_name: str
    users: List[UserResponse]

    class Config:
        from_attributes = True

class ClientResponse(ClientResponseSimple):
    projects: List[ProjectResponse] = []

    class Config:
        from_attributes = True
