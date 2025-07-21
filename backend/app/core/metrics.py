"""
Sistema de métricas Prometheus para FastAPI.
Métricas de latência, QPS, rate limiting e cache.
"""

import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Summary,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    multiprocess,
    start_http_server
)
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class PrometheusMetrics:
    """Classe para gerenciar métricas Prometheus."""
    
    def __init__(self):
        self.registry = CollectorRegistry()
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Inicializa todas as métricas."""
        
        # Métricas de requisições HTTP
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total de requisições HTTP',
            ['method', 'endpoint', 'status_code', 'tenant_id'],
            registry=self.registry
        )
        
        self.http_request_duration_seconds = Histogram(
            'http_request_duration_seconds',
            'Duração das requisições HTTP',
            ['method', 'endpoint', 'tenant_id'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0],
            registry=self.registry
        )
        
        self.http_request_size_bytes = Histogram(
            'http_request_size_bytes',
            'Tamanho das requisições HTTP',
            ['method', 'endpoint', 'tenant_id'],
            buckets=[100, 500, 1000, 5000, 10000, 50000, 100000],
            registry=self.registry
        )
        
        self.http_response_size_bytes = Histogram(
            'http_response_size_bytes',
            'Tamanho das respostas HTTP',
            ['method', 'endpoint', 'tenant_id'],
            buckets=[100, 500, 1000, 5000, 10000, 50000, 100000],
            registry=self.registry
        )
        
        # Métricas de QPS (Queries Per Second)
        self.http_requests_per_second = Counter(
            'http_requests_per_second',
            'Requisições por segundo',
            ['method', 'endpoint', 'tenant_id'],
            registry=self.registry
        )
        
        # Métricas de rate limiting
        self.rate_limit_hits_total = Counter(
            'rate_limit_hits_total',
            'Total de hits de rate limiting',
            ['endpoint', 'tenant_id', 'limit_type'],
            registry=self.registry
        )
        
        self.rate_limit_exceeded_total = Counter(
            'rate_limit_exceeded_total',
            'Total de violações de rate limiting',
            ['endpoint', 'tenant_id', 'limit_type'],
            registry=self.registry
        )
        
        # Métricas de cache
        self.cache_hits_total = Counter(
            'cache_hits_total',
            'Total de cache hits',
            ['cache_type', 'tenant_id'],
            registry=self.registry
        )
        
        self.cache_misses_total = Counter(
            'cache_misses_total',
            'Total de cache misses',
            ['cache_type', 'tenant_id'],
            registry=self.registry
        )
        
        self.cache_size = Gauge(
            'cache_size',
            'Tamanho atual do cache',
            ['cache_type', 'tenant_id'],
            registry=self.registry
        )
        
        # Métricas de secrets
        self.secrets_requests_total = Counter(
            'secrets_requests_total',
            'Total de requisições de secrets',
            ['secret_type', 'provider', 'status'],
            registry=self.registry
        )
        
        self.secrets_request_duration_seconds = Histogram(
            'secrets_request_duration_seconds',
            'Duração das requisições de secrets',
            ['secret_type', 'provider'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
            registry=self.registry
        )
        
        # Métricas de negócio
        self.chat_messages_total = Counter(
            'chat_messages_total',
            'Total de mensagens de chat',
            ['agent_id', 'tenant_id', 'chat_mode'],
            registry=self.registry
        )
        
        self.chat_response_time_seconds = Histogram(
            'chat_response_time_seconds',
            'Tempo de resposta do chat',
            ['agent_id', 'tenant_id', 'chat_mode'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0],
            registry=self.registry
        )
        
        # Métricas de sistema
        self.active_connections = Gauge(
            'active_connections',
            'Conexões ativas',
            ['connection_type'],
            registry=self.registry
        )
        
        self.memory_usage_bytes = Gauge(
            'memory_usage_bytes',
            'Uso de memória em bytes',
            ['type'],
            registry=self.registry
        )
        
        # Métricas de erro
        self.errors_total = Counter(
            'errors_total',
            'Total de erros',
            ['error_type', 'endpoint', 'tenant_id'],
            registry=self.registry
        )
        
        # Métricas de performance
        self.request_queue_size = Gauge(
            'request_queue_size',
            'Tamanho da fila de requisições',
            registry=self.registry
        )
        
        self.processing_time_seconds = Summary(
            'processing_time_seconds',
            'Tempo de processamento',
            ['operation_type'],
            registry=self.registry
        )
    
    def record_request(self, method: str, endpoint: str, status_code: int, 
                      tenant_id: str, duration: float, request_size: int = 0, 
                      response_size: int = 0):
        """Registra métricas de uma requisição."""
        try:
            # Métricas básicas
            self.http_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status_code=str(status_code),
                tenant_id=tenant_id or 'unknown'
            ).inc()
            
            # Duração da requisição
            self.http_request_duration_seconds.labels(
                method=method,
                endpoint=endpoint,
                tenant_id=tenant_id or 'unknown'
            ).observe(duration)
            
            # Tamanho da requisição
            if request_size > 0:
                self.http_request_size_bytes.labels(
                    method=method,
                    endpoint=endpoint,
                    tenant_id=tenant_id or 'unknown'
                ).observe(request_size)
            
            # Tamanho da resposta
            if response_size > 0:
                self.http_response_size_bytes.labels(
                    method=method,
                    endpoint=endpoint,
                    tenant_id=tenant_id or 'unknown'
                ).observe(response_size)
            
            # QPS (incremento simples, será calculado pelo Prometheus)
            self.http_requests_per_second.labels(
                method=method,
                endpoint=endpoint,
                tenant_id=tenant_id or 'unknown'
            ).inc()
            
        except Exception as e:
            logger.error(f"Erro ao registrar métricas de requisição: {e}")
    
    def record_rate_limit(self, endpoint: str, tenant_id: str, limit_type: str, exceeded: bool = False):
        """Registra métricas de rate limiting."""
        try:
            if exceeded:
                self.rate_limit_exceeded_total.labels(
                    endpoint=endpoint,
                    tenant_id=tenant_id or 'unknown',
                    limit_type=limit_type
                ).inc()
            else:
                self.rate_limit_hits_total.labels(
                    endpoint=endpoint,
                    tenant_id=tenant_id or 'unknown',
                    limit_type=limit_type
                ).inc()
        except Exception as e:
            logger.error(f"Erro ao registrar métricas de rate limiting: {e}")
    
    def record_cache(self, cache_type: str, tenant_id: str, hit: bool):
        """Registra métricas de cache."""
        try:
            if hit:
                self.cache_hits_total.labels(
                    cache_type=cache_type,
                    tenant_id=tenant_id or 'unknown'
                ).inc()
            else:
                self.cache_misses_total.labels(
                    cache_type=cache_type,
                    tenant_id=tenant_id or 'unknown'
                ).inc()
        except Exception as e:
            logger.error(f"Erro ao registrar métricas de cache: {e}")
    
    def record_secret_request(self, secret_type: str, provider: str, status: str, duration: float = 0):
        """Registra métricas de requisições de secrets."""
        try:
            self.secrets_requests_total.labels(
                secret_type=secret_type,
                provider=provider,
                status=status
            ).inc()
            
            if duration > 0:
                self.secrets_request_duration_seconds.labels(
                    secret_type=secret_type,
                    provider=provider
                ).observe(duration)
        except Exception as e:
            logger.error(f"Erro ao registrar métricas de secrets: {e}")
    
    def record_chat_message(self, agent_id: str, tenant_id: str, chat_mode: str, response_time: float = 0):
        """Registra métricas de mensagens de chat."""
        try:
            self.chat_messages_total.labels(
                agent_id=agent_id,
                tenant_id=tenant_id or 'unknown',
                chat_mode=chat_mode
            ).inc()
            
            if response_time > 0:
                self.chat_response_time_seconds.labels(
                    agent_id=agent_id,
                    tenant_id=tenant_id or 'unknown',
                    chat_mode=chat_mode
                ).observe(response_time)
        except Exception as e:
            logger.error(f"Erro ao registrar métricas de chat: {e}")
    
    def record_error(self, error_type: str, endpoint: str, tenant_id: str):
        """Registra métricas de erro."""
        try:
            self.errors_total.labels(
                error_type=error_type,
                endpoint=endpoint,
                tenant_id=tenant_id or 'unknown'
            ).inc()
        except Exception as e:
            logger.error(f"Erro ao registrar métricas de erro: {e}")
    
    def update_cache_size(self, cache_type: str, tenant_id: str, size: int):
        """Atualiza métricas de tamanho do cache."""
        try:
            self.cache_size.labels(
                cache_type=cache_type,
                tenant_id=tenant_id or 'unknown'
            ).set(size)
        except Exception as e:
            logger.error(f"Erro ao atualizar métricas de cache: {e}")
    
    def update_active_connections(self, connection_type: str, count: int):
        """Atualiza métricas de conexões ativas."""
        try:
            self.active_connections.labels(
                connection_type=connection_type
            ).set(count)
        except Exception as e:
            logger.error(f"Erro ao atualizar métricas de conexões: {e}")
    
    def update_memory_usage(self, memory_type: str, bytes_used: int):
        """Atualiza métricas de uso de memória."""
        try:
            self.memory_usage_bytes.labels(
                type=memory_type
            ).set(bytes_used)
        except Exception as e:
            logger.error(f"Erro ao atualizar métricas de memória: {e}")
    
    def update_request_queue_size(self, size: int):
        """Atualiza métricas de tamanho da fila de requisições."""
        try:
            self.request_queue_size.set(size)
        except Exception as e:
            logger.error(f"Erro ao atualizar métricas de fila: {e}")
    
    def time_operation(self, operation_type: str):
        """Decorator para medir tempo de operações."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    self.processing_time_seconds.labels(
                        operation_type=operation_type
                    ).observe(duration)
            return wrapper
        return decorator

# Instância global das métricas
metrics = PrometheusMetrics()

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware para coletar métricas Prometheus automaticamente."""
    
    def __init__(self, app, metrics_instance: PrometheusMetrics = None):
        super().__init__(app)
        self.metrics = metrics_instance or metrics
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Extrair informações da requisição
        method = request.method
        endpoint = request.url.path
        tenant_id = self._extract_tenant_id(request)
        
        # Calcular tamanho da requisição
        request_size = 0
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = await request.body()
                request_size = len(body)
            except Exception:
                pass
        
        # Processar requisição
        try:
            response = await call_next(request)
            status_code = response.status_code
            
            # Calcular tamanho da resposta
            response_size = 0
            if hasattr(response, 'body'):
                response_size = len(response.body)
            
            # Calcular duração
            duration = time.time() - start_time
            
            # Registrar métricas
            self.metrics.record_request(
                method=method,
                endpoint=endpoint,
                status_code=status_code,
                tenant_id=tenant_id,
                duration=duration,
                request_size=request_size,
                response_size=response_size
            )
            
            # Registrar erro se status >= 400
            if status_code >= 400:
                error_type = 'client_error' if status_code < 500 else 'server_error'
                self.metrics.record_error(error_type, endpoint, tenant_id)
            
            return response
            
        except Exception as e:
            # Registrar erro
            self.metrics.record_error('exception', endpoint, tenant_id)
            raise
    
    def _extract_tenant_id(self, request: Request) -> str:
        """Extrai tenant_id da requisição."""
        tenant_id = (
            request.headers.get("X-Tenant-ID") or
            request.query_params.get("tenant_id")
        )
        return tenant_id or "unknown"

def setup_prometheus_metrics(app, metrics_instance: PrometheusMetrics = None):
    """Configura métricas Prometheus no app FastAPI."""
    metrics_instance = metrics_instance or metrics
    
    # Adicionar middleware
    app.add_middleware(PrometheusMiddleware, metrics_instance=metrics_instance)
    
    # Endpoint para métricas
    @app.get("/metrics")
    async def get_metrics():
        """Endpoint para expor métricas Prometheus."""
        return Response(
            content=generate_latest(metrics_instance.registry),
            media_type=CONTENT_TYPE_LATEST
        )
    
    # Endpoint para health check das métricas
    @app.get("/metrics/health")
    async def get_metrics_health():
        """Health check das métricas."""
        return {
            "status": "healthy",
            "metrics_enabled": True,
            "registry_size": len(metrics_instance.registry._collector_to_names),
            "timestamp": time.time()
        }
    
    logger.info("✅ Métricas Prometheus configuradas")

def start_prometheus_server(port: int = 8001):
    """Inicia servidor HTTP separado para métricas Prometheus."""
    try:
        start_http_server(port, registry=metrics.registry)
        logger.info(f"🚀 Servidor de métricas Prometheus iniciado na porta {port}")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor de métricas: {e}")

# Funções utilitárias para uso direto
def record_rate_limit_metric(endpoint: str, tenant_id: str, limit_type: str, exceeded: bool = False):
    """Função utilitária para registrar métricas de rate limiting."""
    metrics.record_rate_limit(endpoint, tenant_id, limit_type, exceeded)

def record_cache_metric(cache_type: str, tenant_id: str, hit: bool):
    """Função utilitária para registrar métricas de cache."""
    metrics.record_cache(cache_type, tenant_id, hit)

def record_secret_metric(secret_type: str, provider: str, status: str, duration: float = 0):
    """Função utilitária para registrar métricas de secrets."""
    metrics.record_secret_request(secret_type, provider, status, duration)

def record_chat_metric(agent_id: str, tenant_id: str, chat_mode: str, response_time: float = 0):
    """Função utilitária para registrar métricas de chat."""
    metrics.record_chat_message(agent_id, tenant_id, chat_mode, response_time)

def record_error_metric(error_type: str, endpoint: str, tenant_id: str):
    """Função utilitária para registrar métricas de erro."""
    metrics.record_error(error_type, endpoint, tenant_id) 