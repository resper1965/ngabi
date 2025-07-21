"""
Fixtures de PyTest para testes de integração.
Configura banco de dados de teste, dados de seed e limpeza automática.
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from testcontainers.postgres import PostgresContainer
from dotenv import load_dotenv
import uuid
from passlib.context import CryptContext

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import Base, get_db
from app.models import Tenant, User, Agent, TenantSettings, ChatHistory, Message

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
def postgres_container():
    """Container PostgreSQL para testes usando Testcontainers"""
    with PostgresContainer(
        image="postgres:15-alpine",
        user="test_user",
        password="test_password",
        dbname="test_db"
    ) as container:
        # Aguardar container estar pronto
        container.start()
        yield container

@pytest.fixture(scope="session")
def test_database_url(postgres_container):
    """URL do banco de dados de teste"""
    return postgres_container.get_connection_url()

@pytest.fixture(scope="session")
def test_engine(test_database_url):
    """Engine SQLAlchemy para banco de teste"""
    engine = create_engine(
        test_database_url,
        poolclass=StaticPool,
        echo=False
    )
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Limpar após todos os testes
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def test_session(test_engine) -> Generator[Session, None, None]:
    """Sessão de teste com rollback automático"""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    # Criar sessão com transação
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )
    session = TestingSessionLocal()
    
    yield session
    
    # Rollback e limpeza
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def db_session(test_session):
    """Alias para test_session para compatibilidade"""
    return test_session

@pytest.fixture
def sample_tenant(test_session) -> Tenant:
    """Criar tenant de exemplo para testes"""
    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Company",
        subdomain="test-company"
    )
    test_session.add(tenant)
    test_session.commit()
    test_session.refresh(tenant)
    return tenant

@pytest.fixture
def sample_user(test_session, sample_tenant) -> User:
    """Criar usuário de exemplo para testes"""
    user = User(
        id=uuid.uuid4(),
        tenant_id=sample_tenant.id,
        email="test@example.com",
        password_hash=hash_password("test123"),
        role="admin",
        is_active=True
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user

@pytest.fixture
def sample_agent(test_session, sample_tenant) -> Agent:
    """Criar agente de exemplo para testes"""
    agent = Agent(
        id=uuid.uuid4(),
        tenant_id=sample_tenant.id,
        name="TestAgent",
        config={
            "prompt_template": "You are a test assistant.",
            "kb_filters": ["test"],
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )
    test_session.add(agent)
    test_session.commit()
    test_session.refresh(agent)
    return agent

@pytest.fixture
def sample_tenant_settings(test_session, sample_tenant) -> TenantSettings:
    """Criar configurações de tenant de exemplo"""
    settings = TenantSettings(
        tenant_id=sample_tenant.id,
        orchestrator_name="Test Orchestrator",
        theme_primary="#1a73e8",
        theme_secondary="#fbbc04",
        contact_email="contact@test.com",
        contact_phone="(11) 99999-9999"
    )
    test_session.add(settings)
    test_session.commit()
    test_session.refresh(settings)
    return settings

@pytest.fixture
def sample_chat_history(test_session, sample_tenant, sample_user, sample_agent) -> ChatHistory:
    """Criar histórico de chat de exemplo"""
    chat = ChatHistory(
        tenant_id=sample_tenant.id,
        user_id=sample_user.id,
        agent_id=sample_agent.id,
        message="Hello, how can you help me?",
        response="I'm here to assist you with any questions.",
        chat_mode="UsoCotidiano",
        use_author_voice=False
    )
    test_session.add(chat)
    test_session.commit()
    test_session.refresh(chat)
    return chat

@pytest.fixture
def sample_message(test_session, sample_chat_history) -> Message:
    """Criar mensagem de exemplo"""
    message = Message(
        chat_id=sample_chat_history.id,
        speaker="user",
        content="This is a test message"
    )
    test_session.add(message)
    test_session.commit()
    test_session.refresh(message)
    return message

@pytest.fixture
def seeded_database(test_session):
    """Popular banco com dados de seed para testes de integração"""
    # Dados de seed similares ao script seed.py
    tenants_data = [
        {
            "name": "Test Company A",
            "subdomain": "test-company-a"
        },
        {
            "name": "Test Company B", 
            "subdomain": "test-company-b"
        }
    ]
    
    users_data = [
        {
            "email": "admin@test-company-a.com",
            "password": "admin123",
            "role": "admin",
            "tenant_subdomain": "test-company-a"
        },
        {
            "email": "user@test-company-a.com",
            "password": "user123",
            "role": "user", 
            "tenant_subdomain": "test-company-a"
        },
        {
            "email": "admin@test-company-b.com",
            "password": "admin123",
            "role": "admin",
            "tenant_subdomain": "test-company-b"
        }
    ]
    
    agents_data = [
        {
            "name": "TestAgent A",
            "config": {
                "prompt_template": "You are TestAgent A.",
                "kb_filters": ["test"],
                "temperature": 0.7
            },
            "tenant_subdomain": "test-company-a"
        },
        {
            "name": "TestAgent B",
            "config": {
                "prompt_template": "You are TestAgent B.",
                "kb_filters": ["test"],
                "temperature": 0.8
            },
            "tenant_subdomain": "test-company-b"
        }
    ]
    
    # Criar tenants
    tenants = {}
    for data in tenants_data:
        tenant = Tenant(
            id=uuid.uuid4(),
            name=data["name"],
            subdomain=data["subdomain"]
        )
        test_session.add(tenant)
        tenants[data["subdomain"]] = tenant
    
    test_session.commit()
    
    # Criar usuários
    users = {}
    for data in users_data:
        tenant = tenants.get(data["tenant_subdomain"])
        if tenant:
            user = User(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                email=data["email"],
                password_hash=hash_password(data["password"]),
                role=data["role"],
                is_active=True
            )
            test_session.add(user)
            users[data["email"]] = user
    
    test_session.commit()
    
    # Criar agentes
    agents = {}
    for data in agents_data:
        tenant = tenants.get(data["tenant_subdomain"])
        if tenant:
            agent = Agent(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=data["name"],
                config=data["config"]
            )
            test_session.add(agent)
            agents[data["name"]] = agent
    
    test_session.commit()
    
    # Criar configurações
    settings_data = [
        {
            "tenant_subdomain": "test-company-a",
            "orchestrator_name": "Test Orchestrator A",
            "theme_primary": "#1a73e8",
            "theme_secondary": "#fbbc04"
        },
        {
            "tenant_subdomain": "test-company-b", 
            "orchestrator_name": "Test Orchestrator B",
            "theme_primary": "#34a853",
            "theme_secondary": "#ea4335"
        }
    ]
    
    for data in settings_data:
        tenant = tenants.get(data["tenant_subdomain"])
        if tenant:
            settings = TenantSettings(
                tenant_id=tenant.id,
                orchestrator_name=data["orchestrator_name"],
                theme_primary=data["theme_primary"],
                theme_secondary=data["theme_secondary"]
            )
            test_session.add(settings)
    
    test_session.commit()
    
    return {
        "tenants": tenants,
        "users": users,
        "agents": agents
    }

@pytest.fixture
def test_app(test_engine):
    """Aplicação FastAPI para testes"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    # Substituir dependência do banco
    def override_get_db():
        try:
            TestingSessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=test_engine
            )
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Limpar override
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(test_session, seeded_database):
    """Headers de autenticação para testes"""
    # Usar o primeiro usuário admin disponível
    admin_user = None
    for user in seeded_database["users"].values():
        if user.role == "admin":
            admin_user = user
            break
    
    if not admin_user:
        pytest.skip("Nenhum usuário admin encontrado nos dados de seed")
    
    # Aqui você implementaria a lógica de geração de JWT
    # Por enquanto, retornamos headers básicos
    return {
        "Authorization": f"Bearer test_token_{admin_user.id}",
        "Content-Type": "application/json"
    }

@pytest.fixture
def tenant_headers(test_session, seeded_database):
    """Headers com tenant específico"""
    # Usar o primeiro tenant disponível
    tenant = list(seeded_database["tenants"].values())[0]
    
    return {
        "X-Tenant-ID": str(tenant.id),
        "Content-Type": "application/json"
    }

# Factories para criar dados de teste
@pytest.fixture
def tenant_factory(test_session):
    """Factory para criar tenants"""
    def _create_tenant(name="Test Tenant", subdomain=None):
        if subdomain is None:
            subdomain = f"test-{uuid.uuid4().hex[:8]}"
        
        tenant = Tenant(
            id=uuid.uuid4(),
            name=name,
            subdomain=subdomain
        )
        test_session.add(tenant)
        test_session.commit()
        test_session.refresh(tenant)
        return tenant
    
    return _create_tenant

@pytest.fixture
def user_factory(test_session):
    """Factory para criar usuários"""
    def _create_user(tenant_id, email=None, role="user"):
        if email is None:
            email = f"user-{uuid.uuid4().hex[:8]}@test.com"
        
        user = User(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            email=email,
            password_hash=hash_password("test123"),
            role=role,
            is_active=True
        )
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)
        return user
    
    return _create_user

@pytest.fixture
def agent_factory(test_session):
    """Factory para criar agentes"""
    def _create_agent(tenant_id, name=None):
        if name is None:
            name = f"agent-{uuid.uuid4().hex[:8]}"
        
        agent = Agent(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            name=name,
            config={
                "prompt_template": f"You are {name}.",
                "kb_filters": ["test"],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )
        test_session.add(agent)
        test_session.commit()
        test_session.refresh(agent)
        return agent
    
    return _create_agent

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

def pytest_collection_modifyitems(config, items):
    """Modificar itens de teste automaticamente"""
    for item in items:
        # Marcar testes em tests/ como integration por padrão
        if "tests/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Marcar testes com "test_" como unit por padrão
        if item.name.startswith("test_"):
            item.add_marker(pytest.mark.unit) 