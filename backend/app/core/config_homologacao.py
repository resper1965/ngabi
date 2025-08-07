"""
Configuração para Ambiente de Homologação - n.Gabi
"""

from app.core.config import settings

# Configurações específicas para homologação
HOMOLOGACAO_CONFIG = {
    # Ambiente
    "ENVIRONMENT": "homologacao",
    "DEBUG": False,
    "LOG_LEVEL": "INFO",
    
    # URLs com diretórios
    "FRONTEND_URL": "https://ngabi.ness.tec.br",
    "API_URL": "https://ngabi.ness.tec.br/api",
    "BACKEND_URL": "https://ngabi.ness.tec.br/backend",
    
    # Rate Limiting (mais permissivo para testes)
    "RATE_LIMIT_CHAT": 200,
    "RATE_LIMIT_AUTH": 100,
    "RATE_LIMIT_API": 500,
    
    # Timeouts
    "REQUEST_TIMEOUT": 30,
    "CHAT_TIMEOUT": 60,
    
    # Cache
    "CACHE_TTL": 1800,  # 30 minutos
    "CACHE_MAX_SIZE": 1000,
    
    # LangChain
    "LANGCHAIN_DEBUG": True,
    "LANGCHAIN_TRACING": True,
    
    # OpenAI
    "OPENAI_TIMEOUT": 60,
    "OPENAI_MAX_RETRIES": 3,
    
    # Supabase
    "SUPABASE_TIMEOUT": 30,
    "SUPABASE_MAX_RETRIES": 3,
    
    # Redis
    "REDIS_TIMEOUT": 10,
    "REDIS_MAX_RETRIES": 3,
    
    # Logging
    "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "LOG_FILE": "logs/homologacao.log",
    
    # Monitoring
    "HEALTH_CHECK_INTERVAL": 30,
    "METRICS_ENABLED": True,
    
    # Security
    "CORS_ORIGINS": [
        "https://ngabi.ness.tec.br",
        "http://localhost:3000",  # Para desenvolvimento local
    ],
    
    # Features
    "FEATURES": {
        "chat_enabled": True,
        "agents_enabled": True,
        "langchain_enabled": True,
        "voice_style_enabled": True,
        "rag_enabled": True,
        "streaming_enabled": True,
        "caching_enabled": True,
        "rate_limiting_enabled": True,
        "monitoring_enabled": True,
    }
}

def get_homologacao_config():
    """Obter configuração de homologação."""
    return HOMOLOGACAO_CONFIG

def is_homologacao():
    """Verificar se está em ambiente de homologação."""
    return settings.environment == "homologacao"

def get_homologacao_urls():
    """Obter URLs de homologação."""
    return {
        "frontend": HOMOLOGACAO_CONFIG["FRONTEND_URL"],
        "api": HOMOLOGACAO_CONFIG["API_URL"],
        "backend": HOMOLOGACAO_CONFIG["BACKEND_URL"],
        "docs": f"{HOMOLOGACAO_CONFIG['BACKEND_URL']}/docs",
        "health": f"{HOMOLOGACAO_CONFIG['BACKEND_URL']}/health",
    } 