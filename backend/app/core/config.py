"""
Configurações da aplicação com suporte a secrets.
"""

import os
from typing import Optional
from pydantic import BaseSettings

try:
    from app.core.secrets import secrets_service
    SECRETS_AVAILABLE = True
except ImportError:
    SECRETS_AVAILABLE = False

class Settings(BaseSettings):
    """Configurações da aplicação com suporte a secrets."""
    
    # Configurações básicas
    app_name: str = "Chat Multi-Agente API"
    debug: bool = False
    environment: str = "development"
    
    # Secrets (serão carregados dinamicamente)
    openai_api_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    
    # Configurações de secrets
    secrets_provider: str = "vault"  # vault ou aws
    vault_url: str = "http://localhost:8200"
    vault_token: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # Configurações de cache
    redis_url: str = "redis://localhost:6379/0"
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    # Configurações de rate limiting
    rate_limit_enabled: bool = True
    chat_rate_limit: str = "10/minute"
    
    class Config:
        env_file = ".env"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_secrets()
    
    def _load_secrets(self):
        """Carrega secrets do provedor configurado."""
        if not SECRETS_AVAILABLE:
            self._load_from_env()
            return
        
        try:
            # Carregar secrets do provedor
            secrets = secrets_service.get_all_secrets()
            
            # Atualizar configurações
            if secrets.get('OPENAI_API_KEY'):
                self.openai_api_key = secrets['OPENAI_API_KEY']
            
            if secrets.get('PINECONE_API_KEY'):
                self.pinecone_api_key = secrets['PINECONE_API_KEY']
            
            if secrets.get('JWT_SECRET'):
                self.jwt_secret = secrets['JWT_SECRET']
            
            # Fallback para variáveis de ambiente
            self._load_from_env()
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar secrets: {e}")
            # Usar apenas variáveis de ambiente como fallback
            self._load_from_env()
    
    def _load_from_env(self):
        """Carrega secrets de variáveis de ambiente."""
        if not self.openai_api_key:
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.pinecone_api_key:
            self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        
        if not self.jwt_secret:
            self.jwt_secret = os.getenv('JWT_SECRET')
    
    def validate_secrets(self) -> bool:
        """Valida se todos os secrets necessários estão disponíveis."""
        required_secrets = [
            ('openai_api_key', 'OPENAI_API_KEY'),
            ('pinecone_api_key', 'PINECONE_API_KEY'),
            ('jwt_secret', 'JWT_SECRET')
        ]
        
        missing_secrets = []
        
        for attr_name, secret_name in required_secrets:
            if not getattr(self, attr_name):
                missing_secrets.append(secret_name)
        
        if missing_secrets:
            print(f"❌ Secrets faltando: {', '.join(missing_secrets)}")
            return False
        
        print("✅ Todos os secrets estão configurados")
        return True
    
    def get_secrets_info(self) -> dict:
        """Retorna informações sobre os secrets configurados."""
        return {
            "provider": self.secrets_provider,
            "secrets_available": SECRETS_AVAILABLE,
            "openai_configured": bool(self.openai_api_key),
            "pinecone_configured": bool(self.pinecone_api_key),
            "jwt_configured": bool(self.jwt_secret),
            "all_configured": self.validate_secrets()
        }

# Instância global das configurações
settings = Settings() 