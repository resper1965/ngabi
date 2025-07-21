"""
Exemplos de testes demonstrando o uso das fixtures do conftest.py
"""

import pytest
from sqlalchemy.orm import Session
from app.models import Tenant, User, Agent, TenantSettings

class TestDatabaseFixtures:
    """Testes demonstrando fixtures de banco de dados"""
    
    def test_sample_tenant(self, sample_tenant):
        """Teste com fixture de tenant de exemplo"""
        assert sample_tenant.name == "Test Company"
        assert sample_tenant.subdomain == "test-company"
        assert sample_tenant.id is not None
    
    def test_sample_user(self, sample_user, sample_tenant):
        """Teste com fixture de usuário de exemplo"""
        assert sample_user.email == "test@example.com"
        assert sample_user.role == "admin"
        assert sample_user.tenant_id == sample_tenant.id
        assert sample_user.is_active is True
    
    def test_sample_agent(self, sample_agent, sample_tenant):
        """Teste com fixture de agente de exemplo"""
        assert sample_agent.name == "TestAgent"
        assert sample_agent.tenant_id == sample_tenant.id
        assert "prompt_template" in sample_agent.config
        assert sample_agent.config["temperature"] == 0.7
    
    def test_sample_tenant_settings(self, sample_tenant_settings, sample_tenant):
        """Teste com fixture de configurações de tenant"""
        assert sample_tenant_settings.tenant_id == sample_tenant.id
        assert sample_tenant_settings.orchestrator_name == "Test Orchestrator"
        assert sample_tenant_settings.theme_primary == "#1a73e8"
        assert sample_tenant_settings.theme_secondary == "#fbbc04"

class TestSeededDatabase:
    """Testes com banco populado com dados de seed"""
    
    def test_seeded_tenants(self, seeded_database):
        """Teste verificando tenants criados pelo seed"""
        tenants = seeded_database["tenants"]
        assert len(tenants) == 2
        
        # Verificar tenants específicos
        assert "test-company-a" in tenants
        assert "test-company-b" in tenants
        
        tenant_a = tenants["test-company-a"]
        assert tenant_a.name == "Test Company A"
    
    def test_seeded_users(self, seeded_database):
        """Teste verificando usuários criados pelo seed"""
        users = seeded_database["users"]
        assert len(users) == 3
        
        # Verificar usuários específicos
        assert "admin@test-company-a.com" in users
        assert "user@test-company-a.com" in users
        assert "admin@test-company-b.com" in users
        
        admin_user = users["admin@test-company-a.com"]
        assert admin_user.role == "admin"
    
    def test_seeded_agents(self, seeded_database):
        """Teste verificando agentes criados pelo seed"""
        agents = seeded_database["agents"]
        assert len(agents) == 2
        
        # Verificar agentes específicos
        assert "TestAgent A" in agents
        assert "TestAgent B" in agents
        
        agent_a = agents["TestAgent A"]
        assert agent_a.config["prompt_template"] == "You are TestAgent A."

class TestFactories:
    """Testes demonstrando uso de factories"""
    
    def test_tenant_factory(self, tenant_factory):
        """Teste usando factory de tenant"""
        tenant = tenant_factory(name="Custom Tenant", subdomain="custom")
        assert tenant.name == "Custom Tenant"
        assert tenant.subdomain == "custom"
    
    def test_user_factory(self, tenant_factory, user_factory):
        """Teste usando factory de usuário"""
        tenant = tenant_factory()
        user = user_factory(tenant_id=tenant.id, email="custom@test.com", role="developer")
        
        assert user.email == "custom@test.com"
        assert user.role == "developer"
        assert user.tenant_id == tenant.id
    
    def test_agent_factory(self, tenant_factory, agent_factory):
        """Teste usando factory de agente"""
        tenant = tenant_factory()
        agent = agent_factory(tenant_id=tenant.id, name="CustomAgent")
        
        assert agent.name == "CustomAgent"
        assert agent.tenant_id == tenant.id
        assert agent.config["prompt_template"] == "You are CustomAgent."

class TestDatabaseIsolation:
    """Testes verificando isolamento entre testes"""
    
    def test_database_isolation_1(self, test_session):
        """Primeiro teste - criar dados"""
        tenant = Tenant(
            id=pytest.importorskip("uuid").uuid4(),
            name="Isolation Test 1",
            subdomain="isolation-1"
        )
        test_session.add(tenant)
        test_session.commit()
        
        # Verificar que foi criado
        assert test_session.query(Tenant).filter_by(subdomain="isolation-1").first() is not None
    
    def test_database_isolation_2(self, test_session):
        """Segundo teste - verificar que dados do teste anterior não existem"""
        # O rollback automático deve ter removido os dados do teste anterior
        tenant = test_session.query(Tenant).filter_by(subdomain="isolation-1").first()
        assert tenant is None

class TestFastAPIApp:
    """Testes da aplicação FastAPI"""
    
    def test_health_endpoint(self, test_app):
        """Teste do endpoint de health"""
        response = test_app.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_app_with_database(self, test_app, seeded_database):
        """Teste da aplicação com banco populado"""
        # Aqui você testaria endpoints que dependem do banco
        # Por exemplo, listar tenants, usuários, etc.
        pass

class TestAuthentication:
    """Testes de autenticação"""
    
    def test_auth_headers(self, auth_headers):
        """Teste dos headers de autenticação"""
        assert "Authorization" in auth_headers
        assert auth_headers["Authorization"].startswith("Bearer ")
        assert auth_headers["Content-Type"] == "application/json"
    
    def test_tenant_headers(self, tenant_headers):
        """Teste dos headers de tenant"""
        assert "X-Tenant-ID" in tenant_headers
        assert tenant_headers["Content-Type"] == "application/json"

# Testes com markers personalizados
@pytest.mark.slow
def test_slow_operation():
    """Teste marcado como lento"""
    import time
    time.sleep(0.1)  # Simular operação lenta
    assert True

@pytest.mark.integration
def test_integration_with_database(test_session):
    """Teste de integração com banco"""
    # Este teste será marcado automaticamente como integration
    assert test_session is not None

@pytest.mark.unit
def test_unit_function():
    """Teste unitário simples"""
    # Este teste será marcado automaticamente como unit
    result = 2 + 2
    assert result == 4

# Testes parametrizados
@pytest.mark.parametrize("role,expected_active", [
    ("admin", True),
    ("user", True),
    ("developer", True),
])
def test_user_roles(user_factory, tenant_factory, role, expected_active):
    """Teste parametrizado para diferentes roles de usuário"""
    tenant = tenant_factory()
    user = user_factory(tenant_id=tenant.id, role=role)
    
    assert user.role == role
    assert user.is_active == expected_active

# Testes com fixtures aninhadas
def test_complex_scenario(tenant_factory, user_factory, agent_factory):
    """Teste com múltiplas fixtures"""
    # Criar tenant
    tenant = tenant_factory(name="Complex Test Company")
    
    # Criar múltiplos usuários
    admin = user_factory(tenant_id=tenant.id, role="admin")
    user1 = user_factory(tenant_id=tenant.id, role="user")
    user2 = user_factory(tenant_id=tenant.id, role="user")
    
    # Criar agente
    agent = agent_factory(tenant_id=tenant.id, name="ComplexAgent")
    
    # Verificações
    assert admin.role == "admin"
    assert user1.role == "user"
    assert user2.role == "user"
    assert agent.tenant_id == tenant.id
    
    # Verificar que todos pertencem ao mesmo tenant
    assert admin.tenant_id == user1.tenant_id == user2.tenant_id == agent.tenant_id 