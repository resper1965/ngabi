from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class TenantSettings(Base):
    __tablename__ = "tenant_settings"
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True)
    logo_path = Column(Text)  # caminho no filesystem/NAS
    orchestrator_name = Column(Text)  # nome customizado do agente orquestrador
    theme_primary = Column(String(7))  # ex.: '#1a73e8'
    theme_secondary = Column(String(7))
    contact_email = Column(Text)
    contact_phone = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="settings")
    
    def __repr__(self):
        return f"<TenantSettings(tenant_id={self.tenant_id}, orchestrator_name='{self.orchestrator_name}')>" 