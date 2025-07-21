#!/usr/bin/env python3
"""
Script de seed para popular o banco de dados com dados de exemplo para desenvolvimento.
Conecta ao PostgreSQL usando SQLAlchemy, lê configurações do .env e cria tenants, users e agents.

Execução:
    python scripts/seed.py
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import uuid
from passlib.context import CryptContext

# Adicionar o diretório raiz ao path para importar os modelos
sys.path.append(str(Path(__file__).parent.parent))

from app.models import Tenant, User, Agent, TenantSettings
from app.database import Base

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def load_environment():
    """Carregar variáveis de ambiente do .env"""
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Arquivo .env carregado: {env_path}")
    else:
        print(f"⚠️  Arquivo .env não encontrado: {env_path}")
        print("   Usando variáveis de ambiente do sistema")
    
    return {
        'postgres_url': os.getenv('POSTGRES_URL'),
        'postgres_user': os.getenv('POSTGRES_USER', 'postgres'),
        'postgres_password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'postgres_host': os.getenv('POSTGRES_HOST', 'localhost'),
        'postgres_port': os.getenv('POSTGRES_PORT', '5432'),
        'postgres_db': os.getenv('POSTGRES_DB', 'chat_agents')
    }

def get_database_url(config):
    """Construir URL do banco de dados"""
    if config['postgres_url']:
        return config['postgres_url']
    
    return f"postgresql://{config['postgres_user']}:{config['postgres_password']}@{config['postgres_host']}:{config['postgres_port']}/{config['postgres_db']}"

def create_database_connection(url):
    """Criar conexão com o banco de dados"""
    try:
        engine = create_engine(url, echo=False)
        
        # Testar conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conectado ao PostgreSQL: {version.split(',')[0]}")
        
        return engine
    except SQLAlchemyError as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    return pwd_context.hash(password)

def create_tenants(session):
    """Criar tenants de exemplo"""
    tenants_data = [
        {
            "name": "Empresa ABC Ltda",
            "subdomain": "empresa-abc",
            "description": "Empresa de tecnologia focada em soluções jurídicas"
        },
        {
            "name": "Startup XYZ",
            "subdomain": "startup-xyz", 
            "description": "Startup inovadora em fintech"
        },
        {
            "name": "Consultoria Legal",
            "subdomain": "consultoria-legal",
            "description": "Escritório de advocacia especializado"
        },
        {
            "name": "TechCorp Solutions",
            "subdomain": "techcorp",
            "description": "Corporação de tecnologia global"
        }
    ]
    
    tenants = []
    for data in tenants_data:
        # Verificar se já existe
        existing = session.query(Tenant).filter(Tenant.subdomain == data["subdomain"]).first()
        if existing:
            print(f"   ⏭️  Tenant '{data['name']}' já existe")
            tenants.append(existing)
            continue
        
        tenant = Tenant(
            id=uuid.uuid4(),
            name=data["name"],
            subdomain=data["subdomain"]
        )
        session.add(tenant)
        tenants.append(tenant)
        print(f"   ✅ Tenant criado: {data['name']} ({data['subdomain']})")
    
    session.commit()
    return tenants

def create_users(session, tenants):
    """Criar usuários de exemplo para cada tenant"""
    users_data = [
        # Empresa ABC
        {
            "email": "admin@empresa-abc.com",
            "password": "admin123",
            "role": "admin",
            "name": "Administrador ABC",
            "tenant_subdomain": "empresa-abc"
        },
        {
            "email": "user@empresa-abc.com",
            "password": "user123", 
            "role": "user",
            "name": "Usuário ABC",
            "tenant_subdomain": "empresa-abc"
        },
        {
            "email": "dev@empresa-abc.com",
            "password": "dev123",
            "role": "developer", 
            "name": "Desenvolvedor ABC",
            "tenant_subdomain": "empresa-abc"
        },
        # Startup XYZ
        {
            "email": "admin@startup-xyz.com",
            "password": "admin123",
            "role": "admin",
            "name": "Administrador XYZ",
            "tenant_subdomain": "startup-xyz"
        },
        {
            "email": "dev@startup-xyz.com",
            "password": "dev123",
            "role": "developer",
            "name": "Desenvolvedor XYZ", 
            "tenant_subdomain": "startup-xyz"
        },
        # Consultoria Legal
        {
            "email": "advogado@consultoria-legal.com",
            "password": "adv123",
            "role": "admin",
            "name": "Advogado Principal",
            "tenant_subdomain": "consultoria-legal"
        },
        {
            "email": "assistente@consultoria-legal.com",
            "password": "ass123",
            "role": "user",
            "name": "Assistente Jurídico",
            "tenant_subdomain": "consultoria-legal"
        },
        # TechCorp
        {
            "email": "admin@techcorp.com",
            "password": "admin123",
            "role": "admin",
            "name": "Admin TechCorp",
            "tenant_subdomain": "techcorp"
        }
    ]
    
    users = []
    tenant_map = {t.subdomain: t for t in tenants}
    
    for data in users_data:
        tenant = tenant_map.get(data["tenant_subdomain"])
        if not tenant:
            print(f"   ⚠️  Tenant não encontrado: {data['tenant_subdomain']}")
            continue
        
        # Verificar se usuário já existe
        existing = session.query(User).filter(
            User.tenant_id == tenant.id,
            User.email == data["email"]
        ).first()
        
        if existing:
            print(f"   ⏭️  Usuário '{data['email']}' já existe")
            users.append(existing)
            continue
        
        user = User(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            email=data["email"],
            password_hash=hash_password(data["password"]),
            role=data["role"],
            is_active=True
        )
        session.add(user)
        users.append(user)
        print(f"   ✅ Usuário criado: {data['email']} ({data['role']})")
    
    session.commit()
    return users

def create_agents(session, tenants):
    """Criar agentes de exemplo para cada tenant"""
    agents_data = [
        # Agentes jurídicos
        {
            "name": "LexAI",
            "description": "Assistente jurídico especializado em direito brasileiro",
            "config": {
                "prompt_template": "Você é um assistente jurídico especializado em direito brasileiro. Forneça respostas precisas e baseadas na legislação atual.",
                "kb_filters": ["livros", "jurisprudencia", "legislacao"],
                "temperature": 0.7,
                "max_tokens": 2048,
                "specialization": "direito_civil"
            },
            "tenant_subdomain": "empresa-abc"
        },
        {
            "name": "JurisBot",
            "description": "Assistente para consultoria jurídica",
            "config": {
                "prompt_template": "Você é um assistente jurídico da Consultoria Legal. Ajude com análises de casos e orientações legais.",
                "kb_filters": ["jurisprudencia", "processos", "doutrina"],
                "temperature": 0.6,
                "max_tokens": 1500,
                "specialization": "direito_trabalhista"
            },
            "tenant_subdomain": "consultoria-legal"
        },
        # Agentes financeiros
        {
            "name": "FinBot",
            "description": "Assistente financeiro para análise de dados",
            "config": {
                "prompt_template": "Você é um assistente financeiro especializado em análise de dados e relatórios financeiros.",
                "kb_filters": ["processos", "livros", "relatorios"],
                "temperature": 0.5,
                "max_tokens": 1024,
                "specialization": "analise_financeira"
            },
            "tenant_subdomain": "startup-xyz"
        },
        {
            "name": "InvestAI",
            "description": "Assistente para investimentos e mercado financeiro",
            "config": {
                "prompt_template": "Você é um assistente especializado em investimentos e mercado financeiro. Forneça análises e recomendações.",
                "kb_filters": ["mercado", "investimentos", "analises"],
                "temperature": 0.8,
                "max_tokens": 1800,
                "specialization": "investimentos"
            },
            "tenant_subdomain": "startup-xyz"
        },
        # Agentes de suporte
        {
            "name": "SuporteAI",
            "description": "Assistente de suporte ao cliente",
            "config": {
                "prompt_template": "Você é um assistente de suporte ao cliente. Ajude com dúvidas, problemas e orientações.",
                "kb_filters": ["processos", "faq", "manuais"],
                "temperature": 0.8,
                "max_tokens": 1200,
                "specialization": "suporte_cliente"
            },
            "tenant_subdomain": "techcorp"
        },
        {
            "name": "TechHelper",
            "description": "Assistente técnico para produtos de tecnologia",
            "config": {
                "prompt_template": "Você é um assistente técnico especializado em produtos de tecnologia. Ajude com instalação, configuração e troubleshooting.",
                "kb_filters": ["manuais", "tutoriais", "faq"],
                "temperature": 0.6,
                "max_tokens": 1500,
                "specialization": "suporte_tecnico"
            },
            "tenant_subdomain": "techcorp"
        }
    ]
    
    agents = []
    tenant_map = {t.subdomain: t for t in tenants}
    
    for data in agents_data:
        tenant = tenant_map.get(data["tenant_subdomain"])
        if not tenant:
            print(f"   ⚠️  Tenant não encontrado: {data['tenant_subdomain']}")
            continue
        
        # Verificar se agente já existe
        existing = session.query(Agent).filter(
            Agent.tenant_id == tenant.id,
            Agent.name == data["name"]
        ).first()
        
        if existing:
            print(f"   ⏭️  Agente '{data['name']}' já existe")
            agents.append(existing)
            continue
        
        agent = Agent(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            name=data["name"],
            config=data["config"]
        )
        session.add(agent)
        agents.append(agent)
        print(f"   ✅ Agente criado: {data['name']} ({data['description']})")
    
    session.commit()
    return agents

def create_tenant_settings(session, tenants):
    """Criar configurações de branding para cada tenant"""
    settings_data = [
        {
            "tenant_subdomain": "empresa-abc",
            "orchestrator_name": "Assistente Jurídico ABC",
            "theme_primary": "#1a73e8",
            "theme_secondary": "#fbbc04",
            "contact_email": "contato@empresa-abc.com",
            "contact_phone": "(11) 99999-9999",
            "logo_path": "/logos/empresa-abc.png"
        },
        {
            "tenant_subdomain": "startup-xyz",
            "orchestrator_name": "FinBot XYZ",
            "theme_primary": "#34a853",
            "theme_secondary": "#ea4335",
            "contact_email": "contato@startup-xyz.com",
            "contact_phone": "(21) 88888-8888",
            "logo_path": "/logos/startup-xyz.png"
        },
        {
            "tenant_subdomain": "consultoria-legal",
            "orchestrator_name": "Consultor Legal AI",
            "theme_primary": "#8e63ce",
            "theme_secondary": "#ff6b35",
            "contact_email": "contato@consultoria-legal.com",
            "contact_phone": "(31) 77777-7777",
            "logo_path": "/logos/consultoria-legal.png"
        },
        {
            "tenant_subdomain": "techcorp",
            "orchestrator_name": "TechCorp Assistant",
            "theme_primary": "#000000",
            "theme_secondary": "#00ff00",
            "contact_email": "support@techcorp.com",
            "contact_phone": "(41) 66666-6666",
            "logo_path": "/logos/techcorp.png"
        }
    ]
    
    settings = []
    tenant_map = {t.subdomain: t for t in tenants}
    
    for data in settings_data:
        tenant = tenant_map.get(data["tenant_subdomain"])
        if not tenant:
            print(f"   ⚠️  Tenant não encontrado: {data['tenant_subdomain']}")
            continue
        
        # Verificar se configuração já existe
        existing = session.query(TenantSettings).filter(
            TenantSettings.tenant_id == tenant.id
        ).first()
        
        if existing:
            print(f"   ⏭️  Configurações do tenant '{data['tenant_subdomain']}' já existem")
            settings.append(existing)
            continue
        
        setting = TenantSettings(
            tenant_id=tenant.id,
            logo_path=data["logo_path"],
            orchestrator_name=data["orchestrator_name"],
            theme_primary=data["theme_primary"],
            theme_secondary=data["theme_secondary"],
            contact_email=data["contact_email"],
            contact_phone=data["contact_phone"]
        )
        session.add(setting)
        settings.append(setting)
        print(f"   ✅ Configurações criadas: {data['orchestrator_name']}")
    
    session.commit()
    return settings

def print_summary(tenants, users, agents, settings):
    """Imprimir resumo dos dados criados"""
    print("\n" + "="*60)
    print("📊 RESUMO DOS DADOS CRIADOS")
    print("="*60)
    
    print(f"🏢 Tenants: {len(tenants)}")
    for tenant in tenants:
        print(f"   - {tenant.name} ({tenant.subdomain})")
    
    print(f"\n👤 Usuários: {len(users)}")
    for user in users:
        print(f"   - {user.email} ({user.role})")
    
    print(f"\n🤖 Agentes: {len(agents)}")
    for agent in agents:
        print(f"   - {agent.name}")
    
    print(f"\n🎨 Configurações: {len(settings)}")
    for setting in settings:
        print(f"   - {setting.orchestrator_name}")
    
    print("\n🔑 CREDENCIAIS DE TESTE")
    print("-" * 30)
    test_credentials = [
        ("admin@empresa-abc.com", "admin123", "admin"),
        ("user@empresa-abc.com", "user123", "user"),
        ("admin@startup-xyz.com", "admin123", "admin"),
        ("advogado@consultoria-legal.com", "adv123", "admin"),
        ("admin@techcorp.com", "admin123", "admin")
    ]
    
    for email, password, role in test_credentials:
        print(f"   {email} / {password} ({role})")
    
    print("\n🚀 PRÓXIMOS PASSOS")
    print("-" * 30)
    print("1. Testar conexão com o banco")
    print("2. Executar aplicação FastAPI")
    print("3. Acessar endpoints de autenticação")
    print("4. Testar funcionalidades por tenant")

def main():
    """Função principal"""
    print("🌱 Iniciando seed do banco de dados...")
    print("=" * 60)
    
    # 1. Carregar configurações
    print("📋 Carregando configurações...")
    config = load_environment()
    
    # 2. Conectar ao banco
    print("🔌 Conectando ao banco de dados...")
    db_url = get_database_url(config)
    print(f"   URL: {db_url.replace(config['postgres_password'], '***')}")
    
    engine = create_database_connection(db_url)
    if not engine:
        print("❌ Falha ao conectar ao banco. Verifique as configurações.")
        sys.exit(1)
    
    # 3. Criar sessão
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # 4. Criar dados
        print("\n🏢 Criando tenants...")
        tenants = create_tenants(session)
        
        print("\n👤 Criando usuários...")
        users = create_users(session, tenants)
        
        print("\n🤖 Criando agentes...")
        agents = create_agents(session, tenants)
        
        print("\n🎨 Criando configurações...")
        settings = create_tenant_settings(session, tenants)
        
        # 5. Resumo
        print_summary(tenants, users, agents, settings)
        
        print("\n🎉 Seed concluído com sucesso!")
        
    except SQLAlchemyError as e:
        print(f"❌ Erro durante o seed: {e}")
        session.rollback()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    main() 