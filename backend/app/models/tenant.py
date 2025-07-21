from sqlalchemy import Column, String, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    subdomain = Column(Text, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    agents = relationship("Agent", back_populates="tenant", cascade="all, delete-orphan")
    settings = relationship("TenantSettings", back_populates="tenant", uselist=False, cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="tenant", cascade="all, delete-orphan")
    document_chunks = relationship("DocumentChunk", back_populates="tenant", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index('idx_tenants_subdomain', 'subdomain'),
        Index('idx_tenants_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', subdomain='{self.subdomain}')>" 