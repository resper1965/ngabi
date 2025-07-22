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
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_anon_key: str = Field(..., env="SUPABASE_ANON_KEY")
    supabase_service_role_key: Optional[str] = Field(None, env="SUPABASE_SERVICE_ROLE_KEY")
    
    # =============================================================================
    # CACHE CONFIGURATION (Otimizado)
    # =============================================================================
    # Usar Redis apenas para cache específico do chat
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
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
    # SECURITY CONFIGURATION
    # =============================================================================
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instância global das configurações
settings = Settings() 