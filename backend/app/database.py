"""
Módulo de database otimizado para Supabase como infraestrutura principal.
Remove redundâncias e foca na integração eficiente.
"""

import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# SUPABASE CLIENT (Infraestrutura Principal)
# =============================================================================

# Cliente Supabase global
supabase: Client = None

def get_supabase() -> Client:
    """Obter cliente Supabase configurado."""
    global supabase
    
    if not supabase:
        if not settings.supabase_url or not settings.supabase_anon_key:
            raise Exception("❌ Supabase não configurado. Configure SUPABASE_URL e SUPABASE_ANON_KEY")
        
        try:
            supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
            logger.info(f"✅ Supabase conectado: {settings.supabase_url}")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar Supabase: {e}")
            raise
    
    return supabase

# =============================================================================
# AUTHENTICATION (Delegado para Supabase)
# =============================================================================

def get_current_user():
    """Obter usuário atual autenticado via Supabase."""
    try:
        supabase = get_supabase()
        user = supabase.auth.get_user()
        return user.user if user else None
    except Exception as e:
        logger.warning(f"⚠️ Erro ao obter usuário atual: {e}")
        return None

def is_authenticated() -> bool:
    """Verificar se usuário está autenticado via Supabase."""
    return get_current_user() is not None

def get_user_tenant_id() -> Optional[str]:
    """Obter tenant_id do usuário atual via JWT."""
    try:
        supabase = get_supabase()
        user = supabase.auth.get_user()
        if user and user.user:
            # Extrair tenant_id do JWT ou metadata
            tenant_id = user.user.user_metadata.get('tenant_id')
            return tenant_id
    except Exception as e:
        logger.warning(f"⚠️ Erro ao obter tenant_id: {e}")
    return None

# =============================================================================
# DATABASE OPERATIONS (Otimizadas)
# =============================================================================

async def get_agent_by_id(agent_id: str, tenant_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Obter agente por ID com RLS automático do Supabase."""
    try:
        supabase = get_supabase()
        query = supabase.table('agents').select('*').eq('id', agent_id)
        
        # RLS do Supabase gerencia automaticamente o tenant_id
        response = query.execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao obter agente {agent_id}: {e}")
        return None

async def save_chat_message(
    user_id: str,
    agent_id: str,
    message: str,
    response: str,
    chat_mode: str = "UsoCotidiano"
) -> Optional[Dict[str, Any]]:
    """Salvar mensagem de chat via Supabase."""
    try:
        supabase = get_supabase()
        
        chat_data = {
            "user_id": user_id,
            "agent_id": agent_id,
            "message": message,
            "response": response,
            "chat_mode": chat_mode,
            "created_at": "now()"
        }
        
        response = supabase.table('chat_history').insert(chat_data).execute()
        
        if response.data:
            logger.info(f"✅ Mensagem salva: {response.data[0]['id']}")
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao salvar mensagem: {e}")
        return None

async def get_chat_history(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> list:
    """Obter histórico de chat via Supabase."""
    try:
        supabase = get_supabase()
        query = supabase.table('chat_history').select('*').order('created_at', desc=True)
        
        if user_id:
            query = query.eq('user_id', user_id)
        if agent_id:
            query = query.eq('agent_id', agent_id)
        
        query = query.range(offset, offset + limit - 1)
        response = query.execute()
        
        return response.data or []
    except Exception as e:
        logger.error(f"❌ Erro ao obter histórico: {e}")
        return []

# =============================================================================
# TENANT OPERATIONS (Simplificadas via RLS)
# =============================================================================

async def get_user_agents() -> list:
    """Obter agentes do usuário atual via RLS do Supabase."""
    try:
        supabase = get_supabase()
        response = supabase.table('agents').select('*').execute()
        return response.data or []
    except Exception as e:
        logger.error(f"❌ Erro ao obter agentes: {e}")
        return []

async def create_agent(agent_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Criar agente via Supabase (RLS gerencia tenant)."""
    try:
        supabase = get_supabase()
        response = supabase.table('agents').insert(agent_data).execute()
        
        if response.data:
            logger.info(f"✅ Agente criado: {response.data[0]['id']}")
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao criar agente: {e}")
        return None

# =============================================================================
# HEALTH CHECK
# =============================================================================

async def check_database_health() -> Dict[str, Any]:
    """Verificar saúde da conexão com Supabase."""
    try:
        supabase = get_supabase()
        
        # Teste simples de conexão (sem verificar tabelas)
        # Apenas verifica se consegue conectar ao Supabase
        response = supabase.auth.get_user()
        
        return {
            "status": "connected",
            "provider": "supabase",
            "url": settings.supabase_url,
            "connected": True,
            "tables_ready": False,  # Tabelas precisam ser criadas manualmente
            "timestamp": "now()"
        }
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return {
            "status": "unhealthy",
            "provider": "supabase",
            "error": str(e),
            "connected": False,
            "timestamp": "now()"
        } 