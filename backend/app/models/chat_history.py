from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey, BigInteger, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    chat_mode = Column(Text, nullable=False)  # 'UsoCotidiano' ou 'EscritaLonga'
    use_author_voice = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="chat_history")
    user = relationship("User", back_populates="chat_history")
    agent = relationship("Agent", back_populates="chat_history")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index('idx_chat_history_tenant_id', 'tenant_id'),
        Index('idx_chat_history_user_id', 'user_id'),
        Index('idx_chat_history_agent_id', 'agent_id'),
        Index('idx_chat_history_created_at', 'created_at'),
        Index('idx_chat_history_tenant_created', 'tenant_id', 'created_at'),
        Index('idx_chat_history_chat_mode', 'chat_mode'),
    )
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, tenant_id={self.tenant_id}, user_id={self.user_id})>" 