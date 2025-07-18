from pydantic import BaseModel, UUID4, EmailStr

class User(BaseModel):
    id: UUID4
    tenant_id: UUID4
    email: EmailStr
    role: str 