"""
Router para gerenciamento de agentes - n.Gabi
CRUD completo de agentes com multi-tenancy
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional, Dict, Any
import uuid
import logging
from datetime import datetime

from app.database import get_supabase, get_current_user
from app.core.rate_limiting import rate_limit_by_user
from app.core.events import event_system, EventType
from app.schemas.agents import AgentCreate, AgentUpdate, AgentResponse, AgentList
from app.core.config import settings

router = APIRouter(prefix="/agents", tags=["agents"])
logger = logging.getLogger(__name__)

# =============================================================================
# AGENT CRUD ENDPOINTS
# =============================================================================

@router.get("/", response_model=AgentList)
@rate_limit_by_user(settings.rate_limit_chat, "1 minute")
async def get_user_agents(
    limit: int = 50,
    offset: int = 0
):
    """
    Obter agentes do usuário via RLS do Supabase.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        supabase = get_supabase()
        response = supabase.table('agents').select('*').range(offset, offset + limit - 1).execute()
        
        agents = response.data or []
        
        # Contar total
        count_response = supabase.table('agents').select('count', count='exact').execute()
        total = count_response.count if hasattr(count_response, 'count') else len(agents)
        
        return AgentList(
            agents=agents,
            total=total,
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter agentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent_by_id_endpoint(agent_id: str):
    """
    Obter agente específico por ID.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        supabase = get_supabase()
        response = supabase.table('agents').select('*').eq('id', agent_id).single().execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        return AgentResponse(**response.data)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter agente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate):
    """
    Criar novo agente.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Preparar dados do agente
        agent_dict = agent_data.dict()
        agent_dict.update({
            "id": str(uuid.uuid4()),
            "created_by": user.id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        # Validações
        if not agent_dict.get('name'):
            raise HTTPException(status_code=400, detail="Nome do agente é obrigatório")
        
        if not agent_dict.get('system_prompt'):
            raise HTTPException(status_code=400, detail="Prompt do sistema é obrigatório")
        
        # Inserir via Supabase (RLS gerencia tenant)
        supabase = get_supabase()
        response = supabase.table('agents').insert(agent_dict).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Erro ao criar agente")
        
        created_agent = response.data[0]
        
        # Emitir evento
        await event_system.emit(EventType.AGENT_CREATED, {
            "user_id": user.id,
            "agent_id": created_agent['id'],
            "agent_name": created_agent['name']
        })
        
        logger.info(f"✅ Agente criado: {created_agent['id']} - {created_agent['name']}")
        return AgentResponse(**created_agent)
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar agente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_data: AgentUpdate):
    """
    Atualizar agente existente.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se agente existe
        supabase = get_supabase()
        existing = supabase.table('agents').select('*').eq('id', agent_id).single().execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Preparar dados para atualização
        update_data = agent_data.dict(exclude_unset=True)
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        # Atualizar via Supabase
        response = supabase.table('agents').update(update_data).eq('id', agent_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Erro ao atualizar agente")
        
        updated_agent = response.data[0]
        
        # Emitir evento
        await event_system.emit(EventType.AGENT_UPDATED, {
            "user_id": user.id,
            "agent_id": agent_id,
            "agent_name": updated_agent['name']
        })
        
        logger.info(f"✅ Agente atualizado: {agent_id}")
        return AgentResponse(**updated_agent)
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar agente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """
    Deletar agente.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se agente existe
        supabase = get_supabase()
        existing = supabase.table('agents').select('*').eq('id', agent_id).single().execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Deletar via Supabase
        response = supabase.table('agents').delete().eq('id', agent_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Erro ao deletar agente")
        
        # Emitir evento
        await event_system.emit(EventType.AGENT_DELETED, {
            "user_id": user.id,
            "agent_id": agent_id,
            "agent_name": existing.data['name']
        })
        
        logger.info(f"✅ Agente deletado: {agent_id}")
        return {"message": "Agente deletado com sucesso", "agent_id": agent_id}
        
    except Exception as e:
        logger.error(f"❌ Erro ao deletar agente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# AGENT TEMPLATES
# =============================================================================

@router.get("/templates")
async def get_agent_templates():
    """
    Obter templates de agentes pré-definidos.
    """
    templates = [
        {
            "id": "customer-support",
            "name": "Atendimento ao Cliente",
            "description": "Agente especializado em atendimento ao cliente",
            "system_prompt": "Você é um agente de atendimento ao cliente especializado em resolver problemas e dúvidas. Seja sempre cordial, profissional e eficiente.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 2048
        },
        {
            "id": "sales-assistant",
            "name": "Assistente de Vendas",
            "description": "Agente para auxiliar em vendas e prospecção",
            "system_prompt": "Você é um assistente de vendas experiente. Ajude a identificar necessidades, apresentar soluções e fechar negócios de forma ética.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.8,
            "max_tokens": 2048
        },
        {
            "id": "technical-support",
            "name": "Suporte Técnico",
            "description": "Agente para suporte técnico e troubleshooting",
            "system_prompt": "Você é um técnico especializado em resolver problemas técnicos. Use linguagem clara e forneça soluções passo a passo.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.5,
            "max_tokens": 2048
        }
    ]
    
    return {"templates": templates}

# =============================================================================
# AGENT TESTING
# =============================================================================

@router.post("/{agent_id}/test")
async def test_agent(agent_id: str, test_message: str):
    """
    Testar agente com uma mensagem.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Obter agente
        supabase = get_supabase()
        response = supabase.table('agents').select('*').eq('id', agent_id).single().execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        agent = response.data
        
        # Testar com LLM
        from app.core.llm_service import llm_service
        
        ai_response = await llm_service.process_chat_message(
            message=test_message,
            system_prompt=agent['system_prompt'],
            model=agent.get('model', settings.default_chat_model),
            temperature=agent.get('temperature', settings.temperature),
            max_tokens=agent.get('max_tokens', settings.max_tokens)
        )
        
        return {
            "agent_id": agent_id,
            "agent_name": agent['name'],
            "test_message": test_message,
            "response": ai_response,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao testar agente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@router.get("/health")
async def agents_health():
    """Health check do sistema de agentes."""
    return {
        "status": "healthy",
        "service": "agents",
        "timestamp": datetime.utcnow().isoformat()
    } 