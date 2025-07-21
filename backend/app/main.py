"""
Aplicação FastAPI principal com rate limiting configurado.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.rate_limiting import setup_rate_limiting
from app.core.cache import cache_health_check, get_cache_stats
from app.core.metrics import setup_prometheus_metrics, metrics
from app.middleware.rate_limit_middleware import (
    RateLimitMiddleware,
    LoggingMiddleware,
    MetricsMiddleware
)
from app.routers import chat

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Chat Multi-Agente API",
    description="API para sistema de chat multi-agente com rate limiting",
    version="1.0.0"
)

# =============================================================================
# CONFIGURAÇÃO DE CORS
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# CONFIGURAÇÃO DE RATE LIMITING
# =============================================================================

# Configurar slowapi
setup_rate_limiting(app)

# Configurar métricas Prometheus
setup_prometheus_metrics(app, metrics)

# Adicionar middleware personalizado
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# Configuração de rate limiting por endpoint
rate_limit_config = {
    "/chat/": {"requests": 10, "window": "1 minute"},
    "/chat/stream": {"requests": 5, "window": "1 minute"},
    "/chat/batch": {"requests": 2, "window": "1 minute"},
    "/auth/": {"requests": 5, "window": "1 minute"},
    "/upload/": {"requests": 5, "window": "1 minute"},
}

app.add_middleware(RateLimitMiddleware, rate_limit_config=rate_limit_config)

# =============================================================================
# ROUTERS
# =============================================================================

app.include_router(chat.router, prefix="/api/v1")

# =============================================================================
# ENDPOINTS BÁSICOS
# =============================================================================

@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "message": "Chat Multi-Agente API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check."""
    return {
        "status": "healthy",
        "service": "chat-multi-agente",
        "version": "1.0.0"
    }

@app.get("/metrics")
async def get_metrics(request: Request):
    """
    Endpoint para obter métricas da aplicação.
    """
    # Obter métricas do middleware
    metrics_middleware = None
    for middleware in app.user_middleware:
        if isinstance(middleware.cls, MetricsMiddleware):
            metrics_middleware = middleware.cls
            break
    
    if metrics_middleware:
        return metrics_middleware.get_metrics()
    
    return {"message": "Métricas não disponíveis"}

@app.get("/cache/health")
async def get_cache_health():
    """
    Endpoint para verificar saúde do cache Redis.
    """
    return cache_health_check()

@app.get("/cache/stats")
async def get_cache_stats_endpoint(request: Request):
    """
    Endpoint para obter estatísticas do cache.
    """
    from app.core.rate_limiting import get_tenant_id_from_request
    
    tenant_id = get_tenant_id_from_request(request)
    return get_cache_stats(tenant_id)

@app.get("/secrets/health")
async def get_secrets_health():
    """
    Endpoint para verificar saúde dos secrets.
    """
    from app.core.config import settings
    
    return {
        "status": "healthy" if settings.validate_secrets() else "unhealthy",
        "secrets_info": settings.get_secrets_info(),
        "timestamp": "2024-01-01T00:00:00Z"
    }

# =============================================================================
# HANDLERS DE ERRO
# =============================================================================

@app.exception_handler(429)
async def rate_limit_exceeded_handler(request: Request, exc):
    """
    Handler personalizado para rate limit exceeded.
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Você excedeu o limite de requisições. Tente novamente em alguns minutos.",
            "retry_after": 60,
            "endpoint": request.url.path
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """
    Handler para erros internos.
    """
    logger.error(f"Erro interno: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Erro interno do servidor. Tente novamente mais tarde."
        }
    )

# =============================================================================
# MIDDLEWARE DE LOGGING GLOBAL
# =============================================================================

@app.middleware("http")
async def global_logging_middleware(request: Request, call_next):
    """
    Middleware global para logging de todas as requisições.
    """
    import time
    
    start_time = time.time()
    
    # Log da requisição
    logger.info(f"Requisição iniciada: {request.method} {request.url.path}")
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de processamento
    process_time = time.time() - start_time
    
    # Log da resposta
    logger.info(
        f"Requisição finalizada: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Tempo: {process_time:.3f}s"
    )
    
    # Adicionar header com tempo de processamento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# =============================================================================
# CONFIGURAÇÃO DE STARTUP E SHUTDOWN
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Evento executado na inicialização da aplicação.
    """
    logger.info("🚀 n.Gabi Backend iniciando...")
    logger.info("📊 Rate limiting configurado")
    logger.info("🔧 Middleware de logging ativo")
    logger.info("📈 Métricas habilitadas")
    
    # Verificar conexão com PostgreSQL
    try:
        from app.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ PostgreSQL conectado com sucesso")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao conectar PostgreSQL: {e}")
        logger.info("ℹ️ Verifique se o PostgreSQL está rodando")
    
    # Verificar conexão com Redis
    try:
        from app.core.cache import cache_health_check
        health = cache_health_check()
        if health.get("status") == "healthy":
            logger.info("✅ Redis conectado com sucesso")
        else:
            logger.warning("⚠️ Redis não disponível, cache desabilitado")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao conectar Redis: {e}")
        logger.info("ℹ️ Aplicação funcionará sem cache")
    
    # Verificar conexão com Elasticsearch
    try:
        import requests
        response = requests.get("http://elasticsearch:9200/_cluster/health", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Elasticsearch conectado com sucesso")
        else:
            logger.warning("⚠️ Elasticsearch não disponível")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao conectar Elasticsearch: {e}")
        logger.info("ℹ️ Funcionalidades de busca podem não funcionar")
    
    logger.info("🎉 n.Gabi Backend iniciado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento executado no encerramento da aplicação.
    """
    logger.info("🛑 Aplicação encerrada")

# =============================================================================
# EXEMPLO DE USO DOS DECORATORS
# =============================================================================

# Este é um exemplo de como usar os decorators de rate limiting
# em outros endpoints da aplicação

from app.core.rate_limiting import (
    chat_rate_limit,
    rate_limit_by_tenant,
    rate_limit_by_user,
    conditional_rate_limit
)

@app.get("/api/v1/test/rate-limit")
@chat_rate_limit  # 10 requisições por minuto por tenant
async def test_rate_limit(request: Request):
    """
    Endpoint de teste para rate limiting.
    """
    from app.core.rate_limiting import get_tenant_id_from_request
    
    tenant_id = get_tenant_id_from_request(request)
    
    return {
        "message": "Rate limit testado com sucesso",
        "tenant_id": tenant_id,
        "limit": "10/minute"
    }

@app.get("/api/v1/test/user-limit")
@rate_limit_by_user(5, "1 minute")  # 5 requisições por minuto por usuário
async def test_user_rate_limit(request: Request):
    """
    Endpoint de teste para rate limiting por usuário.
    """
    return {
        "message": "User rate limit testado",
        "limit": "5/minute per user"
    }

@app.get("/api/v1/test/conditional-limit")
@conditional_rate_limit(3, "1 minute")  # Rate limit condicional
async def test_conditional_rate_limit(request: Request):
    """
    Endpoint de teste para rate limiting condicional.
    """
    return {
        "message": "Conditional rate limit testado",
        "enabled": True
    }

# =============================================================================
# DOCUMENTAÇÃO DA API
# =============================================================================

@app.get("/docs/rate-limiting")
async def rate_limiting_docs():
    """
    Documentação sobre rate limiting.
    """
    return {
        "rate_limiting": {
            "description": "Sistema de rate limiting por tenant e usuário",
            "endpoints": {
                "/chat/": "10 requisições por minuto por tenant",
                "/chat/stream": "5 requisições por minuto por tenant",
                "/chat/batch": "2 requisições por minuto por tenant",
                "/auth/": "5 requisições por minuto por IP",
                "/upload/": "5 requisições por minuto por tenant"
            },
            "headers": {
                "X-Tenant-ID": "ID do tenant para rate limiting",
                "X-User-ID": "ID do usuário para rate limiting por usuário",
                "X-User-Role": "Papel do usuário (admin, user, developer)"
            },
            "error_responses": {
                "429": "Rate limit exceeded",
                "500": "Internal server error"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 