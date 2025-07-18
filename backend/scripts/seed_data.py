#!/usr/bin/env python3
"""
Script para inserir dados de seed no banco de dados.
Executa: python scripts/seed_data.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Tenant, User, Agent, TenantSettings
from passlib.context import CryptContext
import uuid
import json

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    return pwd_context.hash(password)

def create_tenants(db: Session):
    """Criar tenants de teste"""
    tenants_data = [
        {
            "name": "Empresa ABC Ltda",
            "subdomain": "empresa-abc"
        },
        {
            "name": "Startup XYZ",
            "subdomain": "startup-xyz"
        },
        {
            "name": "Consultoria Legal",
            "subdomain": "consultoria-legal"
        }
    ]
    
    tenants = []
    for data in tenants_data:
        tenant = Tenant(
            id=uuid.uuid4(),
            name=data["name"],
            subdomain=data["subdomain"]
        )
        db.add(tenant)
        tenants.append(tenant)
    
    db.commit()
    print(f"✅ Criados {len(tenants)} tenants")
    return tenants

def create_users(db: Session, tenants):
    """Criar usuários de teste para cada tenant"""
    users_data = [
        {
            "email": "admin@empresa-abc.com",
            "password": "admin123",
            "role": "admin"
        },
        {
            "email": "user@empresa-abc.com", 
            "password": "user123",
            "role": "user"
        },
        {
            "email": "admin@startup-xyz.com",
            "password": "admin123", 
            "role": "admin"
        },
        {
            "email": "dev@startup-xyz.com",
            "password": "dev123",
            "role": "developer"
        },
        {
            "email": "advogado@consultoria-legal.com",
            "password": "adv123",
            "role": "admin"
        }
    ]
    
    # Mapear usuários para tenants
    tenant_users = {
        "empresa-abc": users_data[:2],
        "startup-xyz": users_data[2:4], 
        "consultoria-legal": users_data[4:]
    }
    
    users = []
    for tenant in tenants:
        if tenant.subdomain in tenant_users:
            for user_data in tenant_users[tenant.subdomain]:
                user = User(
                    id=uuid.uuid4(),
                    tenant_id=tenant.id,
                    email=user_data["email"],
                    password_hash=hash_password(user_data["password"]),
                    role=user_data["role"],
                    is_active=True
                )
                db.add(user)
                users.append(user)
    
    db.commit()
    print(f"✅ Criados {len(users)} usuários")
    return users

def create_agents(db: Session, tenants):
    """Criar agentes de teste para cada tenant"""
    agents_data = [
        {
            "name": "LexAI",
            "config": {
                "prompt_template": "Você é um assistente jurídico especializado em direito brasileiro.",
                "kb_filters": ["livros", "jurisprudencia"],
                "temperature": 0.7,
                "max_tokens": 2048
            }
        },
        {
            "name": "FinBot", 
            "config": {
                "prompt_template": "Você é um assistente financeiro especializado em análise de dados.",
                "kb_filters": ["processos", "livros"],
                "temperature": 0.5,
                "max_tokens": 1024
            }
        },
        {
            "name": "SuporteAI",
            "config": {
                "prompt_template": "Você é um assistente de suporte ao cliente.",
                "kb_filters": ["processos"],
                "temperature": 0.8,
                "max_tokens": 1500
            }
        }
    ]
    
    agents = []
    for tenant in tenants:
        for agent_data in agents_data:
            agent = Agent(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=agent_data["name"],
                config=agent_data["config"]
            )
            db.add(agent)
            agents.append(agent)
    
    db.commit()
    print(f"✅ Criados {len(agents)} agentes")
    return agents

def create_tenant_settings(db: Session, tenants):
    """Criar configurações de branding para cada tenant"""
    settings_data = [
        {
            "orchestrator_name": "Assistente Jurídico ABC",
            "theme_primary": "#1a73e8",
            "theme_secondary": "#fbbc04",
            "contact_email": "contato@empresa-abc.com",
            "contact_phone": "(11) 99999-9999"
        },
        {
            "orchestrator_name": "FinBot XYZ",
            "theme_primary": "#34a853", 
            "theme_secondary": "#ea4335",
            "contact_email": "contato@startup-xyz.com",
            "contact_phone": "(21) 88888-8888"
        },
        {
            "orchestrator_name": "Consultor Legal AI",
            "theme_primary": "#8e63ce",
            "theme_secondary": "#ff6b35",
            "contact_email": "contato@consultoria-legal.com", 
            "contact_phone": "(31) 77777-7777"
        }
    ]
    
    settings = []
    for i, tenant in enumerate(tenants):
        if i < len(settings_data):
            setting = TenantSettings(
                tenant_id=tenant.id,
                orchestrator_name=settings_data[i]["orchestrator_name"],
                theme_primary=settings_data[i]["theme_primary"],
                theme_secondary=settings_data[i]["theme_secondary"],
                contact_email=settings_data[i]["contact_email"],
                contact_phone=settings_data[i]["contact_phone"]
            )
            db.add(setting)
            settings.append(setting)
    
    db.commit()
    print(f"✅ Criadas {len(settings)} configurações de tenant")
    return settings

def main():
    """Função principal para executar o seed"""
    print("🌱 Iniciando seed do banco de dados...")
    
    db = SessionLocal()
    try:
        # Criar dados de teste
        tenants = create_tenants(db)
        users = create_users(db, tenants)
        agents = create_agents(db, tenants)
        settings = create_tenant_settings(db, tenants)
        
        print("\n🎉 Seed concluído com sucesso!")
        print(f"📊 Resumo:")
        print(f"   - Tenants: {len(tenants)}")
        print(f"   - Usuários: {len(users)}")
        print(f"   - Agentes: {len(agents)}")
        print(f"   - Configurações: {len(settings)}")
        
        print("\n🔑 Credenciais de teste:")
        print("   - admin@empresa-abc.com / admin123")
        print("   - user@empresa-abc.com / user123")
        print("   - admin@startup-xyz.com / admin123")
        print("   - advogado@consultoria-legal.com / adv123")
        
    except Exception as e:
        print(f"❌ Erro durante o seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 