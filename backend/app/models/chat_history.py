from pydantic import BaseModel, UUID4
from datetime import datetime

class ChatHistory(BaseModel):
    id: int
    tenant_id: UUID4
    user_id: UUID4
    message: str
    response: str
    created_at: datetime 