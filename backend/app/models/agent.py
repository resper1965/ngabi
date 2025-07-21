from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    config = Column(JSONB, nullable=False)  # prompt templates, flows, KB filters
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="agents")
    chat_history = relationship("ChatHistory", back_populates="agent", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index('idx_agents_tenant_id', 'tenant_id'),
        Index('idx_agents_name', 'name'),
        Index('idx_agents_created_at', 'created_at'),
        # Constraint único para nome por tenant
        {'sqlite_on_conflict': 'REPLACE'}
    )
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', tenant_id={self.tenant_id})>" 