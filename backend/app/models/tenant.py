from pydantic import BaseModel, UUID4

class Tenant(BaseModel):
    id: UUID4
    name: str 