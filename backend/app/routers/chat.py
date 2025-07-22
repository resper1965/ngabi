"""
Router de chat otimizado - foca na lógica de IA e delega infraestrutura para Supabase.
Remove redundâncias e simplifica operações.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional, Dict, Any
import uuid
import logging
from datetime import datetime

from app.database import get_supabase, get_current_user, get_agent_by_id, save_chat_message, get_chat_history
from app.core.rate_limiting import rate_limit_by_user
from app.core.cache import get_cached_response, set_cached_response
from app.core.events import event_system, EventType
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

# =============================================================================
# CHAT ENDPOINTS (Foco na Lógica de IA)
# =============================================================================

@router.post("/", response_model=ChatResponse)
@rate_limit_by_user(settings.rate_limit_chat, "1 minute")
async def send_chat_message(
    request: ChatRequest,
    http_request: Request
):
    """
    Envia mensagem de chat com foco na lógica de IA.
    Rate limit: Configurável por usuário.
    Cache: Apenas para respostas de IA.
    """
    try:
        # Obter usuário atual
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar cache para resposta de IA
        cache_key = f"ai_response:{user.id}:{request.agent_id}:{hash(request.message)}"
        cached_response = get_cached_response(cache_key)
        
        if cached_response:
            logger.info(f"🎯 Cache hit para usuário {user.id}")
            return ChatResponse(**cached_response)
        
        # Obter agente via Supabase (RLS automático)
        agent = await get_agent_by_id(str(request.agent_id))
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Processar mensagem com IA (foco principal do n.Gabi)
        ai_response = await _process_ai_message(request, agent)
        
        # Criar resposta
        chat_response = ChatResponse(
            id=uuid.uuid4(),
            message=request.message,
            response=ai_response,
            agent_name=agent['name'],
            chat_mode=request.chat_mode,
            created_at=datetime.utcnow().isoformat()
        )
        
        # Cache da resposta de IA
        set_cached_response(cache_key, chat_response.dict(), ttl=settings.cache_ttl)
        
        # Salvar no histórico via Supabase (background)
        await save_chat_message(
            user_id=user.id,
            agent_id=str(request.agent_id),
            message=request.message,
            response=ai_response,
            chat_mode=request.chat_mode
        )
        
        # Emitir evento
        await event_system.emit(EventType.CHAT_MESSAGE, {
            "user_id": user.id,
            "agent_id": str(request.agent_id),
            "message": request.message,
            "response": ai_response,
            "chat_mode": request.chat_mode
        })
        
        logger.info(f"✅ Chat processado: {user.id} -> {agent['name']}")
        return chat_response
        
    except Exception as e:
        logger.error(f"❌ Erro no chat: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

@router.post("/stream")
@rate_limit_by_user(settings.rate_limit_chat, "1 minute")
async def stream_chat_message(
    request: ChatRequest,
    http_request: Request
):
    """
    Chat em streaming - foco na experiência em tempo real.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        agent = await get_agent_by_id(str(request.agent_id))
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Implementar streaming de IA
        # TODO: Implementar streaming real com OpenAI ou similar
        return {
            "message": "Streaming implementado",
            "agent": agent['name'],
            "mode": request.chat_mode
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no streaming: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_chat_history_endpoint(
    agent_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Obter histórico de chat via Supabase.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        history = await get_chat_history(
            user_id=user.id,
            agent_id=agent_id,
            limit=limit,
            offset=offset
        )
        
        return {
            "history": history,
            "total": len(history),
            "user_id": user.id
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter histórico: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents")
async def get_user_agents():
    """
    Obter agentes do usuário via RLS do Supabase.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        supabase = get_supabase()
        response = supabase.table('agents').select('*').execute()
        
        return {
            "agents": response.data or [],
            "total": len(response.data or [])
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter agentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents")
async def create_agent(agent_data: Dict[str, Any]):
    """
    Criar agente via Supabase (RLS gerencia tenant).
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Adicionar dados do usuário
        agent_data.update({
            "created_by": user.id,
            "created_at": "now()"
        })
        
        supabase = get_supabase()
        response = supabase.table('agents').insert(agent_data).execute()
        
        if response.data:
            logger.info(f"✅ Agente criado: {response.data[0]['id']}")
            return response.data[0]
        else:
            raise HTTPException(status_code=400, detail="Erro ao criar agente")
            
    except Exception as e:
        logger.error(f"❌ Erro ao criar agente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# AI PROCESSING (Foco Principal do n.Gabi)
# =============================================================================

async def _process_ai_message(request: ChatRequest, agent: Dict[str, Any]) -> str:
    """
    Processar mensagem com IA - foco principal do n.Gabi.
    """
    try:
        # Obter configurações do agente
        system_prompt = agent.get('system_prompt', '')
        model = agent.get('model', settings.default_chat_model)
        temperature = agent.get('temperature', settings.temperature)
        max_tokens = agent.get('max_tokens', settings.max_tokens)
        
        # Preparar contexto
        context = {
            "message": request.message,
            "chat_mode": request.chat_mode,
            "system_prompt": system_prompt,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "kb_filters": request.kb_filters or []
        }
        
        # TODO: Implementar chamada real para IA
        # Por enquanto, simular resposta
        ai_response = f"Resposta do agente {agent['name']} (modo {request.chat_mode}): {request.message}"
        
        logger.info(f"🤖 IA processada: {agent['name']} -> {len(ai_response)} chars")
        return ai_response
        
    except Exception as e:
        logger.error(f"❌ Erro no processamento de IA: {e}")
        return f"Desculpe, ocorreu um erro no processamento: {str(e)}"

# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@router.get("/health")
async def chat_health():
    """Health check do sistema de chat."""
    return {
        "status": "healthy",
        "service": "chat",
        "ai_model": settings.default_chat_model,
        "rate_limit": settings.rate_limit_chat,
        "cache_enabled": settings.cache_enabled,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/stats")
async def get_chat_stats():
    """Estatísticas do sistema de chat."""
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Obter estatísticas via Supabase
        supabase = get_supabase()
        
        # Total de mensagens
        messages_response = supabase.table('chat_history').select('count', count='exact').eq('user_id', user.id).execute()
        total_messages = messages_response.count if hasattr(messages_response, 'count') else 0
        
        # Total de agentes
        agents_response = supabase.table('agents').select('count', count='exact').execute()
        total_agents = agents_response.count if hasattr(agents_response, 'count') else 0
        
        return {
            "user_id": user.id,
            "total_messages": total_messages,
            "total_agents": total_agents,
            "ai_model": settings.default_chat_model,
            "rate_limit": settings.rate_limit_chat
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter stats: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 