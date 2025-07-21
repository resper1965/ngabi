"""
Configuração de Rate Limiting usando slowapi.
Limita requisições por tenant_id para endpoints específicos.
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException, Depends
from typing import Optional
import logging

try:
    from app.core.metrics import record_rate_limit_metric
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False

# Configurar logger
logger = logging.getLogger(__name__)

# Criar instância do limiter
limiter = Limiter(key_func=get_remote_address)

def get_tenant_id_from_request(request: Request) -> Optional[str]:
    """
    Extrai o tenant_id da requisição.
    Pode vir de diferentes fontes: header, query param, path param, etc.
    """
    # 1. Tentar extrair do header X-Tenant-ID
    tenant_id = request.headers.get("X-Tenant-ID")
    if tenant_id:
        return tenant_id
    
    # 2. Tentar extrair do query parameter tenant_id
    tenant_id = request.query_params.get("tenant_id")
    if tenant_id:
        return tenant_id
    
    # 3. Tentar extrair do path parameter (se aplicável)
    tenant_id = request.path_params.get("tenant_id")
    if tenant_id:
        return tenant_id
    
    # 4. Tentar extrair do JWT token (se autenticação estiver implementada)
    # auth_header = request.headers.get("Authorization")
    # if auth_header and auth_header.startswith("Bearer "):
    #     token = auth_header.split(" ")[1]
    #     # Decodificar JWT e extrair tenant_id
    #     # tenant_id = decode_jwt_and_get_tenant_id(token)
    
    # 5. Fallback para IP do cliente (menos seguro)
    logger.warning(f"Tenant ID não encontrado para {request.url.path}, usando IP: {get_remote_address(request)}")
    return get_remote_address(request)

def get_tenant_key(request: Request) -> str:
    """
    Função para gerar chave única baseada no tenant_id.
    Usada pelo slowapi para identificar diferentes tenants.
    """
    tenant_id = get_tenant_id_from_request(request)
    if not tenant_id:
        # Fallback para IP se tenant_id não estiver disponível
        tenant_id = get_remote_address(request)
    
    return f"tenant:{tenant_id}"

def get_user_key(request: Request) -> str:
    """
    Função para gerar chave única baseada no usuário.
    Combina tenant_id + user_id para rate limiting por usuário.
    """
    tenant_id = get_tenant_id_from_request(request)
    user_id = request.headers.get("X-User-ID") or request.query_params.get("user_id")
    
    if not tenant_id:
        tenant_id = get_remote_address(request)
    
    if not user_id:
        # Fallback para IP se user_id não estiver disponível
        user_id = get_remote_address(request)
    
    return f"user:{tenant_id}:{user_id}"

def get_ip_key(request: Request) -> str:
    """
    Função para gerar chave única baseada no IP.
    Fallback para rate limiting por IP.
    """
    return f"ip:{get_remote_address(request)}"

# Decorators de rate limiting
def rate_limit_by_tenant(requests: int, window: str):
    """
    Decorator para limitar requisições por tenant.
    
    Args:
        requests: Número de requisições permitidas
        window: Janela de tempo (ex: "1 minute", "1 hour", "1 day")
    """
    return limiter.limit(f"{requests}/{window}", key_func=get_tenant_key)

def rate_limit_by_user(requests: int, window: str):
    """
    Decorator para limitar requisições por usuário dentro de um tenant.
    
    Args:
        requests: Número de requisições permitidas
        window: Janela de tempo (ex: "1 minute", "1 hour", "1 day")
    """
    return limiter.limit(f"{requests}/{window}", key_func=get_user_key)

def rate_limit_by_ip(requests: int, window: str):
    """
    Decorator para limitar requisições por IP.
    
    Args:
        requests: Número de requisições permitidas
        window: Janela de tempo (ex: "1 minute", "1 hour", "1 day")
    """
    return limiter.limit(f"{requests}/{window}", key_func=get_ip_key)

# Configurações específicas para diferentes endpoints
CHAT_RATE_LIMIT = "10/minute"  # 10 requisições por minuto
AUTH_RATE_LIMIT = "5/minute"   # 5 tentativas de login por minuto
API_RATE_LIMIT = "100/minute"  # 100 requisições gerais por minuto
UPLOAD_RATE_LIMIT = "5/minute" # 5 uploads por minuto

# Decorators pré-configurados
chat_rate_limit = rate_limit_by_tenant(10, "1 minute")
auth_rate_limit = rate_limit_by_ip(5, "1 minute")
api_rate_limit = rate_limit_by_tenant(100, "1 minute")
upload_rate_limit = rate_limit_by_tenant(5, "1 minute")

# Decorators para diferentes níveis de usuário
admin_rate_limit = rate_limit_by_user(50, "1 minute")  # Admins têm mais requisições
user_rate_limit = rate_limit_by_user(20, "1 minute")   # Usuários normais
developer_rate_limit = rate_limit_by_user(100, "1 minute")  # Desenvolvedores

def get_rate_limit_by_role(role: str):
    """
    Retorna o decorator de rate limit baseado no papel do usuário.
    
    Args:
        role: Papel do usuário ('admin', 'user', 'developer')
    """
    role_limits = {
        "admin": admin_rate_limit,
        "user": user_rate_limit,
        "developer": developer_rate_limit,
    }
    return role_limits.get(role, user_rate_limit)

# Middleware para logging de rate limiting
async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware para logging de requisições e rate limiting.
    """
    tenant_id = get_tenant_id_from_request(request)
    client_ip = get_remote_address(request)
    
    # Log da requisição
    logger.info(f"Requisição: {request.method} {request.url.path} - Tenant: {tenant_id} - IP: {client_ip}")
    
    # Processar requisição
    response = await call_next(request)
    
    # Log da resposta
    logger.info(f"Resposta: {response.status_code} - Tenant: {tenant_id} - IP: {client_ip}")
    
    return response

# Função para configurar rate limiting na aplicação
def setup_rate_limiting(app):
    """
    Configura rate limiting na aplicação FastAPI.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    # Adicionar limiter à aplicação
    app.state.limiter = limiter
    
    # Adicionar handler para rate limit exceeded
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Adicionar middleware de logging
    app.middleware("http")(rate_limit_middleware)
    
    logger.info("Rate limiting configurado com sucesso")

# Função para obter estatísticas de rate limiting
def get_rate_limit_stats(request: Request) -> dict:
    """
    Retorna estatísticas de rate limiting para o tenant atual.
    
    Args:
        request: Requisição atual
        
    Returns:
        Dicionário com estatísticas
    """
    tenant_id = get_tenant_id_from_request(request)
    client_ip = get_remote_address(request)
    
    # Aqui você pode implementar lógica para obter estatísticas
    # do Redis ou outro storage usado pelo slowapi
    
    return {
        "tenant_id": tenant_id,
        "client_ip": client_ip,
        "current_limits": {
            "chat": "10/minute",
            "auth": "5/minute",
            "api": "100/minute",
            "upload": "5/minute"
        }
    }

# Função para resetar rate limits (útil para testes)
def reset_rate_limits(request: Request):
    """
    Reseta os rate limits para o tenant atual.
    Útil para testes e debugging.
    
    Args:
        request: Requisição atual
    """
    tenant_id = get_tenant_id_from_request(request)
    client_ip = get_remote_address(request)
    
    # Resetar limites no storage (Redis, etc.)
    # Esta é uma implementação básica - você pode expandir conforme necessário
    
    logger.info(f"Rate limits resetados para tenant: {tenant_id}, IP: {client_ip}")
    
    return {"message": "Rate limits resetados", "tenant_id": tenant_id}

# Configurações de ambiente
from app.core.config import settings

RATE_LIMIT_ENABLED = settings.rate_limit_enabled
RATE_LIMIT_STORAGE_URL = settings.redis_url  # Storage para rate limits

# Função para verificar se rate limiting está habilitado
def is_rate_limiting_enabled() -> bool:
    """Verifica se rate limiting está habilitado."""
    return RATE_LIMIT_ENABLED

# Decorator condicional para rate limiting
def conditional_rate_limit(requests: int, window: str):
    """
    Decorator que aplica rate limiting apenas se estiver habilitado.
    
    Args:
        requests: Número de requisições permitidas
        window: Janela de tempo
    """
    def decorator(func):
        if is_rate_limiting_enabled():
            return rate_limit_by_tenant(requests, window)(func)
        return func
    return decorator 