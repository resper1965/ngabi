"""
Testes para o sistema de cache Redis.
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.cache import (
    RedisCache,
    CacheConfig,
    get_cached_response,
    set_cached_response,
    clear_tenant_cache,
    cache_response
)

client = TestClient(app)

class TestCacheConfig:
    """Testes para configuração do cache."""
    
    def test_cache_config_defaults(self):
        """Testa valores padrão da configuração."""
        config = CacheConfig()
        
        assert config.redis_url == "redis://localhost:6379/0"
        assert config.default_ttl == 3600
        assert config.max_ttl == 86400
        assert config.min_ttl == 60
        assert config.cache_enabled is True
        assert config.cache_prefix == "chat_cache"
    
    def test_cache_config_custom(self):
        """Testa configuração customizada."""
        config = CacheConfig(
            redis_url="redis://test:6379/1",
            default_ttl=1800,
            max_ttl=7200,
            min_ttl=30,
            cache_enabled=False,
            cache_prefix="test_cache"
        )
        
        assert config.redis_url == "redis://test:6379/1"
        assert config.default_ttl == 1800
        assert config.max_ttl == 7200
        assert config.min_ttl == 30
        assert config.cache_enabled is False
        assert config.cache_prefix == "test_cache"

class TestRedisCache:
    """Testes para a classe RedisCache."""
    
    def test_generate_cache_key(self):
        """Testa geração de chave de cache."""
        config = CacheConfig()
        cache = RedisCache(config)
        
        key = cache._generate_cache_key("tenant-123", "agent-456", "Hello world")
        
        assert key.startswith("chat_cache:tenant-123:agent-456:")
        assert len(key.split(":")[-1]) == 16  # Hash de 16 caracteres
    
    def test_generate_cache_key_normalization(self):
        """Testa normalização da query na geração de chave."""
        config = CacheConfig()
        cache = RedisCache(config)
        
        # Queries similares devem gerar a mesma chave
        key1 = cache._generate_cache_key("tenant-123", "agent-456", "Hello World")
        key2 = cache._generate_cache_key("tenant-123", "agent-456", "hello world")
        key3 = cache._generate_cache_key("tenant-123", "agent-456", "  hello world  ")
        
        assert key1 == key2 == key3
    
    @patch('redis.from_url')
    def test_redis_connection_success(self, mock_redis):
        """Testa conexão bem-sucedida com Redis."""
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_redis.return_value = mock_client
        
        config = CacheConfig()
        cache = RedisCache(config)
        
        assert cache.redis_client is not None
        mock_redis.assert_called_once()
        mock_client.ping.assert_called_once()
    
    @patch('redis.from_url')
    def test_redis_connection_failure(self, mock_redis):
        """Testa falha na conexão com Redis."""
        mock_redis.side_effect = Exception("Connection failed")
        
        config = CacheConfig()
        cache = RedisCache(config)
        
        assert cache.redis_client is None

class TestCacheFunctions:
    """Testes para funções utilitárias de cache."""
    
    @patch('app.core.cache.redis_cache')
    def test_get_cached_response(self, mock_cache):
        """Testa função get_cached_response."""
        mock_cache.get_cached_response.return_value = {
            "response": {"message": "cached response"},
            "cached_at": "2024-01-01T00:00:00Z"
        }
        
        result = get_cached_response("tenant-123", "agent-456", "test query")
        
        assert result is not None
        assert result["response"]["message"] == "cached response"
        mock_cache.get_cached_response.assert_called_once_with(
            "tenant-123", "agent-456", "test query"
        )
    
    @patch('app.core.cache.redis_cache')
    def test_set_cached_response(self, mock_cache):
        """Testa função set_cached_response."""
        mock_cache.set_cached_response.return_value = True
        
        response_data = {"message": "test response"}
        result = set_cached_response(
            "tenant-123", "agent-456", "test query", response_data, 1800
        )
        
        assert result is True
        mock_cache.set_cached_response.assert_called_once_with(
            "tenant-123", "agent-456", "test query", response_data, 1800
        )
    
    @patch('app.core.cache.redis_cache')
    def test_clear_tenant_cache(self, mock_cache):
        """Testa função clear_tenant_cache."""
        mock_cache.clear_tenant_cache.return_value = 5
        
        result = clear_tenant_cache("tenant-123")
        
        assert result == 5
        mock_cache.clear_tenant_cache.assert_called_once_with("tenant-123")

class TestCacheDecorator:
    """Testes para o decorator de cache."""
    
    @patch('app.core.cache.redis_cache')
    @patch('app.core.cache.cache_config')
    def test_cache_decorator_hit(self, mock_config, mock_cache):
        """Testa decorator quando há cache hit."""
        mock_config.cache_enabled = True
        mock_cache.get_cached_response.return_value = {
            "response": {"message": "cached response"}
        }
        
        @cache_response(ttl=3600)
        async def test_function(request, **kwargs):
            return {"message": "new response"}
        
        # Mock da requisição
        mock_request = Mock()
        mock_request.headers = {"X-Tenant-ID": "tenant-123"}
        mock_request.query_params = {}
        mock_request.path_params = {}
        
        # Mock dos kwargs
        kwargs = {
            "agent_id": "agent-456",
            "message": "test query"
        }
        
        result = await test_function(mock_request, **kwargs)
        
        assert result["message"] == "cached response"
        mock_cache.get_cached_response.assert_called_once()
        mock_cache.set_cached_response.assert_not_called()
    
    @patch('app.core.cache.redis_cache')
    @patch('app.core.cache.cache_config')
    def test_cache_decorator_miss(self, mock_config, mock_cache):
        """Testa decorator quando há cache miss."""
        mock_config.cache_enabled = True
        mock_cache.get_cached_response.return_value = None
        mock_cache.set_cached_response.return_value = True
        
        @cache_response(ttl=3600)
        async def test_function(request, **kwargs):
            return {"message": "new response"}
        
        # Mock da requisição
        mock_request = Mock()
        mock_request.headers = {"X-Tenant-ID": "tenant-123"}
        mock_request.query_params = {}
        mock_request.path_params = {}
        
        # Mock dos kwargs
        kwargs = {
            "agent_id": "agent-456",
            "message": "test query"
        }
        
        result = await test_function(mock_request, **kwargs)
        
        assert result["message"] == "new response"
        mock_cache.get_cached_response.assert_called_once()
        mock_cache.set_cached_response.assert_called_once()
    
    @patch('app.core.cache.cache_config')
    def test_cache_decorator_disabled(self, mock_config):
        """Testa decorator quando cache está desabilitado."""
        mock_config.cache_enabled = False
        
        @cache_response(ttl=3600)
        async def test_function(request, **kwargs):
            return {"message": "new response"}
        
        # Mock da requisição
        mock_request = Mock()
        mock_request.headers = {"X-Tenant-ID": "tenant-123"}
        
        result = await test_function(mock_request)
        
        assert result["message"] == "new response"

class TestCacheEndpoints:
    """Testes para endpoints de cache."""
    
    def test_cache_health_endpoint(self):
        """Testa endpoint de saúde do cache."""
        with patch('app.core.cache.cache_health_check') as mock_health:
            mock_health.return_value = {
                "status": "healthy",
                "connection": "ok"
            }
            
            response = client.get("/cache/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["connection"] == "ok"
    
    def test_cache_stats_endpoint(self):
        """Testa endpoint de estatísticas do cache."""
        with patch('app.core.cache.get_cache_stats') as mock_stats:
            mock_stats.return_value = {
                "total_keys": 10,
                "avg_ttl": 1800
            }
            
            headers = {"X-Tenant-ID": "test-tenant"}
            response = client.get("/cache/stats", headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_keys"] == 10
            assert data["avg_ttl"] == 1800
    
    def test_cache_clear_endpoint(self):
        """Testa endpoint para limpar cache."""
        with patch('app.core.cache.clear_tenant_cache') as mock_clear:
            mock_clear.return_value = 5
            
            headers = {"X-Tenant-ID": "test-tenant"}
            response = client.delete("/chat/cache/clear", headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert data["deleted_keys"] == 5
            assert data["tenant_id"] == "test-tenant"
    
    def test_cache_clear_endpoint_no_tenant(self):
        """Testa endpoint para limpar cache sem tenant ID."""
        response = client.delete("/chat/cache/clear")
        
        assert response.status_code == 400
        data = response.json()
        assert "Tenant ID é obrigatório" in data["detail"]
    
    def test_cache_test_endpoint(self):
        """Testa endpoint de teste do cache."""
        headers = {"X-Tenant-ID": "test-tenant"}
        request_data = {
            "agent_id": "test-agent",
            "message": "test message"
        }
        
        response = client.post(
            "/chat/cache/test",
            json=request_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "test message"
        assert data["agent_id"] == "test-agent"
        assert data["tenant_id"] == "test-tenant"
        assert data["cached"] is True

class TestCacheIntegration:
    """Testes de integração para cache."""
    
    @patch('app.core.cache.redis_cache')
    def test_chat_endpoint_with_cache(self, mock_cache):
        """Testa endpoint de chat com cache."""
        # Configurar mock para cache miss
        mock_cache.get_cached_response.return_value = None
        mock_cache.set_cached_response.return_value = True
        
        headers = {"X-Tenant-ID": "test-tenant"}
        request_data = {
            "user_id": "test-user",
            "agent_id": "test-agent",
            "message": "Hello, how are you?",
            "chat_mode": "UsoCotidiano"
        }
        
        response = client.post(
            "/api/v1/chat/",
            json=request_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "agent_name" in data
        
        # Verificar se cache foi chamado
        mock_cache.get_cached_response.assert_called_once()
        mock_cache.set_cached_response.assert_called_once()
    
    @patch('app.core.cache.redis_cache')
    def test_chat_endpoint_cache_hit(self, mock_cache):
        """Testa endpoint de chat com cache hit."""
        # Configurar mock para cache hit
        cached_response = {
            "response": {
                "id": "cached-id",
                "message": "Hello, how are you?",
                "response": "I'm doing well, thank you!",
                "agent_name": "Test Agent",
                "chat_mode": "UsoCotidiano",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
        mock_cache.get_cached_response.return_value = cached_response
        
        headers = {"X-Tenant-ID": "test-tenant"}
        request_data = {
            "user_id": "test-user",
            "agent_id": "test-agent",
            "message": "Hello, how are you?",
            "chat_mode": "UsoCotidiano"
        }
        
        response = client.post(
            "/api/v1/chat/",
            json=request_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cached-id"
        assert data["response"] == "I'm doing well, thank you!"
        
        # Verificar que set_cached_response não foi chamado (já estava no cache)
        mock_cache.set_cached_response.assert_not_called()

# Fixtures para testes
@pytest.fixture
def mock_redis_client():
    """Fixture para mock do cliente Redis."""
    with patch('redis.from_url') as mock_redis:
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_redis.return_value = mock_client
        yield mock_client

@pytest.fixture
def cache_config():
    """Fixture para configuração de cache de teste."""
    return CacheConfig(
        redis_url="redis://localhost:6379/1",
        default_ttl=1800,
        cache_enabled=True,
        cache_prefix="test_cache"
    )

@pytest.fixture
def test_tenant_headers():
    """Fixture para headers de tenant de teste."""
    return {"X-Tenant-ID": f"test-tenant-{int(time.time())}"} 