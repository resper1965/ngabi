"""
Configurações da aplicação com suporte a secrets.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

# Configuração otimizada para Supabase como infraestrutura principal
class Settings(BaseSettings):
    # =============================================================================
    # SUPABASE CONFIGURATION (Infraestrutura Principal)
    # =============================================================================
    supabase_url: Optional[str] = Field(default=None, env="SUPABASE_URL")
    supabase_anon_key: Optional[str] = Field(default=None, env="SUPABASE_ANON_KEY")
    supabase_service_role_key: Optional[str] = Field(None, env="SUPABASE_SERVICE_ROLE_KEY")
    
    # =============================================================================
    # CACHE CONFIGURATION (EasyUIPanel Redis)
    # =============================================================================
    # Redis configurado pelo EasyUIPanel
    redis_url: str = Field(default="redis://default:6cebb38271cd2fea746a@ngabi_ngabi-redis:6379", env="REDIS_URL")
    redis_host: str = Field(default="ngabi_ngabi-redis", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: str = Field(default="6cebb38271cd2fea746a", env="REDIS_PASSWORD")
    redis_username: str = Field(default="default", env="REDIS_USERNAME")
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hora
    
    # =============================================================================
    # RATE LIMITING (Simplificado)
    # =============================================================================
    # Rate limiting básico para complementar Supabase
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_default: int = Field(default=100, env="RATE_LIMIT_DEFAULT")  # req/min
    rate_limit_chat: int = Field(default=20, env="RATE_LIMIT_CHAT")  # req/min por usuário
    
    # =============================================================================
    # APPLICATION CONFIGURATION
    # =============================================================================
    app_name: str = Field(default="n.Gabi", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # =============================================================================
    # CORS CONFIGURATION
    # =============================================================================
    cors_origins: str = Field(default="http://localhost:3000", env="CORS_ORIGINS")
    
    # =============================================================================
    # AI/CHAT CONFIGURATION (Foco Principal)
    # =============================================================================
    default_chat_model: str = Field(default="gpt-3.5-turbo", env="DEFAULT_CHAT_MODEL")
    max_tokens: int = Field(default=2048, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    
    # =============================================================================
    # EVENT SYSTEM CONFIGURATION
    # =============================================================================
    events_enabled: bool = Field(default=True, env="EVENTS_ENABLED")
    webhooks_enabled: bool = Field(default=True, env="WEBHOOKS_ENABLED")
    
    # =============================================================================
    # SECURITY CONFIGURATION (Delegado para Supabase)
    # =============================================================================
    # JWT é gerenciado automaticamente pelo Supabase Auth
    # Não precisamos de JWT_SECRET separado
    
    # =============================================================================
    # LOGGING CONFIGURATION
    # =============================================================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # =============================================================================
    # CHAT RATE LIMITING
    # =============================================================================
    chat_rate_limit: str = Field(default="10/minute", env="CHAT_RATE_LIMIT")
    

    
    # =============================================================================
    # ADDITIONAL CONFIGURATION (Fallback)
    # =============================================================================
    environment: str = Field(default="production", env="ENVIRONMENT")
    secrets_provider: str = Field(default="env", env="SECRETS_PROVIDER")
    vault_url: Optional[str] = Field(None, env="VAULT_URL")
    vault_token: Optional[str] = Field(None, env="VAULT_TOKEN")
    aws_region: Optional[str] = Field(None, env="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, env="AWS_SECRET_ACCESS_KEY")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    pinecone_api_key: Optional[str] = Field(None, env="PINECONE_API_KEY")
    # jwt_secret removido - gerenciado pelo Supabase Auth
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignorar variáveis extras

# Instância global das configurações
settings = Settings() 