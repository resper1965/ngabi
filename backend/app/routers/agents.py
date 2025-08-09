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
    request: Request,
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
    from app.core.agent_specialists import AgentSpecialists
    
    # Templates básicos
    basic_templates = [
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
    
    # Templates especialistas
    specialist_templates = AgentSpecialists.get_specialist_templates()
    
    return {
        "basic_templates": basic_templates,
        "specialist_templates": specialist_templates,
        "categories": AgentSpecialists.get_categories()
    }

# =============================================================================
# SPECIALIST AGENTS
# =============================================================================

@router.get("/specialists")
async def get_specialist_agents():
    """
    Obter todos os agentes especialistas disponíveis.
    """
    from app.core.agent_specialists import AgentSpecialists
    
    specialists = AgentSpecialists.get_specialist_templates()
    return {
        "specialists": specialists,
        "total": len(specialists),
        "categories": AgentSpecialists.get_categories()
    }

@router.get("/specialists/category/{category}")
async def get_specialists_by_category(category: str):
    """
    Obter agentes especialistas por categoria.
    """
    from app.core.agent_specialists import AgentSpecialists
    
    specialists = AgentSpecialists.get_specialist_by_category(category)
    return {
        "category": category,
        "specialists": specialists,
        "total": len(specialists)
    }

@router.get("/specialists/{specialist_id}")
async def get_specialist_by_id(specialist_id: str):
    """
    Obter agente especialista específico por ID.
    """
    from app.core.agent_specialists import AgentSpecialists
    
    specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
    if not specialist:
        raise HTTPException(status_code=404, detail="Especialista não encontrado")
    
    return specialist

@router.post("/specialists/create")
async def create_specialist_agent(
    name: str,
    description: str,
    category: str,
    system_prompt: str,
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    metadata: Dict[str, Any] = None
):
    """
    Criar agente especialista customizado.
    """
    from app.core.agent_specialists import AgentSpecialists
    
    user = get_current_user()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    # Criar especialista customizado
    custom_specialist = AgentSpecialists.create_custom_specialist(
        name=name,
        description=description,
        category=category,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        metadata=metadata
    )
    
    # Salvar no banco de dados
    try:
        supabase = get_supabase()
        agent_data = {
            "id": custom_specialist["id"],
            "name": custom_specialist["name"],
            "description": custom_specialist["description"],
            "system_prompt": custom_specialist["system_prompt"],
            "model": custom_specialist["model"],
            "temperature": custom_specialist["temperature"],
            "max_tokens": custom_specialist["max_tokens"],
            "metadata": custom_specialist["metadata"],
            "created_by": user.id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        response = supabase.table('agents').insert(agent_data).execute()
        
        if response.data:
            logger.info(f"✅ Especialista customizado criado: {name}")
            return {
                "success": True,
                "specialist": custom_specialist,
                "message": "Especialista criado com sucesso"
            }
        else:
            raise HTTPException(status_code=500, detail="Erro ao salvar especialista")
            
    except Exception as e:
        logger.error(f"❌ Erro ao criar especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# LANGCHAIN INTEGRATION
# =============================================================================

@router.post("/specialists/{specialist_id}/langchain")
async def test_specialist_with_langchain(
    specialist_id: str,
    test_message: str,
    use_memory: bool = True
):
    """
    Testar agente especialista com LangChain.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se especialista existe
        from app.core.agent_specialists import AgentSpecialists
        specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
        
        if not specialist:
            raise HTTPException(status_code=404, detail="Especialista não encontrado")
        
        # Usar LangChain Service
        from app.services.langchain_service import langchain_service
        
        ai_response = await langchain_service.process_with_specialist_chain(
            specialist_id=specialist_id,
            message=test_message,
            use_memory=use_memory
        )
        
        return {
            "specialist_id": specialist_id,
            "specialist_name": specialist['name'],
            "test_message": test_message,
            "response": ai_response,
            "use_memory": use_memory,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao testar especialista com LangChain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/specialists/{specialist_id}/rag")
async def create_rag_for_specialist(
    specialist_id: str,
    documents: List[Dict[str, Any]],
    tenant_id: str
):
    """
    Criar chain RAG para especialista com documentos no Supabase.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se especialista existe
        from app.core.agent_specialists import AgentSpecialists
        specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
        
        if not specialist:
            raise HTTPException(status_code=404, detail="Especialista não encontrado")
        
        # Criar chain RAG com Supabase
        from app.services.langchain_service import langchain_service
        
        rag_chain = await langchain_service.create_rag_chain(
            specialist_id=specialist_id,
            documents=documents,
            tenant_id=tenant_id
        )
        
        return {
            "success": True,
            "specialist_id": specialist_id,
            "tenant_id": tenant_id,
            "documents_count": len(documents),
            "rag_chain_created": True,
            "supabase_storage": rag_chain.get("supabase_storage", {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar RAG para especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/specialists/{specialist_id}/rag/test")
async def test_rag_specialist(
    specialist_id: str,
    test_message: str,
    tenant_id: str
):
    """
    Testar especialista com RAG.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se especialista existe
        from app.core.agent_specialists import AgentSpecialists
        specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
        
        if not specialist:
            raise HTTPException(status_code=404, detail="Especialista não encontrado")
        
        # Testar com RAG
        from app.services.langchain_service import langchain_service
        
        ai_response = await langchain_service.process_with_rag_chain(
            specialist_id=specialist_id,
            message=test_message,
            tenant_id=tenant_id
        )
        
        return {
            "specialist_id": specialist_id,
            "specialist_name": specialist['name'],
            "test_message": test_message,
            "response": ai_response,
            "tenant_id": tenant_id,
            "rag_used": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao testar RAG para especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/langchain/chains")
async def get_langchain_chains():
    """
    Obter informações sobre chains LangChain disponíveis.
    """
    try:
        from app.services.langchain_service import langchain_service
        
        chains = langchain_service.get_available_chains()
        chains_info = {}
        
        for chain_id in chains:
            chain_info = langchain_service.get_chain_info(chain_id)
            if chain_info:
                chains_info[chain_id] = chain_info
        
        return {
            "chains": chains_info,
            "total_chains": len(chains),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter chains LangChain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/specialists/{specialist_id}/memory")
async def clear_specialist_memory(specialist_id: str):
    """
    Limpar memória de um especialista.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.services.langchain_service import langchain_service
        
        await langchain_service.clear_memory(specialist_id)
        
        return {
            "success": True,
            "specialist_id": specialist_id,
            "memory_cleared": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao limpar memória do especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/langchain/health")
async def langchain_health():
    """
    Health check do LangChain Service.
    """
    try:
        from app.services.langchain_service import langchain_service
        
        health_info = await langchain_service.health_check()
        
        return health_info
        
    except Exception as e:
        logger.error(f"❌ Erro no health check do LangChain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# SUPABASE VECTOR STORE ENDPOINTS
# =============================================================================

@router.get("/specialists/{specialist_id}/documents")
async def get_specialist_documents(
    specialist_id: str,
    tenant_id: str,
    limit: int = 100
):
    """
    Obter documentos de um especialista do Supabase.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        documents = await supabase_vectorstore.get_documents_for_specialist(
            specialist_id=specialist_id,
            tenant_id=tenant_id,
            limit=limit
        )
        
        return {
            "specialist_id": specialist_id,
            "tenant_id": tenant_id,
            "documents": documents,
            "total_documents": len(documents),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter documentos do especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/specialists/{specialist_id}/documents")
async def delete_specialist_documents(
    specialist_id: str,
    tenant_id: str
):
    """
    Deletar documentos de um especialista do Supabase.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        result = await supabase_vectorstore.delete_documents_for_specialist(
            specialist_id=specialist_id,
            tenant_id=tenant_id
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Erro ao deletar documentos do especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/specialists/{specialist_id}/stats")
async def get_specialist_stats(
    specialist_id: str,
    tenant_id: str
):
    """
    Obter estatísticas de documentos de um especialista.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        stats = await supabase_vectorstore.get_specialist_stats(
            specialist_id=specialist_id,
            tenant_id=tenant_id
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas do especialista: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/specialists/documents/overview")
async def get_specialists_with_documents():
    """
    Listar especialistas que possuem documentos armazenados.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        specialists = await supabase_vectorstore.list_specialists_with_documents()
        
        return {
            "specialists": specialists,
            "total_specialists": len(specialists),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar especialistas com documentos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vectorstore/health")
async def vectorstore_health():
    """
    Health check do Supabase Vector Store.
    """
    try:
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        health_info = await supabase_vectorstore.health_check()
        
        return health_info
        
    except Exception as e:
        logger.error(f"❌ Erro no health check do Vector Store: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# VOICE STYLE BASE ENDPOINTS
# =============================================================================

@router.post("/voice-style/initialize")
async def initialize_voice_style_base(
    organization_name: str = "Sua Organização",
    tenant_id: str = None
):
    """
    Inicializar base vetorial de estilo de voz da organização.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.core.voice_style_base import VoiceStyleBase
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        # Usar tenant_id se fornecido, senão usar organization_name
        if not tenant_id:
            tenant_id = organization_name.lower().replace(" ", "-")
        
        # Obter documentos de estilo de voz personalizados
        voice_documents = VoiceStyleBase.get_voice_style_documents(organization_name)
        
        # Armazenar no Supabase
        storage_result = await supabase_vectorstore.store_documents_for_specialist(
            specialist_id=VoiceStyleBase.VOICE_STYLE_SPECIALIST_ID,
            tenant_id=tenant_id,
            documents=voice_documents
        )
        
        return {
            "success": True,
            "specialist_id": VoiceStyleBase.VOICE_STYLE_SPECIALIST_ID,
            "badge": VoiceStyleBase.get_voice_style_badge(),
            "organization_name": organization_name,
            "tenant_id": tenant_id,
            "documents_stored": len(voice_documents),
            "storage_result": storage_result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar base de estilo de voz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voice-style/specialist")
async def get_voice_style_specialist(organization_name: str = "Sua Organização"):
    """
    Obter configuração do especialista de estilo de voz da organização.
    """
    try:
        from app.core.voice_style_base import VoiceStyleBase
        
        specialist = VoiceStyleBase.get_voice_style_specialist(organization_name)
        
        return {
            "specialist": specialist,
            "badge": VoiceStyleBase.get_voice_style_badge(),
            "organization_name": organization_name,
            "auto_integrate": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter especialista de estilo de voz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voice-style/documents")
async def get_voice_style_documents(tenant_id: str = None):
    """
    Obter documentos da base de estilo de voz da organização.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.core.voice_style_base import VoiceStyleBase
        from app.services.supabase_vectorstore import supabase_vectorstore
        
        # Usar tenant_id se fornecido, senão usar "brand" como fallback
        if not tenant_id:
            tenant_id = "brand"
        
        documents = await supabase_vectorstore.get_documents_for_specialist(
            specialist_id=VoiceStyleBase.VOICE_STYLE_SPECIALIST_ID,
            tenant_id=tenant_id,
            limit=100
        )
        
        return {
            "specialist_id": VoiceStyleBase.VOICE_STYLE_SPECIALIST_ID,
            "badge": VoiceStyleBase.get_voice_style_badge(),
            "tenant_id": tenant_id,
            "documents": documents,
            "total_documents": len(documents),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter documentos de estilo de voz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice-style/test")
async def test_voice_style_integration(
    test_message: str,
    organization_name: str = "Sua Organização",
    tenant_id: str = None
):
    """
    Testar integração de estilo de voz da organização.
    """
    try:
        user = get_current_user()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        from app.core.voice_style_base import VoiceStyleBase
        from app.services.langchain_service import langchain_service
        
        # Usar tenant_id se fornecido, senão usar organization_name
        if not tenant_id:
            tenant_id = organization_name.lower().replace(" ", "-")
        
        # Testar com especialista de estilo de voz
        response = await langchain_service.process_with_specialist_chain(
            specialist_id=VoiceStyleBase.VOICE_STYLE_SPECIALIST_ID,
            message=test_message,
            use_memory=False,
            tenant_id=tenant_id
        )
        
        return {
            "specialist_id": VoiceStyleBase.VOICE_STYLE_SPECIALIST_ID,
            "badge": VoiceStyleBase.get_voice_style_badge(),
            "organization_name": organization_name,
            "tenant_id": tenant_id,
            "test_message": test_message,
            "response": response,
            "auto_integration": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao testar estilo de voz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# AGENT TESTING
# =============================================================================

@router.post("/{agent_id}/test")
async def test_agent(agent_id: str, test_message: str, tenant_id: str = None):
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
        
        # Verificar se é um agente especialista
        from app.core.agent_specialists import AgentSpecialists
        from app.core.voice_style_base import VoiceStyleBase
        
        specialist = AgentSpecialists.get_specialist_by_id(agent_id)
        
        if specialist:
            # Usar LangChain para especialistas
            from app.services.langchain_service import langchain_service
            
            ai_response = await langchain_service.process_with_specialist_chain(
                specialist_id=agent_id,
                message=test_message,
                use_memory=True,
                tenant_id=tenant_id
            )
            
            # Verificar se tem badge especial
            badge = specialist.get("metadata", {}).get("badge", "")
            if not badge and VoiceStyleBase.is_voice_style_specialist(agent_id):
                badge = VoiceStyleBase.get_voice_style_badge()
            
            logger.info(f"✅ Agente especialista testado com LangChain: {agent_id}")
        else:
            # Usar LLMService para agentes básicos
            from app.core.llm_service import get_llm_service
            
            ai_response = await get_llm_service().process_chat_message(
                message=test_message,
                system_prompt=agent['system_prompt'],
                model=agent.get('model', settings.default_chat_model),
                temperature=agent.get('temperature', settings.temperature),
                max_tokens=agent.get('max_tokens', settings.max_tokens)
            )
            
            badge = ""
            logger.info(f"✅ Agente básico testado com LLMService: {agent_id}")
        
        return {
            "agent_id": agent_id,
            "agent_name": agent['name'],
            "badge": badge,
            "tenant_id": tenant_id,
            "test_message": test_message,
            "response": ai_response,
            "timestamp": datetime.utcnow().isoformat(),
            "langchain_used": specialist is not None,
            "voice_style_applied": specialist is not None and not VoiceStyleBase.is_voice_style_specialist(agent_id)
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