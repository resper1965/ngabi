#!/usr/bin/env python3
"""
Script de teste para verificar se o backend inicia corretamente.
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_backend_import():
    """Testar se o backend pode ser importado."""
    try:
        # Adicionar backend ao path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        # Testar importações principais
        logger.info("🔄 Testando importações...")
        
        # Testar secrets
        from app.core.secrets import SecretsService
        logger.info("✅ SecretsService importado com sucesso")
        
        # Testar cache
        from app.core.cache import CacheConfig, RedisCache
        logger.info("✅ Cache importado com sucesso")
        
        # Testar config
        from app.core.config import settings
        logger.info("✅ Config importado com sucesso")
        
        # Testar main
        from app.main import app
        logger.info("✅ App importado com sucesso")
        
        logger.info("🎉 Todas as importações funcionaram!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na importação: {e}")
        return False

def test_secrets_service():
    """Testar o serviço de secrets."""
    try:
        from app.core.secrets import SecretsService
        
        # Criar instância
        secrets_service = SecretsService()
        logger.info("✅ SecretsService criado com sucesso")
        
        # Testar obtenção de secrets
        openai_key = secrets_service.get_openai_api_key()
        if openai_key:
            logger.info("✅ OpenAI API Key obtida")
        else:
            logger.warning("⚠️ OpenAI API Key não encontrada (normal se não configurada)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no SecretsService: {e}")
        return False

def test_cache_service():
    """Testar o serviço de cache."""
    try:
        from app.core.cache import CacheConfig, RedisCache
        
        # Criar configuração
        config = CacheConfig()
        logger.info(f"✅ CacheConfig criado: {config.redis_url}")
        
        # Criar cache
        cache = RedisCache(config)
        logger.info("✅ RedisCache criado com sucesso")
        
        # Testar health check
        health = cache.health_check()
        logger.info(f"✅ Health check: {health}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no Cache: {e}")
        return False

def main():
    """Função principal de teste."""
    logger.info("🚀 Iniciando testes do backend...")
    
    # Testar importações
    if not test_backend_import():
        logger.error("❌ Falha nos testes de importação")
        return False
    
    # Testar secrets
    if not test_secrets_service():
        logger.error("❌ Falha nos testes de secrets")
        return False
    
    # Testar cache
    if not test_cache_service():
        logger.error("❌ Falha nos testes de cache")
        return False
    
    logger.info("🎉 Todos os testes passaram!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 