"""
Aplicação FastAPI principal com Supabase.
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
from app.routers import chat
from app.database import get_supabase

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="n.Gabi API",
    description="API da plataforma n.Gabi com Supabase",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middlewares customizados
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(RateLimitMiddleware)

# Configurar métricas Prometheus
setup_prometheus_metrics(app)

# Incluir routers
app.include_router(chat.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação."""
    logger.info("🚀 Iniciando n.Gabi Backend com Supabase...")
    
    # Configurar métricas
    logger.info("📈 Métricas habilitadas")
    
    # Verificar conexão com Supabase
    try:
        supabase = get_supabase()
        # Testar conexão fazendo uma query simples
        response = supabase.table('tenants').select('id').limit(1).execute()
        logger.info("✅ Supabase conectado com sucesso")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao conectar Supabase: {e}")
        logger.info("ℹ️ Verifique se o Supabase está configurado")
    
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
    
    logger.info("🎉 n.Gabi Backend iniciado com sucesso!")

@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "message": "n.Gabi API",
        "version": "2.0.0",
        "status": "running",
        "database": "Supabase"
    }

@app.get("/health")
async def health_check():
    """Health check da aplicação."""
    try:
        # Verificar Supabase
        supabase = get_supabase()
        supabase.table('tenants').select('id').limit(1).execute()
        
        # Verificar Redis
        cache_health = cache_health_check()
        
        return {
            "status": "healthy",
            "database": "connected",
            "cache": cache_health.get("status", "unknown"),
            "timestamp": "2024-07-21T18:38:34Z"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2024-07-21T18:38:34Z"
            }
        )

@app.get("/metrics")
async def get_metrics():
    """Endpoint para métricas Prometheus."""
    return metrics

@app.get("/cache/stats")
async def get_cache_stats():
    """Estatísticas do cache Redis."""
    return get_cache_stats()

@app.get("/cache/health")
async def cache_health():
    """Health check do cache."""
    return cache_health_check()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 