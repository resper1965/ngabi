"""
Supabase Retriever - n.Gabi
Retriever customizado para buscar documentos no Supabase
"""

import logging
from typing import List, Dict, Any
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

from app.services.supabase_vectorstore import supabase_vectorstore

logger = logging.getLogger(__name__)

class SupabaseRetriever(BaseRetriever):
    """Retriever customizado para buscar documentos no Supabase."""
    
    def __init__(
        self,
        supabase_vectorstore,
        specialist_id: str,
        tenant_id: str,
        limit: int = 5
    ):
        self.supabase_vectorstore = supabase_vectorstore
        self.specialist_id = specialist_id
        self.tenant_id = tenant_id
        self.limit = limit
    
    async def aget_relevant_documents(self, query: str) -> List[Document]:
        """Buscar documentos relevantes no Supabase."""
        try:
            # Buscar documentos similares no Supabase
            similar_docs = await self.supabase_vectorstore.search_similar_documents(
                specialist_id=self.specialist_id,
                tenant_id=self.tenant_id,
                query=query,
                limit=self.limit
            )
            
            # Converter para documentos LangChain
            documents = []
            for doc in similar_docs:
                document = Document(
                    page_content=doc.get("content", ""),
                    metadata={
                        "id": doc.get("id"),
                        "specialist_id": doc.get("specialist_id"),
                        "tenant_id": doc.get("tenant_id"),
                        "chunk_index": doc.get("chunk_index"),
                        **doc.get("metadata", {})
                    }
                )
                documents.append(document)
            
            logger.info(f"✅ {len(documents)} documentos relevantes encontrados para query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar documentos relevantes: {e}")
            return []
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Versão síncrona para compatibilidade."""
        import asyncio
        
        try:
            # Executar versão assíncrona
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.aget_relevant_documents(query))
        except RuntimeError:
            # Se não há loop ativo, criar um novo
            return asyncio.run(self.aget_relevant_documents(query))
    
    async def aget_relevant_documents_with_scores(self, query: str) -> List[tuple[Document, float]]:
        """Buscar documentos com scores de similaridade."""
        try:
            # Buscar documentos similares no Supabase
            similar_docs = await self.supabase_vectorstore.search_similar_documents(
                specialist_id=self.specialist_id,
                tenant_id=self.tenant_id,
                query=query,
                limit=self.limit
            )
            
            # Converter para documentos com scores
            documents_with_scores = []
            for doc in similar_docs:
                document = Document(
                    page_content=doc.get("content", ""),
                    metadata={
                        "id": doc.get("id"),
                        "specialist_id": doc.get("specialist_id"),
                        "tenant_id": doc.get("tenant_id"),
                        "chunk_index": doc.get("chunk_index"),
                        **doc.get("metadata", {})
                    }
                )
                
                # Score de similaridade (se disponível)
                score = doc.get("similarity", 0.0)
                documents_with_scores.append((document, score))
            
            logger.info(f"✅ {len(documents_with_scores)} documentos com scores encontrados")
            return documents_with_scores
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar documentos com scores: {e}")
            return [] 