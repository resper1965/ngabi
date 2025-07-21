"""
Testes para o sistema de rate limiting.
"""

import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.core.rate_limiting import (
    get_tenant_id_from_request,
    get_tenant_key,
    get_user_key,
    rate_limit_by_tenant,
    rate_limit_by_user
)

client = TestClient(app)

class TestRateLimiting:
    """Testes para funcionalidades de rate limiting."""
    
    def test_get_tenant_id_from_header(self):
        """Testa extração de tenant_id do header."""
        from fastapi import Request
        from unittest.mock import Mock
        
        # Mock da requisição
        request = Mock()
        request.headers = {"X-Tenant-ID": "test-tenant-123"}
        request.query_params = {}
        request.path_params = {}
        
        tenant_id = get_tenant_id_from_request(request)
        assert tenant_id == "test-tenant-123"
    
    def test_get_tenant_id_from_query(self):
        """Testa extração de tenant_id do query parameter."""
        from fastapi import Request
        from unittest.mock import Mock
        
        # Mock da requisição
        request = Mock()
        request.headers = {}
        request.query_params = {"tenant_id": "test-tenant-456"}
        request.path_params = {}
        
        tenant_id = get_tenant_id_from_request(request)
        assert tenant_id == "test-tenant-456"
    
    def test_get_tenant_id_fallback_to_ip(self):
        """Testa fallback para IP quando tenant_id não está disponível."""
        from fastapi import Request
        from unittest.mock import Mock
        
        # Mock da requisição
        request = Mock()
        request.headers = {}
        request.query_params = {}
        request.path_params = {}
        request.client.host = "192.168.1.1"
        
        with patch('app.core.rate_limiting.get_remote_address', return_value="192.168.1.1"):
            tenant_id = get_tenant_id_from_request(request)
            assert tenant_id == "192.168.1.1"
    
    def test_get_tenant_key(self):
        """Testa geração de chave para tenant."""
        from fastapi import Request
        from unittest.mock import Mock
        
        # Mock da requisição
        request = Mock()
        request.headers = {"X-Tenant-ID": "test-tenant"}
        request.query_params = {}
        request.path_params = {}
        
        key = get_tenant_key(request)
        assert key == "tenant:test-tenant"
    
    def test_get_user_key(self):
        """Testa geração de chave para usuário."""
        from fastapi import Request
        from unittest.mock import Mock
        
        # Mock da requisição
        request = Mock()
        request.headers = {"X-Tenant-ID": "test-tenant", "X-User-ID": "user-123"}
        request.query_params = {}
        request.path_params = {}
        
        key = get_user_key(request)
        assert key == "user:test-tenant:user-123"

class TestRateLimitEndpoints:
    """Testes para endpoints com rate limiting."""
    
    def test_chat_endpoint_rate_limit(self):
        """Testa rate limiting no endpoint de chat."""
        headers = {"X-Tenant-ID": "test-tenant-123"}
        
        # Fazer 10 requisições (limite por minuto)
        for i in range(10):
            response = client.post(
                "/api/v1/chat/test-rate-limit",
                headers=headers
            )
            assert response.status_code == 200
        
        # A 11ª requisição deve falhar
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=headers
        )
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["error"]
    
    def test_different_tenants_separate_limits(self):
        """Testa que diferentes tenants têm limites separados."""
        headers_tenant_1 = {"X-Tenant-ID": "tenant-1"}
        headers_tenant_2 = {"X-Tenant-ID": "tenant-2"}
        
        # Tenant 1: 10 requisições
        for i in range(10):
            response = client.post(
                "/api/v1/chat/test-rate-limit",
                headers=headers_tenant_1
            )
            assert response.status_code == 200
        
        # Tenant 1: 11ª requisição deve falhar
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=headers_tenant_1
        )
        assert response.status_code == 429
        
        # Tenant 2: ainda pode fazer 10 requisições
        for i in range(10):
            response = client.post(
                "/api/v1/chat/test-rate-limit",
                headers=headers_tenant_2
            )
            assert response.status_code == 200
    
    def test_user_rate_limit(self):
        """Testa rate limiting por usuário."""
        headers = {
            "X-Tenant-ID": "test-tenant",
            "X-User-ID": "user-123"
        }
        
        # Fazer 5 requisições (limite por usuário)
        for i in range(5):
            response = client.get(
                "/api/v1/test/user-limit",
                headers=headers
            )
            assert response.status_code == 200
        
        # A 6ª requisição deve falhar
        response = client.get(
            "/api/v1/test/user-limit",
            headers=headers
        )
        assert response.status_code == 429
    
    def test_stream_endpoint_lower_limit(self):
        """Testa que endpoint de stream tem limite menor."""
        headers = {"X-Tenant-ID": "test-tenant"}
        
        # Fazer 5 requisições (limite do stream)
        for i in range(5):
            response = client.post(
                "/api/v1/chat/stream",
                json={"message": "test"},
                headers=headers
            )
            assert response.status_code == 200
        
        # A 6ª requisição deve falhar
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": "test"},
            headers=headers
        )
        assert response.status_code == 429
    
    def test_batch_endpoint_very_low_limit(self):
        """Testa que endpoint de batch tem limite muito baixo."""
        headers = {"X-Tenant-ID": "test-tenant"}
        
        # Fazer 2 requisições (limite do batch)
        for i in range(2):
            response = client.post(
                "/api/v1/chat/batch",
                json=[{"message": "test"}],
                headers=headers
            )
            assert response.status_code == 200
        
        # A 3ª requisição deve falhar
        response = client.post(
            "/api/v1/chat/batch",
            json=[{"message": "test"}],
            headers=headers
        )
        assert response.status_code == 429

class TestRateLimitRecovery:
    """Testes para recuperação após rate limiting."""
    
    def test_rate_limit_reset_after_window(self):
        """Testa que rate limit é resetado após a janela de tempo."""
        headers = {"X-Tenant-ID": "test-tenant-recovery"}
        
        # Fazer 10 requisições (limite)
        for i in range(10):
            response = client.post(
                "/api/v1/chat/test-rate-limit",
                headers=headers
            )
            assert response.status_code == 200
        
        # 11ª deve falhar
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=headers
        )
        assert response.status_code == 429
        
        # Simular passagem do tempo (em produção, aguardar 1 minuto)
        # Aqui vamos mockar o tempo para testar
        with patch('time.time') as mock_time:
            # Simular que passou 1 minuto
            mock_time.return_value = time.time() + 61
            
            # Agora deve funcionar novamente
            response = client.post(
                "/api/v1/chat/test-rate-limit",
                headers=headers
            )
            assert response.status_code == 200

class TestRateLimitHeaders:
    """Testes para headers de rate limiting."""
    
    def test_rate_limit_headers_in_response(self):
        """Testa que headers de rate limiting estão na resposta."""
        headers = {"X-Tenant-ID": "test-tenant-headers"}
        
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=headers
        )
        
        assert response.status_code == 200
        assert "X-Rate-Limit-Tenant" in response.headers
        assert "X-Process-Time" in response.headers
        assert response.headers["X-Rate-Limit-Tenant"] == "test-tenant-headers"
    
    def test_retry_after_header_on_limit_exceeded(self):
        """Testa header Retry-After quando limite é excedido."""
        headers = {"X-Tenant-ID": "test-tenant-retry"}
        
        # Exceder o limite
        for i in range(10):
            client.post("/api/v1/chat/test-rate-limit", headers=headers)
        
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=headers
        )
        
        assert response.status_code == 429
        assert "Retry-After" in response.headers

class TestRateLimitConfiguration:
    """Testes para configuração de rate limiting."""
    
    def test_conditional_rate_limit_enabled(self):
        """Testa rate limiting condicional quando habilitado."""
        headers = {"X-Tenant-ID": "test-tenant-conditional"}
        
        # Fazer 3 requisições (limite condicional)
        for i in range(3):
            response = client.get(
                "/api/v1/test/conditional-limit",
                headers=headers
            )
            assert response.status_code == 200
        
        # 4ª deve falhar
        response = client.get(
            "/api/v1/test/conditional-limit",
            headers=headers
        )
        assert response.status_code == 429
    
    def test_rate_limit_stats_endpoint(self):
        """Testa endpoint de estatísticas de rate limiting."""
        headers = {"X-Tenant-ID": "test-tenant-stats"}
        
        response = client.get(
            "/api/v1/chat/rate-limit-stats",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "tenant_id" in data
        assert "client_ip" in data
        assert "current_limits" in data
        assert data["tenant_id"] == "test-tenant-stats"

class TestRateLimitErrorHandling:
    """Testes para tratamento de erros de rate limiting."""
    
    def test_rate_limit_exceeded_error_format(self):
        """Testa formato do erro quando rate limit é excedido."""
        headers = {"X-Tenant-ID": "test-tenant-error"}
        
        # Exceder o limite
        for i in range(10):
            client.post("/api/v1/chat/test-rate-limit", headers=headers)
        
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=headers
        )
        
        assert response.status_code == 429
        error_data = response.json()
        
        assert "error" in error_data
        assert "message" in error_data
        assert "retry_after" in error_data
        assert "tenant_id" in error_data
        assert "endpoint" in error_data
        assert error_data["error"] == "Rate limit exceeded"
    
    def test_rate_limit_without_tenant_id(self):
        """Testa rate limiting quando tenant_id não está disponível."""
        # Fazer requisição sem tenant_id (deve usar IP como fallback)
        response = client.post("/api/v1/chat/test-rate-limit")
        
        # Deve funcionar, mas usar IP como identificador
        assert response.status_code == 200
        data = response.json()
        assert "tenant_id" in data
        # O tenant_id deve ser o IP do cliente

# Fixtures para testes
@pytest.fixture
def test_tenant_headers():
    """Fixture para headers de tenant de teste."""
    return {"X-Tenant-ID": f"test-tenant-{int(time.time())}"}

@pytest.fixture
def test_user_headers():
    """Fixture para headers de usuário de teste."""
    return {
        "X-Tenant-ID": f"test-tenant-{int(time.time())}",
        "X-User-ID": f"user-{int(time.time())}"
    }

# Testes de integração
class TestRateLimitIntegration:
    """Testes de integração para rate limiting."""
    
    def test_full_chat_flow_with_rate_limiting(self, test_tenant_headers):
        """Testa fluxo completo de chat com rate limiting."""
        # Simular requisições de chat
        chat_data = {
            "user_id": "test-user",
            "agent_id": "test-agent",
            "message": "Hello, how are you?",
            "chat_mode": "UsoCotidiano"
        }
        
        # Fazer 10 requisições (limite)
        for i in range(10):
            response = client.post(
                "/api/v1/chat/",
                json=chat_data,
                headers=test_tenant_headers
            )
            assert response.status_code == 200
        
        # 11ª deve falhar
        response = client.post(
            "/api/v1/chat/",
            json=chat_data,
            headers=test_tenant_headers
        )
        assert response.status_code == 429
    
    def test_multiple_endpoints_same_tenant(self, test_tenant_headers):
        """Testa que diferentes endpoints têm limites separados para o mesmo tenant."""
        # Testar chat normal
        for i in range(10):
            response = client.post(
                "/api/v1/chat/test-rate-limit",
                headers=test_tenant_headers
            )
            assert response.status_code == 200
        
        # Chat normal deve falhar
        response = client.post(
            "/api/v1/chat/test-rate-limit",
            headers=test_tenant_headers
        )
        assert response.status_code == 429
        
        # Mas stream ainda deve funcionar (limite separado)
        for i in range(5):
            response = client.post(
                "/api/v1/chat/stream",
                json={"message": "test"},
                headers=test_tenant_headers
            )
            assert response.status_code == 200 