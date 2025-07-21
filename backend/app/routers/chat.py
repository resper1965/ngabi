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
@chat_rate_limit  # 10 requisições por minuto por tenant
@cache_response(ttl=3600)  # Cache por 1 hora
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
        chat_history = ChatHistory(
            tenant_id=uuid.UUID(tenant_id),
            user_id=request.user_id,
            agent_id=request.agent_id,
            message=request.message,
            response=response_text,
            chat_mode=request.chat_mode,
            use_author_voice=request.use_author_voice
        )
        
        db.add(chat_history)
        db.commit()
        db.refresh(chat_history)
        
        # Atualizar ID da resposta com o ID real do histórico
        chat_response.id = chat_history.id
        chat_response.created_at = chat_history.created_at
        
    except Exception as e:
        logger.error(f"Erro ao salvar no histórico: {e}")
        # Não falhar a requisição se o histórico falhar
    
    return chat_response

@router.post("/stream")
@rate_limit_by_tenant(5, "1 minute")  # 5 requisições por minuto por tenant
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
@rate_limit_by_tenant(2, "1 minute")  # 2 requisições por minuto por tenant
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

# =============================================================================
# ENDPOINTS COM RATE LIMITING POR USUÁRIO
# =============================================================================

@router.post("/user-chat")
@rate_limit_by_user(20, "1 minute")  # 20 requisições por minuto por usuário
async def user_chat_message(
    request: ChatRequest,
    http_request: Request
):
    """
    Chat específico por usuário.
    Rate limit: 20 requisições por minuto por usuário.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    user_id = http_request.headers.get("X-User-ID")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header é obrigatório")
    
    # Implementar lógica de chat por usuário
    return ChatResponse(
        id=uuid.uuid4(),
        message=request.message,
        response=f"Resposta para usuário {user_id}: {request.message}",
        agent_name="User Agent",
        chat_mode=request.chat_mode,
        created_at=None
    )

# =============================================================================
# ENDPOINTS COM RATE LIMITING DINÂMICO
# =============================================================================

@router.post("/role-based-chat")
async def role_based_chat(
    request: ChatRequest,
    http_request: Request
):
    """
    Chat com rate limiting baseado no papel do usuário.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    user_role = http_request.headers.get("X-User-Role", "user")
    
    # Aplicar rate limit baseado no papel
    rate_limit_decorator = get_rate_limit_by_role(user_role)
    
    # Executar com rate limiting dinâmico
    return await rate_limit_decorator(lambda: _process_role_chat(request, user_role))()

async def _process_role_chat(request: ChatRequest, role: str):
    """Função auxiliar para processar chat baseado em papel."""
    return ChatResponse(
        id=uuid.uuid4(),
        message=request.message,
        response=f"Resposta para {role}: {request.message}",
        agent_name=f"{role.title()} Agent",
        chat_mode=request.chat_mode,
        created_at=None
    )

# =============================================================================
# ENDPOINTS DE MONITORAMENTO
# =============================================================================

@router.get("/rate-limit-stats")
async def get_chat_rate_limit_stats(http_request: Request):
    """
    Retorna estatísticas de rate limiting para o tenant atual.
    """
    return get_rate_limit_stats(http_request)

@router.get("/history")
@rate_limit_by_tenant(50, "1 minute")  # 50 requisições por minuto por tenant
async def get_chat_history(
    limit: int = 10,
    offset: int = 0,
    http_request: Request = None
):
    """
    Retorna histórico de chat.
    Rate limit: 50 requisições por minuto por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    chat_repo = BaseRepository(ChatHistory, db, tenant_id)
    chats = chat_repo.get_multi(limit=limit, offset=offset)
    
    return {
        "chats": [
            {
                "id": chat.id,
                "message": chat.message,
                "response": chat.response,
                "chat_mode": chat.chat_mode,
                "created_at": chat.created_at
            }
            for chat in chats
        ],
        "total": len(chats)
    }

# =============================================================================
# ENDPOINTS DE TESTE
# =============================================================================

@router.get("/test-rate-limit")
@rate_limit_by_tenant(3, "1 minute")  # 3 requisições por minuto por tenant
async def test_rate_limit(http_request: Request):
    """
    Endpoint para testar rate limiting.
    Rate limit: 3 requisições por minuto por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    return {
        "message": "Rate limit testado com sucesso",
        "tenant_id": tenant_id,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.post("/test-different-limits")
@rate_limit_by_tenant(5, "30 seconds")  # 5 requisições por 30 segundos
async def test_different_limits(http_request: Request):
    """
    Teste com diferentes limites de tempo.
    Rate limit: 5 requisições por 30 segundos por tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    return {
        "message": "Teste com limite de 30 segundos",
        "tenant_id": tenant_id,
        "limit": "5/30 seconds"
    }

# =============================================================================
# ENDPOINTS DE CACHE
# =============================================================================

@router.get("/cache/stats")
async def get_chat_cache_stats(http_request: Request):
    """
    Retorna estatísticas do cache de chat.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    stats = get_cache_stats(tenant_id)
    stats["endpoint"] = "/chat/cache/stats"
    
    return stats

@router.get("/cache/health")
async def get_cache_health():
    """
    Verifica saúde da conexão Redis.
    """
    health = cache_health_check()
    return health

@router.delete("/cache/clear")
async def clear_chat_cache(http_request: Request):
    """
    Limpa cache de chat do tenant atual.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID é obrigatório")
    
    deleted_keys = clear_tenant_cache(tenant_id)
    
    return {
        "message": f"Cache limpo para tenant {tenant_id}",
        "deleted_keys": deleted_keys,
        "tenant_id": tenant_id
    }

@router.post("/cache/test")
@cache_response(ttl=300)  # Cache por 5 minutos
async def test_cache_functionality(
    request: dict,
    http_request: Request
):
    """
    Endpoint para testar funcionalidade de cache.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    agent_id = request.get("agent_id", "test-agent")
    message = request.get("message", "test message")
    
    # Simular processamento
    response = {
        "id": str(uuid.uuid4()),
        "message": message,
        "response": f"Resposta cacheada para: {message}",
        "agent_id": agent_id,
        "tenant_id": tenant_id,
        "cached": True,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return response

# =============================================================================
# ENDPOINTS DE ADMINISTRAÇÃO
# =============================================================================

@router.post("/admin/reset-limits")
async def admin_reset_rate_limits(http_request: Request):
    """
    Endpoint administrativo para resetar rate limits.
    Apenas para desenvolvimento/debugging.
    """
    from app.core.rate_limiting import reset_rate_limits
    
    # Verificar se é admin (implementar autenticação)
    user_role = http_request.headers.get("X-User-Role")
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    return reset_rate_limits(http_request)

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