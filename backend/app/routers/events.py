"""
Router para gerenciamento de eventos do sistema.
"""

from fastapi import APIRouter, HTTPException, Request, Query
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, timedelta

from app.core.events import event_system, EventType
from app.core.rate_limiting import get_tenant_id_from_request

router = APIRouter(prefix="/events", tags=["events"])
logger = logging.getLogger(__name__)

# =============================================================================
# ENDPOINTS DE EVENTOS
# =============================================================================

@router.get("/history")
async def get_events_history(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de eventos"),
    http_request: Request = None
):
    """
    Recupera histórico de eventos do tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        events = await event_system.get_event_history(
            tenant_id=tenant_id,
            event_type=event_type,
            limit=limit
        )
        
        return {
            "events": events,
            "total": len(events),
            "tenant_id": tenant_id,
            "event_type": event_type
        }
        
    except Exception as e:
        logger.error(f"Erro ao recuperar histórico de eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar eventos")

@router.get("/stats")
async def get_events_stats(
    days: int = Query(7, ge=1, le=30, description="Número de dias para análise"),
    http_request: Request = None
):
    """
    Retorna estatísticas de eventos do tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        # Buscar eventos dos últimos N dias
        from_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        events = await event_system.get_event_history(
            tenant_id=tenant_id,
            limit=1000  # Buscar mais eventos para estatísticas
        )
        
        # Filtrar por data
        recent_events = [
            event for event in events 
            if event.get("timestamp", "") >= from_date
        ]
        
        # Calcular estatísticas
        stats = {
            "total_events": len(recent_events),
            "events_by_type": {},
            "events_by_day": {},
            "error_count": 0,
            "chat_messages": 0,
            "user_logins": 0
        }
        
        for event in recent_events:
            event_type = event.get("event_type", "unknown")
            
            # Contar por tipo
            if event_type not in stats["events_by_type"]:
                stats["events_by_type"][event_type] = 0
            stats["events_by_type"][event_type] += 1
            
            # Contar por dia
            event_date = event.get("timestamp", "")[:10]  # YYYY-MM-DD
            if event_date not in stats["events_by_day"]:
                stats["events_by_day"][event_date] = 0
            stats["events_by_day"][event_date] += 1
            
            # Contadores específicos
            if event_type == EventType.ERROR_OCCURRED.value:
                stats["error_count"] += 1
            elif event_type == EventType.CHAT_MESSAGE.value:
                stats["chat_messages"] += 1
            elif event_type == EventType.USER_LOGIN.value:
                stats["user_logins"] += 1
        
        return {
            "stats": stats,
            "tenant_id": tenant_id,
            "period_days": days,
            "from_date": from_date
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas de eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao calcular estatísticas")

@router.post("/reprocess")
async def reprocess_failed_events(
    max_retries: int = Query(3, ge=1, le=10, description="Máximo de tentativas"),
    http_request: Request = None
):
    """
    Reprocessa eventos que falharam.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        await event_system.reprocess_failed_events(max_retries=max_retries)
        
        return {
            "message": "Reprocessamento de eventos iniciado",
            "tenant_id": tenant_id,
            "max_retries": max_retries
        }
        
    except Exception as e:
        logger.error(f"Erro ao reprocessar eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao reprocessar eventos")

@router.get("/types")
async def get_event_types():
    """
    Retorna lista de tipos de eventos disponíveis.
    """
    try:
        return {
            "available_events": [e.value for e in EventType],
            "critical_events": event_system.get_critical_events(),
            "registered_events": event_system.get_registered_events()
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar tipos de eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar tipos de eventos")

@router.post("/test")
async def test_event_system(
    event_type: str = Query(EventType.CHAT_MESSAGE.value, description="Tipo de evento para teste"),
    test_data: Dict[str, Any] = None,
    http_request: Request = None
):
    """
    Testa o sistema de eventos emitindo um evento de teste.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    if test_data is None:
        test_data = {
            "tenant_id": tenant_id,
            "user_id": "test-user-id",
            "message": "Teste do sistema de eventos",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # Emitir evento de teste
        await event_system.emit(event_type, test_data)
        
        return {
            "message": "Evento de teste emitido com sucesso",
            "event_type": event_type,
            "test_data": test_data,
            "tenant_id": tenant_id
        }
        
    except Exception as e:
        logger.error(f"Erro ao emitir evento de teste: {e}")
        raise HTTPException(status_code=500, detail="Erro ao emitir evento de teste")

@router.delete("/clear")
async def clear_events_history(
    event_type: Optional[str] = Query(None, description="Tipo de evento para limpar"),
    days_old: int = Query(30, ge=1, le=365, description="Limpar eventos mais antigos que N dias"),
    http_request: Request = None
):
    """
    Limpa histórico de eventos antigos.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        from app.database import get_supabase
        supabase = get_supabase()
        
        # Calcular data limite
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        
        # Construir query
        query = supabase.table("events").delete().eq("tenant_id", tenant_id).lt("timestamp", cutoff_date)
        
        if event_type:
            query = query.eq("event_type", event_type)
        
        response = query.execute()
        
        return {
            "message": "Histórico de eventos limpo",
            "tenant_id": tenant_id,
            "event_type": event_type,
            "cutoff_date": cutoff_date,
            "deleted_count": len(response.data) if response.data else 0
        }
        
    except Exception as e:
        logger.error(f"Erro ao limpar histórico de eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao limpar histórico")

# =============================================================================
# ENDPOINTS ADMIN (para administradores)
# =============================================================================

@router.get("/admin/all")
async def get_all_events(
    tenant_id: Optional[str] = Query(None, description="ID do tenant"),
    event_type: Optional[str] = Query(None, description="Tipo de evento"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de eventos"),
    http_request: Request = None
):
    """
    Endpoint admin para visualizar todos os eventos (sem filtro de tenant).
    """
    # TODO: Implementar verificação de admin
    try:
        from app.database import get_supabase
        supabase = get_supabase()
        
        query = supabase.table("events").select("*")
        
        if tenant_id:
            query = query.eq("tenant_id", tenant_id)
        
        if event_type:
            query = query.eq("event_type", event_type)
        
        response = query.order("timestamp", desc=True).limit(limit).execute()
        
        return {
            "events": response.data,
            "total": len(response.data),
            "filters": {
                "tenant_id": tenant_id,
                "event_type": event_type,
                "limit": limit
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao recuperar todos os eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar eventos") 