"""
Repositório para DocumentChunk com métodos de busca por similaridade usando pgvector.
"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from sqlalchemy.dialects.postgresql import VECTOR
import uuid

from app.repositories.base import BaseRepository
from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    """Repositório para operações com DocumentChunk."""
    
    def __init__(self, db: Session, tenant_id: Optional[str] = None):
        super().__init__(DocumentChunk, db, tenant_id)
    
    def get_by_document_id(self, document_id: uuid.UUID) -> List[DocumentChunk]:
        """Busca todos os chunks de um documento específico."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(self.model.document_id == document_id).order_by(self.model.chunk_index).all()
    
    def get_by_source_type(self, source_type: str) -> List[DocumentChunk]:
        """Busca chunks por tipo de fonte."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(self.model.source_type == source_type).all()
    
    def get_by_processing_status(self, status: str) -> List[DocumentChunk]:
        """Busca chunks por status de processamento."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(self.model.processing_status == status).all()
    
    def get_pending_chunks(self, limit: int = 100) -> List[DocumentChunk]:
        """Busca chunks pendentes de processamento."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(
            self.model.processing_status.in_(["pending", "processing"])
        ).order_by(self.model.created_at).limit(limit).all()
    
    def get_processed_chunks(self) -> List[DocumentChunk]:
        """Busca chunks processados com sucesso."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(
            self.model.processing_status == "completed",
            self.model.embedding.isnot(None)
        ).all()
    
    def get_by_content_hash(self, content_hash: str) -> Optional[DocumentChunk]:
        """Busca chunk por hash do conteúdo (detecção de duplicatas)."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(self.model.content_hash == content_hash).first()
    
    def search_similar_chunks(
        self, 
        embedding: List[float], 
        limit: int = 10, 
        threshold: float = 0.7,
        source_types: Optional[List[str]] = None
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Busca chunks similares usando similaridade de embedding.
        
        Args:
            embedding: Vetor de embedding para comparação
            limit: Número máximo de resultados
            threshold: Limite mínimo de similaridade (0-1)
            source_types: Filtro por tipos de fonte específicos
            
        Returns:
            Lista de tuplas (chunk, similarity_score)
        """
        # Converter lista para vetor PostgreSQL
        embedding_vector = f"[{','.join(map(str, embedding))}]"
        
        # Construir query base
        query = self._add_tenant_filter(self.db.query(self.model))
        query = query.filter(
            self.model.processing_status == "completed",
            self.model.embedding.isnot(None)
        )
        
        # Aplicar filtro de tipos de fonte se especificado
        if source_types:
            query = query.filter(self.model.source_type.in_(source_types))
        
        # Adicionar cálculo de similaridade usando pgvector
        similarity_expr = func.cosine_similarity(self.model.embedding, text(f"'{embedding_vector}'::vector"))
        
        # Filtrar por threshold e ordenar por similaridade
        query = query.filter(similarity_expr >= threshold)
        query = query.order_by(similarity_expr.desc())
        query = query.limit(limit)
        
        # Executar query e retornar resultados com scores
        results = []
        for chunk in query.all():
            # Calcular similaridade para o resultado
            similarity = self._calculate_similarity(chunk.embedding, embedding)
            results.append((chunk, similarity))
        
        return results
    
    def search_similar_chunks_by_source(
        self, 
        embedding: List[float], 
        source_type: str,
        limit: int = 10, 
        threshold: float = 0.7
    ) -> List[Tuple[DocumentChunk, float]]:
        """Busca chunks similares de um tipo de fonte específico."""
        return self.search_similar_chunks(
            embedding=embedding,
            limit=limit,
            threshold=threshold,
            source_types=[source_type]
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos chunks do tenant."""
        query = self._add_tenant_filter(self.db.query(self.model))
        
        stats = {
            "total_chunks": query.count(),
            "processed_chunks": query.filter(
                self.model.processing_status == "completed",
                self.model.embedding.isnot(None)
            ).count(),
            "pending_chunks": query.filter(
                self.model.processing_status.in_(["pending", "processing"])
            ).count(),
            "failed_chunks": query.filter(
                self.model.processing_status == "failed"
            ).count(),
            "by_source_type": {},
            "by_status": {}
        }
        
        # Estatísticas por tipo de fonte
        source_stats = self.db.query(
            self.model.source_type,
            func.count(self.model.id).label('count'),
            func.avg(self.model.chunk_size).label('avg_size')
        ).filter(self.model.tenant_id == self.tenant_id).group_by(self.model.source_type).all()
        
        for source_type, count, avg_size in source_stats:
            stats["by_source_type"][source_type] = {
                "count": count,
                "avg_size": float(avg_size) if avg_size else 0
            }
        
        # Estatísticas por status
        status_stats = self.db.query(
            self.model.processing_status,
            func.count(self.model.id).label('count')
        ).filter(self.model.tenant_id == self.tenant_id).group_by(self.model.processing_status).all()
        
        for status, count in status_stats:
            stats["by_status"][status] = count
        
        return stats
    
    def bulk_create_chunks(self, chunks_data: List[Dict[str, Any]]) -> List[DocumentChunk]:
        """Cria múltiplos chunks de uma vez."""
        chunks = []
        for data in chunks_data:
            chunk = DocumentChunk.create_chunk(
                tenant_id=uuid.UUID(data["tenant_id"]),
                document_id=uuid.UUID(data["document_id"]),
                chunk_index=data["chunk_index"],
                content=data["content"],
                source_type=data["source_type"],
                source_id=data["source_id"],
                source_name=data["source_name"],
                source_path=data.get("source_path")
            )
            chunks.append(chunk)
        
        self.db.add_all(chunks)
        self.db.commit()
        
        # Refresh dos objetos para obter IDs gerados
        for chunk in chunks:
            self.db.refresh(chunk)
        
        return chunks
    
    def update_embedding(self, chunk_id: int, embedding: List[float], model: str = None) -> Optional[DocumentChunk]:
        """Atualiza o embedding de um chunk."""
        chunk = self.get(chunk_id)
        if chunk:
            chunk.mark_as_completed(embedding, model)
            self.db.commit()
            self.db.refresh(chunk)
        return chunk
    
    def mark_as_failed(self, chunk_id: int, error_message: str) -> Optional[DocumentChunk]:
        """Marca um chunk como falhou no processamento."""
        chunk = self.get(chunk_id)
        if chunk:
            chunk.mark_as_failed(error_message)
            self.db.commit()
            self.db.refresh(chunk)
        return chunk
    
    def delete_by_document_id(self, document_id: uuid.UUID) -> int:
        """Remove todos os chunks de um documento."""
        query = self._add_tenant_filter(self.db.query(self.model))
        deleted_count = query.filter(self.model.document_id == document_id).delete()
        self.db.commit()
        return deleted_count
    
    def _calculate_similarity(self, embedding1, embedding2: List[float]) -> float:
        """Calcula similaridade entre dois embeddings."""
        try:
            # Converter para listas se necessário
            if hasattr(embedding1, 'tolist'):
                embedding1 = embedding1.tolist()
            elif hasattr(embedding1, '__iter__'):
                embedding1 = list(embedding1)
            
            # Calcular similaridade de cosseno
            import numpy as np
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Normalizar vetores
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Similaridade de cosseno
            similarity = np.dot(vec1, vec2) / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            # Fallback para cálculo simples
            print(f"Erro ao calcular similaridade: {e}")
            return 0.0
    
    def get_chunks_for_processing(self, batch_size: int = 50) -> List[DocumentChunk]:
        """Busca chunks pendentes para processamento em lote."""
        query = self._add_tenant_filter(self.db.query(self.model))
        return query.filter(
            self.model.processing_status == "pending"
        ).order_by(self.model.created_at).limit(batch_size).all()
    
    def get_duplicate_chunks(self) -> List[Tuple[DocumentChunk, DocumentChunk]]:
        """Busca chunks duplicados baseado no content_hash."""
        query = self._add_tenant_filter(self.db.query(self.model))
        
        # Buscar content_hashes que aparecem mais de uma vez
        duplicate_hashes = self.db.query(
            self.model.content_hash
        ).filter(self.model.tenant_id == self.tenant_id).group_by(
            self.model.content_hash
        ).having(func.count(self.model.id) > 1).all()
        
        duplicates = []
        for (content_hash,) in duplicate_hashes:
            chunks = query.filter(self.model.content_hash == content_hash).all()
            if len(chunks) > 1:
                # Retornar pares de duplicatas
                for i in range(len(chunks) - 1):
                    duplicates.append((chunks[i], chunks[i + 1]))
        
        return duplicates 