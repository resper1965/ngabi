"""
Schemas para endpoints de chat.
"""

from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime


class ChatRequest(BaseModel):
    user_id: uuid.UUID
    agent_id: uuid.UUID
    message: str
    chat_mode: str = "UsoCotidiano"
    use_author_voice: bool = False
    kb_filters: Optional[List[str]] = None


class ChatResponse(BaseModel):
    id: uuid.UUID
    message: str
    response: str
    agent_name: str
    chat_mode: str
    created_at: Optional[str] = None


class ChatMessage(BaseModel):
    id: uuid.UUID
    content: str
    speaker: str  # 'user' ou 'agent'
    timestamp: str 