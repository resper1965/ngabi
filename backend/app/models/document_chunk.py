"""
Modelo SQLAlchemy para document_chunks com suporte a pgvector.
"""

from sqlalchemy import Column, String, DateTime, Text, Integer, BigInteger, ForeignKey, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, VECTOR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class DocumentChunk(Base):
    """Modelo para chunks de documentos com embeddings vetoriais."""
    
    __tablename__ = "document_chunks"
    
    # Identificação
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    
    # Metadados do documento
    document_id = Column(UUID(as_uuid=True), nullable=False)
    chunk_index = Column(Integer, nullable=False)  # índice do chunk no documento
    chunk_size = Column(Integer, nullable=False)   # tamanho do chunk em caracteres
    
    # Conteúdo e processamento
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)  # hash SHA-256 do conteúdo
    embedding = Column(VECTOR(1536))  # vetor de embedding (dimensão padrão OpenAI)
    
    # Metadados da fonte
    source_type = Column(String(50), nullable=False)  # 'livro', 'processo', 'jurisprudencia', etc.
    source_id = Column(String(255), nullable=False)   # ID da fonte original
    source_name = Column(String(500), nullable=False) # nome/título da fonte
    source_path = Column(Text)  # caminho do arquivo (se aplicável)
    
    # Metadados de processamento
    processing_status = Column(String(20), default="pending")  # 'pending', 'processing', 'completed', 'failed'
    processing_error = Column(Text)  # mensagem de erro se falhou
    embedding_model = Column(String(100))  # modelo usado para embedding
    
    # Metadados temporais
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True))  # quando o embedding foi gerado
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="document_chunks")
    
    # Constraints
    __table_args__ = (
        # Índices principais
        Index('idx_document_chunks_tenant_source', 'tenant_id', 'source_type'),
        Index('idx_document_chunks_tenant_id', 'tenant_id'),
        Index('idx_document_chunks_source_type', 'source_type'),
        Index('idx_document_chunks_document_id', 'document_id'),
        Index('idx_document_chunks_processing_status', 'processing_status'),
        Index('idx_document_chunks_created_at', 'created_at'),
        Index('idx_document_chunks_content_hash', 'content_hash'),
        
        # Índices compostos especializados
        Index('idx_document_chunks_tenant_source_status', 'tenant_id', 'source_type', 'processing_status'),
        Index('idx_document_chunks_tenant_document_chunk', 'tenant_id', 'document_id', 'chunk_index'),
        Index('idx_document_chunks_tenant_source_created', 'tenant_id', 'source_type', 'created_at'),
        
        # Constraints
        CheckConstraint(
            'chunk_size > 0 AND chunk_size <= 10000',
            name='chk_document_chunks_chunk_size'
        ),
        CheckConstraint(
            "source_type IN ('livro', 'processo', 'jurisprudencia', 'manual', 'faq', 'legislacao', 'doutrina', 'outro')",
            name='chk_document_chunks_source_type'
        ),
        CheckConstraint(
            "processing_status IN ('pending', 'processing', 'completed', 'failed')",
            name='chk_document_chunks_processing_status'
        ),
        # Constraint único para tenant + document + chunk_index
        {'sqlite_on_conflict': 'REPLACE'}
    )
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, tenant_id={self.tenant_id}, source_type='{self.source_type}', chunk_index={self.chunk_index})>"
    
    def __str__(self):
        return f"Chunk {self.chunk_index} de {self.source_name} ({self.source_type})"
    
    @property
    def is_processed(self) -> bool:
        """Verifica se o chunk foi processado com sucesso."""
        return self.processing_status == "completed" and self.embedding is not None
    
    @property
    def is_pending(self) -> bool:
        """Verifica se o chunk está pendente de processamento."""
        return self.processing_status in ["pending", "processing"]
    
    @property
    def is_failed(self) -> bool:
        """Verifica se o processamento falhou."""
        return self.processing_status == "failed"
    
    def mark_as_processing(self):
        """Marca o chunk como em processamento."""
        self.processing_status = "processing"
        self.processing_error = None
    
    def mark_as_completed(self, embedding, model: str = None):
        """Marca o chunk como processado com sucesso."""
        self.processing_status = "completed"
        self.embedding = embedding
        self.embedding_model = model
        self.processed_at = func.now()
        self.processing_error = None
    
    def mark_as_failed(self, error_message: str):
        """Marca o chunk como falhou no processamento."""
        self.processing_status = "failed"
        self.processing_error = error_message
    
    def get_content_preview(self, max_length: int = 100) -> str:
        """Retorna uma prévia do conteúdo."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."
    
    def to_dict(self, include_embedding: bool = False):
        """Converte o modelo para dicionário."""
        data = {
            "id": self.id,
            "tenant_id": str(self.tenant_id),
            "document_id": str(self.document_id),
            "chunk_index": self.chunk_index,
            "chunk_size": self.chunk_size,
            "content": self.content,
            "content_hash": self.content_hash,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_path": self.source_path,
            "processing_status": self.processing_status,
            "processing_error": self.processing_error,
            "embedding_model": self.embedding_model,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "is_processed": self.is_processed,
            "is_pending": self.is_pending,
            "is_failed": self.is_failed,
        }
        
        if include_embedding and self.embedding is not None:
            data["embedding"] = self.embedding.tolist() if hasattr(self.embedding, 'tolist') else list(self.embedding)
        
        return data
    
    @classmethod
    def create_chunk(
        cls,
        tenant_id: uuid.UUID,
        document_id: uuid.UUID,
        chunk_index: int,
        content: str,
        source_type: str,
        source_id: str,
        source_name: str,
        source_path: str = None
    ) -> "DocumentChunk":
        """Cria um novo chunk de documento."""
        import hashlib
        
        # Calcular hash do conteúdo
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        return cls(
            tenant_id=tenant_id,
            document_id=document_id,
            chunk_index=chunk_index,
            chunk_size=len(content),
            content=content,
            content_hash=content_hash,
            source_type=source_type,
            source_id=source_id,
            source_name=source_name,
            source_path=source_path,
            processing_status="pending"
        )
    
    @classmethod
    def get_source_types(cls) -> list[str]:
        """Retorna os tipos de fonte válidos."""
        return ['livro', 'processo', 'jurisprudencia', 'manual', 'faq', 'legislacao', 'doutrina', 'outro']
    
    @classmethod
    def get_processing_statuses(cls) -> list[str]:
        """Retorna os status de processamento válidos."""
        return ['pending', 'processing', 'completed', 'failed'] 