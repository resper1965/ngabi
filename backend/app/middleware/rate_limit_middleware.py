"""
Middleware personalizado para rate limiting com logging e métricas.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.rate_limiting import (
    get_tenant_id_from_request,
    get_remote_address,
    is_rate_limiting_enabled
)

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware personalizado para rate limiting com logging e métricas.
    """
    
    def __init__(self, app, rate_limit_config: dict = None):
        super().__init__(app)
        self.rate_limit_config = rate_limit_config or {}
        self.request_counts = {}  # Para métricas básicas
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa a requisição com rate limiting e logging.
        """
        start_time = time.time()
        
        # Extrair informações da requisição
        tenant_id = get_tenant_id_from_request(request)
        client_ip = get_remote_address(request)
        path = request.url.path
        method = request.method
        
        # Log da requisição recebida
        logger.info(
            f"Requisição recebida: {method} {path} - "
            f"Tenant: {tenant_id} - IP: {client_ip}"
        )
        
        # Verificar se rate limiting está habilitado
        if not is_rate_limiting_enabled():
            logger.debug("Rate limiting desabilitado, processando requisição normalmente")
            response = await call_next(request)
            return response
        
        # Verificar se o endpoint tem configuração específica
        endpoint_config = self._get_endpoint_config(path, method)
        if endpoint_config:
            # Aplicar rate limiting personalizado
            rate_limit_result = await self._check_rate_limit(
                request, tenant_id, client_ip, endpoint_config
            )
            
            if not rate_limit_result["allowed"]:
                logger.warning(
                    f"Rate limit excedido: {method} {path} - "
                    f"Tenant: {tenant_id} - IP: {client_ip}"
                )
                
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "message": f"Limite de {endpoint_config['requests']} requisições por {endpoint_config['window']} excedido",
                        "retry_after": rate_limit_result.get("retry_after", 60),
                        "tenant_id": tenant_id,
                        "endpoint": path
                    }
                )
        
        # Processar requisição
        try:
            response = await call_next(request)
            
            # Calcular tempo de processamento
            process_time = time.time() - start_time
            
            # Log da resposta
            logger.info(
                f"Resposta enviada: {response.status_code} - "
                f"Tenant: {tenant_id} - IP: {client_ip} - "
                f"Tempo: {process_time:.3f}s"
            )
            
            # Adicionar headers de rate limiting
            response.headers["X-Rate-Limit-Tenant"] = tenant_id
            response.headers["X-Process-Time"] = str(process_time)
            
            # Atualizar métricas
            self._update_metrics(tenant_id, path, response.status_code, process_time)
            
            return response
            
        except Exception as e:
            # Log de erro
            logger.error(
                f"Erro ao processar requisição: {method} {path} - "
                f"Tenant: {tenant_id} - IP: {client_ip} - "
                f"Erro: {str(e)}"
            )
            
            # Retornar erro 500
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "Erro interno do servidor",
                    "tenant_id": tenant_id
                }
            )
    
    def _get_endpoint_config(self, path: str, method: str) -> dict:
        """
        Retorna configuração de rate limiting para o endpoint.
        """
        # Configurações específicas por endpoint
        endpoint_configs = {
            "/chat/": {"requests": 10, "window": "1 minute"},
            "/chat/stream": {"requests": 5, "window": "1 minute"},
            "/chat/batch": {"requests": 2, "window": "1 minute"},
            "/auth/login": {"requests": 5, "window": "1 minute"},
            "/upload/": {"requests": 5, "window": "1 minute"},
        }
        
        # Buscar configuração mais específica
        for endpoint, config in endpoint_configs.items():
            if path.startswith(endpoint):
                return config
        
        # Configuração padrão
        return {"requests": 100, "window": "1 minute"}
    
    async def _check_rate_limit(self, request: Request, tenant_id: str, client_ip: str, config: dict) -> dict:
        """
        Verifica se a requisição está dentro do rate limit.
        Implementação básica - pode ser expandida com Redis, etc.
        """
        # Chave única para o rate limit
        rate_limit_key = f"{tenant_id}:{request.url.path}"
        
        # Implementação básica usando dicionário em memória
        # Em produção, use Redis ou outro storage distribuído
        current_time = time.time()
        
        if rate_limit_key not in self.request_counts:
            self.request_counts[rate_limit_key] = []
        
        # Remover requisições antigas (baseado na janela de tempo)
        window_seconds = self._parse_time_window(config["window"])
        cutoff_time = current_time - window_seconds
        
        self.request_counts[rate_limit_key] = [
            req_time for req_time in self.request_counts[rate_limit_key]
            if req_time > cutoff_time
        ]
        
        # Verificar se ainda há espaço no rate limit
        if len(self.request_counts[rate_limit_key]) >= config["requests"]:
            # Rate limit excedido
            oldest_request = min(self.request_counts[rate_limit_key])
            retry_after = int(oldest_request + window_seconds - current_time)
            
            return {
                "allowed": False,
                "retry_after": max(retry_after, 1)
            }
        
        # Adicionar requisição atual
        self.request_counts[rate_limit_key].append(current_time)
        
        return {"allowed": True}
    
    def _parse_time_window(self, window: str) -> int:
        """
        Converte janela de tempo para segundos.
        """
        if "second" in window:
            return 1
        elif "minute" in window:
            return 60
        elif "hour" in window:
            return 3600
        elif "day" in window:
            return 86400
        else:
            return 60  # Padrão: 1 minuto
    
    def _update_metrics(self, tenant_id: str, path: str, status_code: int, process_time: float):
        """
        Atualiza métricas de requisições.
        """
        # Implementação básica - pode ser expandida com Prometheus, etc.
        metric_key = f"{tenant_id}:{path}"
        
        if metric_key not in self.request_counts:
            self.request_counts[metric_key] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_time": 0.0,
                "avg_time": 0.0
            }
        
        metrics = self.request_counts[metric_key]
        metrics["total_requests"] += 1
        metrics["total_time"] += process_time
        metrics["avg_time"] = metrics["total_time"] / metrics["total_requests"]
        
        if 200 <= status_code < 400:
            metrics["successful_requests"] += 1
        else:
            metrics["failed_requests"] += 1

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging detalhado de requisições.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Adiciona logging detalhado para todas as requisições.
        """
        start_time = time.time()
        
        # Informações da requisição
        tenant_id = get_tenant_id_from_request(request)
        client_ip = get_remote_address(request)
        user_agent = request.headers.get("user-agent", "Unknown")
        
        # Log de início
        logger.info(
            f"=== REQUISIÇÃO INICIADA ==="
            f"\nMétodo: {request.method}"
            f"\nPath: {request.url.path}"
            f"\nQuery: {request.url.query}"
            f"\nTenant: {tenant_id}"
            f"\nIP: {client_ip}"
            f"\nUser-Agent: {user_agent}"
            f"\nHeaders: {dict(request.headers)}"
        )
        
        # Processar requisição
        response = await call_next(request)
        
        # Calcular tempo
        process_time = time.time() - start_time
        
        # Log de fim
        logger.info(
            f"=== REQUISIÇÃO FINALIZADA ==="
            f"\nStatus: {response.status_code}"
            f"\nTempo: {process_time:.3f}s"
            f"\nTenant: {tenant_id}"
            f"\nIP: {client_ip}"
        )
        
        return response

class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware para coleta de métricas.
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.metrics = {
            "total_requests": 0,
            "requests_by_tenant": {},
            "requests_by_endpoint": {},
            "response_times": [],
            "error_counts": 0
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Coleta métricas durante o processamento da requisição.
        """
        start_time = time.time()
        
        # Incrementar contador total
        self.metrics["total_requests"] += 1
        
        # Métricas por tenant
        tenant_id = get_tenant_id_from_request(request)
        if tenant_id not in self.metrics["requests_by_tenant"]:
            self.metrics["requests_by_tenant"][tenant_id] = 0
        self.metrics["requests_by_tenant"][tenant_id] += 1
        
        # Métricas por endpoint
        endpoint = request.url.path
        if endpoint not in self.metrics["requests_by_endpoint"]:
            self.metrics["requests_by_endpoint"][endpoint] = 0
        self.metrics["requests_by_endpoint"][endpoint] += 1
        
        # Processar requisição
        try:
            response = await call_next(request)
            
            # Calcular tempo de resposta
            process_time = time.time() - start_time
            self.metrics["response_times"].append(process_time)
            
            # Manter apenas os últimos 1000 tempos
            if len(self.metrics["response_times"]) > 1000:
                self.metrics["response_times"] = self.metrics["response_times"][-1000:]
            
            return response
            
        except Exception as e:
            # Incrementar contador de erros
            self.metrics["error_counts"] += 1
            raise
    
    def get_metrics(self) -> dict:
        """
        Retorna métricas coletadas.
        """
        avg_response_time = 0
        if self.metrics["response_times"]:
            avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
        
        return {
            "total_requests": self.metrics["total_requests"],
            "requests_by_tenant": self.metrics["requests_by_tenant"],
            "requests_by_endpoint": self.metrics["requests_by_endpoint"],
            "error_count": self.metrics["error_counts"],
            "avg_response_time": avg_response_time,
            "success_rate": (
                (self.metrics["total_requests"] - self.metrics["error_counts"]) / 
                self.metrics["total_requests"] * 100
            ) if self.metrics["total_requests"] > 0 else 0
        } 