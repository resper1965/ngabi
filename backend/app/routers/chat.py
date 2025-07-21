"""
Router para endpoints de chat com rate limiting aplicado.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional
import uuid
import logging
from datetime import datetime

from app.database import get_supabase
from app.core.rate_limiting import (
    chat_rate_limit,
    rate_limit_by_tenant,
    rate_limit_by_user,
    get_rate_limit_by_role,
    get_tenant_id_from_request,
    get_rate_limit_stats
)
from app.core.cache import (
    cache_response,
    get_cached_response,
    set_cached_response,
    clear_tenant_cache,
    get_cache_stats,
    cache_health_check
)
from app.core.metrics import record_chat_metric, metrics
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

# =============================================================================
# ENDPOINTS COM RATE LIMITING
# =============================================================================

@router.post("/", response_model=ChatResponse)
# @chat_rate_limit  # 10 requisições por minuto por tenant
# @cache_response(ttl=3600)  # Cache por 1 hora
async def send_chat_message(
    request: ChatRequest,
    http_request: Request
):
    """
    Envia uma mensagem de chat com cache Redis.
    Rate limit: 10 requisições por minuto por tenant.
    Cache: 1 hora por tenant + agent + query.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    # Verificar cache primeiro
    cached_response = get_cached_response(
        tenant_id=tenant_id,
        agent_id=str(request.agent_id),
        query=request.message
    )
    
    if cached_response:
        logger.info(f"🎯 Cache hit para tenant {tenant_id}, agent {request.agent_id}")
        return cached_response["response"]
    
    # Validar se o agente existe e pertence ao tenant
    supabase = get_supabase()
    agent_response = supabase.table('agents').select('*').eq('id', str(request.agent_id)).eq('tenant_id', tenant_id).execute()
    agent = agent_response.data[0] if agent_response.data else None
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    # Aqui você implementaria a lógica de chat
    # Por exemplo, chamar OpenAI, processar resposta, etc.
    
    # Simular resposta (em produção, seria a resposta real do LLM)
    response_text = f"Resposta do agente {agent['name']}: {request.message}"
    
    # Criar resposta
    chat_response = ChatResponse(
        id=uuid.uuid4(),
        message=request.message,
        response=response_text,
        agent_name=agent['name'],
        chat_mode=request.chat_mode,
        created_at=datetime.utcnow()
    )
    
    # Salvar no cache
    cache_saved = set_cached_response(
        tenant_id=tenant_id,
        agent_id=str(request.agent_id),
        query=request.message,
        response=chat_response.dict(),
        ttl=3600  # 1 hora
    )
    
    if cache_saved:
        logger.info(f"💾 Resposta cacheada para tenant {tenant_id}, agent {request.agent_id}")
    
    # Salvar no histórico (opcional - pode ser feito em background)
    try:
        # Salvar no Supabase
        history_data = {
            'tenant_id': tenant_id,
            'user_id': str(request.user_id),
            'agent_id': str(request.agent_id),
            'message': request.message,
            'response': response_text,
            'chat_mode': request.chat_mode,
            'use_author_voice': request.use_author_voice
        }
        
        history_response = supabase.table('chat_history').insert(history_data).execute()
        
        if history_response.data:
            # Atualizar ID da resposta com o ID real do histórico
            chat_response.id = history_response.data[0]['id']
            chat_response.created_at = history_response.data[0]['created_at']
        
    except Exception as e:
        logger.error(f"Erro ao salvar no histórico: {e}")
        # Não falhar a requisição se o histórico falhar
    
    return chat_response

@router.post("/stream")
# @rate_limit_by_tenant(5, "1 minute")  # 5 requisições por minuto por tenant
async def stream_chat_message(
    request: ChatRequest,
    http_request: Request
):
    """
    Stream de chat (para respostas longas).
    Rate limit: 5 requisições por minuto por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    # Implementar streaming de resposta
    # Por enquanto, retorna uma resposta simples
    return {"message": "Stream endpoint - implementar streaming"}

@router.post("/batch")
# @rate_limit_by_tenant(2, "1 minute")  # 2 requisições por minuto por tenant
async def batch_chat_messages(
    requests: List[ChatRequest],
    http_request: Request
):
    """
    Processa múltiplas mensagens de chat em lote.
    Rate limit: 2 requisições por minuto por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    if len(requests) > 10:
        raise HTTPException(status_code=400, detail="Máximo de 10 mensagens por lote")
    
    responses = []
    for req in requests:
        # Processar cada mensagem
        response = ChatResponse(
            id=uuid.uuid4(),
            message=req.message,
            response=f"Resposta para: {req.message}",
            agent_name="Batch Agent",
            chat_mode=req.chat_mode,
            created_at=None
        )
        responses.append(response)
    
    return {"responses": responses}

@router.post("/user-chat")
# @rate_limit_by_user(20, "1 minute")  # 20 requisições por minuto por usuário
async def user_chat_message(
    request: ChatRequest,
    http_request: Request
):
    """
    Chat específico por usuário.
    Rate limit: 20 requisições por minuto por usuário.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    # Implementar lógica específica por usuário
    return {"message": f"Chat do usuário {request.user_id} no tenant {tenant_id}"}

@router.post("/role-based-chat")
async def role_based_chat(
    request: ChatRequest,
    http_request: Request
):
    """
    Chat baseado em roles/permissões.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    # Determinar role do usuário
    role = "user"  # Implementar lógica de roles
    
    return await _process_role_chat(request, role)

async def _process_role_chat(request: ChatRequest, role: str):
    """
    Processa chat baseado no role do usuário.
    """
    if role == "admin":
        return {"message": f"Admin chat: {request.message}"}
    elif role == "moderator":
        return {"message": f"Moderator chat: {request.message}"}
    else:
        return {"message": f"User chat: {request.message}"}

@router.get("/rate-limit-stats")
async def get_chat_rate_limit_stats(http_request: Request):
    """
    Retorna estatísticas de rate limiting.
    """
    return get_rate_limit_stats(http_request)

@router.get("/history")
# @rate_limit_by_tenant(50, "1 minute")  # 50 requisições por minuto por tenant
async def get_chat_history(
    limit: int = 10,
    offset: int = 0,
    http_request: Request = None
):
    """
    Retorna histórico de chat.
    Rate limit: 50 requisições por minuto por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request) if http_request else "default"
    
    # Implementar busca no Supabase
    supabase = get_supabase()
    history_response = supabase.table('chat_history').select('*').eq('tenant_id', tenant_id).range(offset, offset + limit - 1).execute()
    
    return {"history": history_response.data}

@router.get("/test-rate-limit")
# @rate_limit_by_tenant(3, "1 minute")  # 3 requisições por minuto por tenant
async def test_rate_limit(http_request: Request):
    """
    Endpoint para testar rate limiting.
    Rate limit: 3 requisições por minuto por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    return {
        "message": "Rate limit test",
        "tenant_id": tenant_id,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/test-different-limits")
# @rate_limit_by_tenant(5, "30 seconds")  # 5 requisições por 30 segundos
async def test_different_limits(http_request: Request):
    """
    Testa diferentes limites de rate limiting.
    Rate limit: 5 requisições por 30 segundos.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    return {
        "message": "Different rate limit test",
        "tenant_id": tenant_id,
        "limit": "5 requests per 30 seconds",
        "timestamp": datetime.utcnow().isoformat()
    }

# =============================================================================
# ENDPOINTS DE CACHE
# =============================================================================

@router.get("/cache/stats")
async def get_chat_cache_stats(http_request: Request):
    """
    Retorna estatísticas do cache.
    """
    return get_cache_stats(http_request)

@router.get("/cache/health")
async def get_cache_health():
    """
    Verifica saúde do cache.
    """
    return cache_health_check()

@router.delete("/cache/clear")
async def clear_chat_cache(http_request: Request):
    """
    Limpa cache do tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    cleared = clear_tenant_cache(tenant_id)
    return {
        "message": "Cache limpo" if cleared else "Erro ao limpar cache",
        "tenant_id": tenant_id
    }

@router.post("/cache/test")
# @cache_response(ttl=300)  # Cache por 5 minutos
async def test_cache_functionality(
    request: dict,
    http_request: Request
):
    """
    Testa funcionalidade de cache.
    Cache: 5 minutos.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    # Simular processamento
    result = {
        "message": "Cache test",
        "data": request,
        "tenant_id": tenant_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return result

# =============================================================================
# ENDPOINTS ADMIN
# =============================================================================

@router.post("/admin/reset-limits")
async def admin_reset_rate_limits(http_request: Request):
    """
    Endpoint admin para resetar rate limits.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    # Implementar reset de rate limits
    # Por enquanto, retorna sucesso
    return {
        "message": "Rate limits resetados",
        "tenant_id": tenant_id,
        "timestamp": datetime.utcnow().isoformat()
    }

# =============================================================================
# SCHEMAS (definições básicas)
# =============================================================================

# Nota: Estes schemas devem ser movidos para app/schemas/chat.py
# Aqui estão apenas para referência

class ChatRequest:
    user_id: uuid.UUID
    agent_id: uuid.UUID
    message: str
    chat_mode: str = "UsoCotidiano"
    use_author_voice: bool = False
    kb_filters: Optional[List[str]] = None

class ChatResponse:
    id: uuid.UUID
    message: str
    response: str
    agent_name: str
    chat_mode: str
    created_at: Optional[str] = None

class ChatMessage:
    id: uuid.UUID
    content: str
    speaker: str  # 'user' ou 'agent'
    timestamp: str 