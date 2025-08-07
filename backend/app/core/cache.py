"""
Sistema de cache Redis para FastAPI.
Cache de respostas de chat com TTL configurável.
"""

import json
import hashlib
import logging
from typing import Optional, Any, Dict, Union
from functools import wraps
import pickle
from datetime import datetime, timedelta

import redis
from fastapi import Request, HTTPException
from pydantic import BaseModel

try:
    from app.core.metrics import record_cache_metric
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False

logger = logging.getLogger(__name__)

class CacheConfig:
    """Configuração do cache Redis (EasyUIPanel)."""
    
    def __init__(
        self,
        redis_url: str = None,
        default_ttl: int = 3600,  # 1 hora em segundos
        max_ttl: int = 86400,     # 24 horas em segundos
        min_ttl: int = 60,        # 1 minuto em segundos
        cache_enabled: bool = True,
        cache_prefix: str = "chat_cache"
    ):
        # Usar variável de ambiente ou fallback para localhost
        import os
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.default_ttl = default_ttl
        self.max_ttl = max_ttl
        self.min_ttl = min_ttl
        self.cache_enabled = cache_enabled
        self.cache_prefix = cache_prefix

class RedisCache:
    """Classe para gerenciar cache Redis."""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """Conecta ao Redis."""
        try:
            self.redis_client = redis.from_url(
                self.config.redis_url,
                decode_responses=False,  # Para suportar pickle
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # Testar conexão
            self.redis_client.ping()
            logger.info(f"✅ Conectado ao Redis: {self.config.redis_url}")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao conectar ao Redis: {e}")
            logger.info("🔄 Cache será desabilitado - aplicação continuará funcionando")
            self.redis_client = None
    
    def _generate_cache_key(self, tenant_id: str, agent_id: str, query: str) -> str:
        """
        Gera chave única para cache baseada em tenant, agent e query.
        
        Args:
            tenant_id: ID do tenant
            agent_id: ID do agente
            query: Query/mensagem do usuário
            
        Returns:
            Chave única para cache
        """
        # Normalizar e hash da query para evitar chaves muito longas
        query_hash = hashlib.sha256(query.lower().strip().encode()).hexdigest()[:16]
        
        # Gerar chave estruturada
        cache_key = f"{self.config.cache_prefix}:{tenant_id}:{agent_id}:{query_hash}"
        
        return cache_key
    
    def get_cached_response(
        self, 
        tenant_id: str, 
        agent_id: str, 
        query: str
    ) -> Optional[Dict[str, Any]]:
        """
        Busca resposta cacheada no Redis.
        
        Args:
            tenant_id: ID do tenant
            agent_id: ID do agente
            query: Query/mensagem do usuário
            
        Returns:
            Resposta cacheada ou None se não encontrada
        """
        if not self.config.cache_enabled or not self.redis_client:
            return None
        
        try:
            cache_key = self._generate_cache_key(tenant_id, agent_id, query)
            
            # Buscar no Redis
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                # Deserializar dados
                cached_response = pickle.loads(cached_data)
                
                logger.info(f"🎯 Cache hit: {cache_key}")
                return cached_response
            
            logger.debug(f"❌ Cache miss: {cache_key}")
            return None
            
        except Exception as e:
            logger.warning(f"Erro ao buscar cache (continuando sem cache): {e}")
            return None
    
    def set_cached_response(
        self,
        tenant_id: str,
        agent_id: str,
        query: str,
        response: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """
        Salva resposta no cache Redis.
        
        Args:
            tenant_id: ID do tenant
            agent_id: ID do agente
            query: Query/mensagem do usuário
            response: Resposta para cachear
            ttl: Tempo de vida em segundos (opcional)
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if not self.config.cache_enabled or not self.redis_client:
            return False
        
        try:
            # Validar TTL
            if ttl is None:
                ttl = self.config.default_ttl
            elif ttl > self.config.max_ttl:
                ttl = self.config.max_ttl
            elif ttl < self.config.min_ttl:
                ttl = self.config.min_ttl
            
            cache_key = self._generate_cache_key(tenant_id, agent_id, query)
            
            # Preparar dados para cache
            cache_data = {
                "response": response,
                "tenant_id": tenant_id,
                "agent_id": agent_id,
                "query": query,
                "cached_at": datetime.utcnow().isoformat(),
                "ttl": ttl
            }
            
            # Serializar e salvar
            serialized_data = pickle.dumps(cache_data)
            self.redis_client.setex(cache_key, ttl, serialized_data)
            
            logger.info(f"💾 Cache salvo: {cache_key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.warning(f"Erro ao salvar cache (continuando sem cache): {e}")
            return False
    
    def delete_cached_response(
        self,
        tenant_id: str,
        agent_id: str,
        query: str
    ) -> bool:
        """
        Remove resposta do cache.
        
        Args:
            tenant_id: ID do tenant
            agent_id: ID do agente
            query: Query/mensagem do usuário
            
        Returns:
            True se removeu com sucesso, False caso contrário
        """
        if not self.redis_client:
            return False
        
        try:
            cache_key = self._generate_cache_key(tenant_id, agent_id, query)
            result = self.redis_client.delete(cache_key)
            
            if result:
                logger.info(f"🗑️ Cache removido: {cache_key}")
            
            return bool(result)
            
        except Exception as e:
            logger.warning(f"Erro ao remover cache (continuando sem cache): {e}")
            return False
    
    def clear_tenant_cache(self, tenant_id: str) -> int:
        """
        Remove todo o cache de um tenant.
        
        Args:
            tenant_id: ID do tenant
            
        Returns:
            Número de chaves removidas
        """
        if not self.redis_client:
            return 0
        
        try:
            pattern = f"{self.config.cache_prefix}:{tenant_id}:*"
            keys = self.redis_client.keys(pattern)
            
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"🗑️ Cache do tenant {tenant_id} limpo: {deleted} chaves")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.warning(f"Erro ao limpar cache do tenant (continuando sem cache): {e}")
            return 0
    
    def get_cache_stats(self, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache.
        
        Args:
            tenant_id: ID do tenant (opcional)
            
        Returns:
            Estatísticas do cache
        """
        if not self.redis_client:
            return {"error": "Redis não conectado"}
        
        try:
            if tenant_id:
                pattern = f"{self.config.cache_prefix}:{tenant_id}:*"
            else:
                pattern = f"{self.config.cache_prefix}:*"
            
            keys = self.redis_client.keys(pattern)
            
            stats = {
                "total_keys": len(keys),
                "pattern": pattern,
                "cache_prefix": self.config.cache_prefix
            }
            
            if tenant_id:
                stats["tenant_id"] = tenant_id
            
            # Calcular TTL médio das chaves
            total_ttl = 0
            valid_keys = 0
            
            for key in keys[:100]:  # Limitar a 100 chaves para performance
                ttl = self.redis_client.ttl(key)
                if ttl > 0:
                    total_ttl += ttl
                    valid_keys += 1
            
            if valid_keys > 0:
                stats["avg_ttl"] = total_ttl / valid_keys
                stats["valid_keys_sampled"] = valid_keys
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas do cache: {e}")
            return {"error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde da conexão Redis.
        
        Returns:
            Status da conexão
        """
        if not self.redis_client:
            return {
                "status": "disconnected",
                "error": "Redis client não inicializado"
            }
        
        try:
            # Testar conexão
            self.redis_client.ping()
            
            # Testar operações básicas
            test_key = f"{self.config.cache_prefix}:health_check"
            self.redis_client.setex(test_key, 60, "test")
            value = self.redis_client.get(test_key)
            self.redis_client.delete(test_key)
            
            return {
                "status": "healthy",
                "connection": "ok",
                "operations": "ok",
                "redis_url": self.config.redis_url
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "redis_url": self.config.redis_url
            }

# Instância global do cache
from app.core.config import settings

cache_config = CacheConfig(
    redis_url=settings.redis_url,
    cache_enabled=settings.cache_enabled,
    default_ttl=settings.cache_ttl
)
redis_cache = RedisCache(cache_config)

def cache_response(ttl: Optional[int] = None, key_func: Optional[callable] = None):
    """
    Decorator para cachear respostas de endpoints.
    
    Args:
        ttl: Tempo de vida em segundos (opcional)
        key_func: Função para gerar chave customizada (opcional)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Verificar se cache está habilitado
            if not cache_config.cache_enabled:
                return await func(*args, **kwargs)
            
            # Extrair parâmetros da requisição
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                # Se não encontrar Request nos args, procurar nos kwargs
                request = kwargs.get('request') or kwargs.get('http_request')
            
            if not request:
                logger.warning("Request não encontrada para cache")
                return await func(*args, **kwargs)
            
            # Extrair tenant_id e agent_id
            tenant_id = _extract_tenant_id(request)
            agent_id = _extract_agent_id(request, kwargs)
            query = _extract_query(request, kwargs)
            
            if not all([tenant_id, agent_id, query]):
                logger.debug("Parâmetros insuficientes para cache")
                return await func(*args, **kwargs)
            
            # Gerar chave de cache
            if key_func:
                cache_key = key_func(tenant_id, agent_id, query)
            else:
                cache_key = redis_cache._generate_cache_key(tenant_id, agent_id, query)
            
            # Tentar buscar do cache
            cached_response = redis_cache.get_cached_response(tenant_id, agent_id, query)
            
            if cached_response:
                logger.info(f"🎯 Retornando resposta cacheada para: {cache_key}")
                return cached_response["response"]
            
            # Executar função original
            response = await func(*args, **kwargs)
            
            # Salvar no cache
            if response:
                redis_cache.set_cached_response(
                    tenant_id=tenant_id,
                    agent_id=agent_id,
                    query=query,
                    response=response,
                    ttl=ttl
                )
            
            return response
        
        return wrapper
    return decorator

def _extract_tenant_id(request: Request) -> Optional[str]:
    """Extrai tenant_id da requisição."""
    # Tentar diferentes fontes
    tenant_id = (
        request.headers.get("X-Tenant-ID") or
        request.query_params.get("tenant_id") or
        request.path_params.get("tenant_id")
    )
    
    return tenant_id

def _extract_agent_id(request: Request, kwargs: dict) -> Optional[str]:
    """Extrai agent_id da requisição."""
    # Tentar diferentes fontes
    agent_id = (
        kwargs.get("agent_id") or
        request.query_params.get("agent_id") or
        request.path_params.get("agent_id")
    )
    
    # Se não encontrou, tentar extrair do body
    if not agent_id and hasattr(request, 'body'):
        try:
            body = kwargs.get("request") or {}
            if isinstance(body, dict):
                agent_id = body.get("agent_id")
        except:
            pass
    
    return agent_id

def _extract_query(request: Request, kwargs: dict) -> Optional[str]:
    """Extrai query/mensagem da requisição."""
    # Tentar diferentes fontes
    query = (
        kwargs.get("query") or
        kwargs.get("message") or
        request.query_params.get("query") or
        request.query_params.get("message")
    )
    
    # Se não encontrou, tentar extrair do body
    if not query and hasattr(request, 'body'):
        try:
            body = kwargs.get("request") or {}
            if isinstance(body, dict):
                query = body.get("message") or body.get("query")
        except:
            pass
    
    return query

# Funções utilitárias para uso direto
def get_cached_response(tenant_id: str, agent_id: str, query: str) -> Optional[Dict[str, Any]]:
    """
    Função utilitária para buscar resposta cacheada.
    
    Args:
        tenant_id: ID do tenant
        agent_id: ID do agente
        query: Query/mensagem do usuário
        
    Returns:
        Resposta cacheada ou None
    """
    return redis_cache.get_cached_response(tenant_id, agent_id, query)

def set_cached_response(
    tenant_id: str,
    agent_id: str,
    query: str,
    response: Dict[str, Any],
    ttl: Optional[int] = None
) -> bool:
    """
    Função utilitária para salvar resposta no cache.
    
    Args:
        tenant_id: ID do tenant
        agent_id: ID do agente
        query: Query/mensagem do usuário
        response: Resposta para cachear
        ttl: Tempo de vida em segundos (opcional)
        
    Returns:
        True se salvou com sucesso
    """
    return redis_cache.set_cached_response(tenant_id, agent_id, query, response, ttl)

def clear_tenant_cache(tenant_id: str) -> int:
    """
    Função utilitária para limpar cache de um tenant.
    
    Args:
        tenant_id: ID do tenant
        
    Returns:
        Número de chaves removidas
    """
    return redis_cache.clear_tenant_cache(tenant_id)

def get_cache_stats(tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Função utilitária para obter estatísticas do cache.
    
    Args:
        tenant_id: ID do tenant (opcional)
        
    Returns:
        Estatísticas do cache
    """
    return redis_cache.get_cache_stats(tenant_id)

def cache_health_check() -> Dict[str, Any]:
    """
    Função utilitária para verificar saúde do cache.
    
    Returns:
        Status do cache
    """
    return redis_cache.health_check() 