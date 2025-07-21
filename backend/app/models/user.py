from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    email = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False)  # 'admin', 'user', 'developer'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="users")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index('idx_users_tenant_id', 'tenant_id'),
        Index('idx_users_email', 'email'),
        Index('idx_users_role', 'role'),
        Index('idx_users_is_active', 'is_active'),
        Index('idx_users_created_at', 'created_at'),
        # Constraint único para email por tenant
        {'sqlite_on_conflict': 'REPLACE'}
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>" 