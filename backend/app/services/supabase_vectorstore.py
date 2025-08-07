"""
Supabase Vector Store Service - n.Gabi
Armazenamento de embeddings e RAG no Supabase
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.database import get_supabase
from app.core.config import settings
from app.core.agent_specialists import AgentSpecialists

logger = logging.getLogger(__name__)

class SupabaseVectorStore:
    """Serviço para armazenar embeddings e RAG no Supabase."""
    
    def __init__(self):
        self.supabase = get_supabase()
        self._ensure_tables()
    
    def _ensure_tables(self):
        """Garantir que as tabelas necessárias existam."""
        try:
            # Tabela de embeddings
            self.supabase.rpc('create_embeddings_table', {}).execute()
            logger.info("✅ Tabela de embeddings verificada")
        except Exception as e:
            logger.warning(f"⚠️ Tabela de embeddings pode não existir: {e}")
    
    async def store_documents_for_specialist(
        self,
        specialist_id: str,
        tenant_id: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Armazenar documentos para um especialista no Supabase."""
        try:
            # Verificar se especialista existe
            specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
            if not specialist:
                raise ValueError(f"Especialista não encontrado: {specialist_id}")
            
            # Preparar dados para inserção
            embeddings_data = []
            for i, doc in enumerate(documents):
                embedding_id = str(uuid.uuid4())
                
                embedding_data = {
                    "id": embedding_id,
                    "specialist_id": specialist_id,
                    "tenant_id": tenant_id,
                    "content": doc.get("content", ""),
                    "metadata": doc.get("metadata", {}),
                    "chunk_index": i,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                
                embeddings_data.append(embedding_data)
            
            # Inserir no Supabase
            response = self.supabase.table('embeddings').insert(embeddings_data).execute()
            
            if response.data:
                logger.info(f"✅ {len(embeddings_data)} documentos armazenados para especialista {specialist_id}")
                
                return {
                    "success": True,
                    "specialist_id": specialist_id,
                    "tenant_id": tenant_id,
                    "documents_stored": len(embeddings_data),
                    "embedding_ids": [doc["id"] for doc in embeddings_data],
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                raise Exception("Erro ao inserir embeddings no Supabase")
                
        except Exception as e:
            logger.error(f"❌ Erro ao armazenar documentos para especialista {specialist_id}: {e}")
            raise
    
    async def get_documents_for_specialist(
        self,
        specialist_id: str,
        tenant_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Obter documentos de um especialista do Supabase."""
        try:
            response = self.supabase.table('embeddings')\
                .select('*')\
                .eq('specialist_id', specialist_id)\
                .eq('tenant_id', tenant_id)\
                .order('chunk_index')\
                .limit(limit)\
                .execute()
            
            if response.data:
                logger.info(f"✅ {len(response.data)} documentos recuperados para especialista {specialist_id}")
                return response.data
            else:
                return []
                
        except Exception as e:
            logger.error(f"❌ Erro ao obter documentos para especialista {specialist_id}: {e}")
            raise
    
    async def search_similar_documents(
        self,
        specialist_id: str,
        tenant_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Buscar documentos similares usando RPC do Supabase."""
        try:
            # Usar função RPC para busca de similaridade
            response = self.supabase.rpc(
                'match_embeddings',
                {
                    'query_embedding': query,  # Será convertido para embedding
                    'match_threshold': 0.7,
                    'match_count': limit,
                    'specialist_id': specialist_id,
                    'tenant_id': tenant_id
                }
            ).execute()
            
            if response.data:
                logger.info(f"✅ {len(response.data)} documentos similares encontrados")
                return response.data
            else:
                return []
                
        except Exception as e:
            logger.error(f"❌ Erro ao buscar documentos similares: {e}")
            # Fallback para busca simples
            return await self.get_documents_for_specialist(specialist_id, tenant_id, limit)
    
    async def delete_documents_for_specialist(
        self,
        specialist_id: str,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Deletar documentos de um especialista."""
        try:
            response = self.supabase.table('embeddings')\
                .delete()\
                .eq('specialist_id', specialist_id)\
                .eq('tenant_id', tenant_id)\
                .execute()
            
            logger.info(f"✅ Documentos deletados para especialista {specialist_id}")
            
            return {
                "success": True,
                "specialist_id": specialist_id,
                "tenant_id": tenant_id,
                "documents_deleted": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao deletar documentos para especialista {specialist_id}: {e}")
            raise
    
    async def get_specialist_stats(
        self,
        specialist_id: str,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Obter estatísticas de documentos de um especialista."""
        try:
            # Contar documentos
            count_response = self.supabase.table('embeddings')\
                .select('count', count='exact')\
                .eq('specialist_id', specialist_id)\
                .eq('tenant_id', tenant_id)\
                .execute()
            
            document_count = count_response.count if hasattr(count_response, 'count') else 0
            
            # Obter metadados
            metadata_response = self.supabase.table('embeddings')\
                .select('metadata')\
                .eq('specialist_id', specialist_id)\
                .eq('tenant_id', tenant_id)\
                .limit(1)\
                .execute()
            
            metadata = metadata_response.data[0].get('metadata', {}) if metadata_response.data else {}
            
            return {
                "specialist_id": specialist_id,
                "tenant_id": tenant_id,
                "document_count": document_count,
                "metadata": metadata,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas para especialista {specialist_id}: {e}")
            raise
    
    async def list_specialists_with_documents(self) -> List[Dict[str, Any]]:
        """Listar especialistas que possuem documentos armazenados."""
        try:
            response = self.supabase.table('embeddings')\
                .select('specialist_id, tenant_id, count')\
                .execute()
            
            # Agrupar por especialista e tenant
            specialists = {}
            for row in response.data:
                key = f"{row['specialist_id']}_{row['tenant_id']}"
                if key not in specialists:
                    specialists[key] = {
                        "specialist_id": row['specialist_id'],
                        "tenant_id": row['tenant_id'],
                        "document_count": 1
                    }
                else:
                    specialists[key]["document_count"] += 1
            
            return list(specialists.values())
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar especialistas com documentos: {e}")
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check do Supabase Vector Store."""
        try:
            # Testar conexão
            response = self.supabase.table('embeddings').select('count', count='exact').limit(1).execute()
            
            return {
                "status": "healthy",
                "service": "supabase_vectorstore",
                "connection": "ok",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no health check do Supabase Vector Store: {e}")
            return {
                "status": "unhealthy",
                "service": "supabase_vectorstore",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Instância global do Supabase Vector Store
supabase_vectorstore = SupabaseVectorStore() 