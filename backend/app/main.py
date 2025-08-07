"""
Aplicação FastAPI principal otimizada - Supabase como infraestrutura.
Foco na lógica de IA e delegação de infraestrutura para Supabase.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.cache import cache_health_check, get_cache_stats
from app.core.metrics import setup_prometheus_metrics, metrics
from app.middleware.rate_limit_middleware import (
    RateLimitMiddleware,
    LoggingMiddleware,
    MetricsMiddleware
)
from app.routers import chat, auth, events, webhooks, agents
from app.database import get_supabase, check_database_health
from app.core.config import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Plataforma de chat multi-agente com IA - Supabase como infraestrutura",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

# CORS
origins = settings.cors_origins.split(",") if settings.cors_origins else ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting (Simplificado)
if settings.rate_limit_enabled:
    app.add_middleware(RateLimitMiddleware)

# Logging e Métricas
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# Configurar métricas Prometheus
setup_prometheus_metrics(app)

# =============================================================================
# STARTUP EVENT
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Inicialização da aplicação."""
    logger.info("🚀 Iniciando n.Gabi - Chat Multi-Agente")
    logger.info(f"📋 Versão: {settings.app_version}")
    logger.info(f"🔧 Modo: {'Debug' if settings.debug else 'Production'}")
    
    logger.info("📊 Métricas configuradas")
    
    # Verificar Supabase (Infraestrutura Principal)
    try:
        supabase = get_supabase()
        supabase_url = supabase.supabase_url
        if supabase_url:
            logger.info(f"✅ Supabase conectado: {supabase_url}")
            logger.info("🗄️ Banco de dados: Supabase PostgreSQL")
            logger.info("🔐 Autenticação: Supabase Auth")
            logger.info("🔄 Realtime: Supabase Realtime")
        else:
            logger.warning("⚠️ Supabase não configurado corretamente")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao conectar Supabase: {e}")
        logger.info("ℹ️ Verifique se SUPABASE_URL e SUPABASE_ANON_KEY estão configurados")
    
    # Verificar Cache Redis (Complementar)
    try:
        cache_stats = get_cache_stats()
        if cache_stats.get("connected"):
            logger.info("💾 Cache Redis: Conectado")
        else:
            logger.warning("⚠️ Cache Redis: Não conectado")
    except Exception as e:
        logger.warning(f"⚠️ Erro no cache Redis: {e}")
    
    # Verificar Eventos
    if settings.events_enabled:
        logger.info("📡 Sistema de Eventos: Habilitado")
    if settings.webhooks_enabled:
        logger.info("🔗 Webhooks: Habilitados")
    
    logger.info("🎯 Foco: Lógica de IA e Chat Multi-Agente")
    logger.info("🏗️ Infraestrutura: Supabase (DB, Auth, Realtime)")
    logger.info("✅ n.Gabi iniciado com sucesso!")

# =============================================================================
# HEALTH CHECK ENDPOINT
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check da aplicação."""
    try:
        # Verificar Supabase
        db_health = await check_database_health()
        
        # Verificar Cache
        cache_health = cache_health_check()
        
        return {
            "status": "healthy",
            "application": settings.app_name,
            "version": settings.app_version,
            "infrastructure": {
                "database": "supabase",
                "auth": "supabase",
                "realtime": "supabase",
                "cache": "redis"
            },
            "services": {
                "database": db_health.get("status", "unknown"),
                "cache": cache_health.get("status", "unknown"),
                "events": "enabled" if settings.events_enabled else "disabled",
                "webhooks": "enabled" if settings.webhooks_enabled else "disabled"
            },
            "ai": {
                "model": settings.default_chat_model,
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens
            },
            "rate_limiting": {
                "enabled": settings.rate_limit_enabled,
                "default_limit": settings.rate_limit_default,
                "chat_limit": settings.rate_limit_chat
            },
            "timestamp": "2024-07-21T18:38:34Z"
        }
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2024-07-21T18:38:34Z"
            }
        )

# =============================================================================
# METRICS ENDPOINT
# =============================================================================

@app.get("/metrics")
async def get_metrics():
    """Endpoint para métricas Prometheus."""
    return metrics

# =============================================================================
# CACHE ENDPOINTS
# =============================================================================

@app.get("/cache/health")
async def cache_health():
    """Health check do cache."""
    return cache_health_check()

@app.get("/cache/stats")
async def cache_stats():
    """Estatísticas do cache."""
    return get_cache_stats()

# =============================================================================
# ROUTERS (Foco na Lógica de Negócio)
# =============================================================================

# Autenticação (Delegada para Supabase)
app.include_router(auth.router, prefix="/api/v1")

# Chat (Foco Principal - Lógica de IA)
app.include_router(chat.router, prefix="/api/v1")

# Agentes (CRUD Completo)
app.include_router(agents.router, prefix="/api/v1")



# Eventos (Complementar)
if settings.events_enabled:
    app.include_router(events.router, prefix="/api/v1")

# Webhooks (Complementar)
if settings.webhooks_enabled:
    app.include_router(webhooks.router, prefix="/api/v1")

# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@app.get("/")
async def root():
    """Endpoint raiz com informações da aplicação."""
    return {
        "message": f"Bem-vindo ao {settings.app_name}",
        "version": settings.app_version,
        "description": "Plataforma de chat multi-agente com IA",
        "architecture": {
            "focus": "AI Logic & Chat Multi-Agent",
            "infrastructure": "Supabase (DB, Auth, Realtime)",
            "cache": "Redis (Complementar)",
            "events": "Hybrid Event System"
        },
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global de exceções."""
    logger.error(f"❌ Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "message": str(exc) if settings.debug else "Algo deu errado",
            "timestamp": "2024-07-21T18:38:34Z"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 