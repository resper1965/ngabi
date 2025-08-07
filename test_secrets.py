#!/usr/bin/env python3
"""
Script para testar a configuração de secrets do n.Gabi
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_secrets_config():
    """Testa a configuração de secrets."""
    print("🔍 Testando configuração de secrets...")
    
    # 1. Verificar variáveis de ambiente
    print("\n📋 Variáveis de ambiente:")
    env_vars = [
        'SECRETS_PROVIDER',
        'OPENAI_API_KEY',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'REDIS_URL'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * len(value)}")
        else:
            print(f"❌ {var}: Não configurado")
    
    # 2. Testar importação do secrets
    print("\n📦 Testando importação do secrets...")
    try:
        sys.path.append('backend')
        from app.core.secrets import SecretsService
        
        print("✅ SecretsService importado com sucesso")
        
        # 3. Testar inicialização
        print("\n🔧 Testando inicialização...")
        try:
            secrets_service = SecretsService()
            print("✅ SecretsService inicializado com sucesso")
            
            # 4. Testar recuperação de secrets
            print("\n🎯 Testando recuperação de secrets...")
            
            openai_key = secrets_service.get_openai_api_key()
            if openai_key:
                print(f"✅ OpenAI API Key: {'*' * len(openai_key)}")
            else:
                print("❌ OpenAI API Key: Não encontrado")
            
            jwt_secret = secrets_service.get_jwt_secret()
            if jwt_secret:
                print(f"✅ JWT Secret: {'*' * len(jwt_secret)}")
            else:
                print("❌ JWT Secret: Não encontrado")
            
            # 5. Testar todos os secrets
            print("\n📊 Todos os secrets:")
            all_secrets = secrets_service.get_all_secrets()
            for key, value in all_secrets.items():
                print(f"✅ {key}: {'*' * len(value)}")
            
            print("\n🎉 Teste de secrets concluído com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar SecretsService: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Erro ao importar SecretsService: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_environment():
    """Testa o ambiente de execução."""
    print("🔍 Testando ambiente...")
    
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('backend'):
        print("❌ Diretório 'backend' não encontrado")
        return False
    
    if not os.path.exists('backend/app/core/secrets.py'):
        print("❌ Arquivo 'secrets.py' não encontrado")
        return False
    
    print("✅ Ambiente OK")
    return True

if __name__ == "__main__":
    print("🚀 Teste de Secrets - n.Gabi")
    print("=" * 40)
    
    # Testar ambiente
    if not test_environment():
        sys.exit(1)
    
    # Testar secrets
    if test_secrets_config():
        print("\n✅ Todos os testes passaram!")
        sys.exit(0)
    else:
        print("\n❌ Alguns testes falharam!")
        sys.exit(1) 