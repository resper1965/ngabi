"""
Fixtures de PyTest para testes de integração com Supabase.
Configura Supabase de teste, dados de seed e limpeza automática.
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path
from typing import Generator, AsyncGenerator
from dotenv import load_dotenv
import uuid
from passlib.context import CryptContext

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import get_supabase

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    return pwd_context.hash(password)

@pytest.fixture(scope="session")
def event_loop():
    """Criar event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def supabase_client():
    """Cliente Supabase para testes"""
    # Carregar variáveis de ambiente de teste
    load_dotenv(".env.test", override=True)
    
    try:
        client = get_supabase()
        return client
    except Exception as e:
        pytest.skip(f"Supabase não configurado para testes: {e}")

@pytest.fixture
def test_tenant_id():
    """ID de tenant para testes"""
    return str(uuid.uuid4())

@pytest.fixture
def test_user_id():
    """ID de usuário para testes"""
    return str(uuid.uuid4())

@pytest.fixture
def test_agent_id():
    """ID de agente para testes"""
    return str(uuid.uuid4())

@pytest.fixture
def sample_tenant_data(test_tenant_id):
    """Dados de tenant de exemplo"""
    return {
        "id": test_tenant_id,
        "name": "Test Company",
        "domain": "test-company",
        "settings": {"theme": "default"},
        "is_active": True
    }

@pytest.fixture
def sample_user_data(test_user_id, test_tenant_id):
    """Dados de usuário de exemplo"""
    return {
        "id": test_user_id,
        "tenant_id": test_tenant_id,
        "email": "test@example.com",
        "name": "Test User",
        "role": "user",
        "is_active": True
    }

@pytest.fixture
def sample_agent_data(test_agent_id, test_tenant_id):
    """Dados de agente de exemplo"""
    return {
        "id": test_agent_id,
        "tenant_id": test_tenant_id,
        "name": "TestAgent",
        "description": "Test agent for testing",
        "system_prompt": "You are a test assistant.",
        "model": "gpt-3.5-turbo",
        "is_active": True
    }

@pytest.fixture
def seeded_database(supabase_client, sample_tenant_data, sample_user_data, sample_agent_data):
    """Popular banco com dados de seed para testes de integração"""
    try:
        # Inserir tenant
        tenant_response = supabase_client.table('tenants').insert(sample_tenant_data).execute()
        
        # Inserir usuário
        user_response = supabase_client.table('users').insert(sample_user_data).execute()
        
        # Inserir agente
        agent_response = supabase_client.table('agents').insert(sample_agent_data).execute()
        
        return {
            "tenant": tenant_response.data[0] if tenant_response.data else None,
            "user": user_response.data[0] if user_response.data else None,
            "agent": agent_response.data[0] if agent_response.data else None
        }
    except Exception as e:
        pytest.skip(f"Erro ao popular banco de teste: {e}")

@pytest.fixture
def test_app(supabase_client):
    """Aplicação FastAPI para testes"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    with TestClient(app) as client:
        yield client

@pytest.fixture
def auth_headers(seeded_database):
    """Headers de autenticação para testes"""
    if not seeded_database.get("user"):
        pytest.skip("Usuário de teste não encontrado")
    
    return {
        "Authorization": f"Bearer test_token_{seeded_database['user']['id']}",
        "Content-Type": "application/json"
    }

@pytest.fixture
def tenant_headers(seeded_database):
    """Headers com tenant específico"""
    if not seeded_database.get("tenant"):
        pytest.skip("Tenant de teste não encontrado")
    
    return {
        "X-Tenant-ID": seeded_database["tenant"]["id"],
        "Content-Type": "application/json"
    }

# Configurações de pytest
def pytest_configure(config):
    """Configurações globais do pytest"""
    # Configurar markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "supabase: mark test as requiring Supabase"
    )

def pytest_collection_modifyitems(config, items):
    """Modificar itens de teste automaticamente"""
    for item in items:
        # Marcar testes em tests/ como integration por padrão
        if "tests/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Marcar testes com "test_" como unit por padrão
        if item.name.startswith("test_"):
            item.add_marker(pytest.mark.unit)
        
        # Marcar testes que usam Supabase
        if any(marker in str(item.fspath) for marker in ["supabase", "integration"]):
            item.add_marker(pytest.mark.supabase) 