"""
Router para gerenciamento de webhooks.
"""

from fastapi import APIRouter, HTTPException, Request, Query, Body
from typing import List, Optional, Dict, Any
import logging

from app.core.webhooks import webhook_system
from app.core.rate_limiting import get_tenant_id_from_request

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)

# =============================================================================
# ENDPOINTS DE WEBHOOKS
# =============================================================================

@router.post("/register")
async def register_webhook(
    event_type: str = Body(..., description="Tipo de evento a monitorar"),
    url: str = Body(..., description="URL para enviar o webhook"),
    secret: Optional[str] = Body(None, description="Secret para assinar o webhook"),
    http_request: Request = None
):
    """
    Registra um novo webhook para um tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        webhook = await webhook_system.register_webhook(
            tenant_id=tenant_id,
            event_type=event_type,
            url=url,
            secret=secret
        )
        
        if webhook:
            return {
                "message": "Webhook registrado com sucesso",
                "webhook": webhook,
                "tenant_id": tenant_id
            }
        else:
            raise HTTPException(status_code=500, detail="Falha ao registrar webhook")
            
    except Exception as e:
        logger.error(f"Erro ao registrar webhook: {e}")
        raise HTTPException(status_code=500, detail="Erro ao registrar webhook")

@router.delete("/unregister/{webhook_id}")
async def unregister_webhook(
    webhook_id: str,
    http_request: Request = None
):
    """
    Remove um webhook registrado.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        success = await webhook_system.unregister_webhook(webhook_id)
        
        if success:
            return {
                "message": "Webhook removido com sucesso",
                "webhook_id": webhook_id,
                "tenant_id": tenant_id
            }
        else:
            raise HTTPException(status_code=404, detail="Webhook não encontrado")
            
    except Exception as e:
        logger.error(f"Erro ao remover webhook: {e}")
        raise HTTPException(status_code=500, detail="Erro ao remover webhook")

@router.get("/list")
async def list_webhooks(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    http_request: Request = None
):
    """
    Lista webhooks de um tenant.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        webhooks = await webhook_system.get_webhooks(tenant_id, event_type)
        
        return {
            "webhooks": webhooks,
            "total": len(webhooks),
            "tenant_id": tenant_id,
            "event_type": event_type
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar webhooks: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar webhooks")

@router.post("/test")
async def test_webhook(
    url: str = Body(..., description="URL para testar"),
    secret: Optional[str] = Body(None, description="Secret para assinar"),
    http_request: Request = None
):
    """
    Testa uma URL de webhook.
    """
    tenant_id = get_tenant_id_from_request(http_request)
    
    try:
        result = await webhook_system.test_webhook(url, secret)
        
        return {
            "test_result": result,
            "tenant_id": tenant_id
        }
        
    except Exception as e:
        logger.error(f"Erro ao testar webhook: {e}")
        raise HTTPException(status_code=500, detail="Erro ao testar webhook")

@router.get("/events")
async def get_available_events():
    """
    Retorna lista de tipos de eventos disponíveis para webhooks.
    """
    try:
        from app.core.events import EventType
        
        return {
            "available_events": [e.value for e in EventType],
            "description": "Tipos de eventos que podem ser monitorados por webhooks"
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar eventos disponíveis: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar eventos")

# =============================================================================
# ENDPOINT PARA RECEBER WEBHOOKS (exemplo)
# =============================================================================

@router.post("/receive")
async def receive_webhook(
    payload: Dict[str, Any] = Body(...),
    x_ngabi_signature: Optional[str] = None
):
    """
    Endpoint para receber webhooks (exemplo de implementação).
    """
    try:
        # Verificar assinatura se fornecida
        if x_ngabi_signature:
            # TODO: Implementar verificação de assinatura
            logger.info(f"Webhook recebido com assinatura: {x_ngabi_signature}")
        
        # Processar webhook
        event_type = payload.get("event_type")
        data = payload.get("data", {})
        
        logger.info(f"Webhook recebido: {event_type}")
        logger.debug(f"Dados do webhook: {data}")
        
        # Aqui você pode implementar lógica específica para cada tipo de evento
        if event_type == "chat_message":
            # Processar mensagem de chat
            pass
        elif event_type == "user_login":
            # Processar login de usuário
            pass
        elif event_type == "error_occurred":
            # Processar erro
            pass
        
        return {
            "message": "Webhook recebido com sucesso",
            "event_type": event_type,
            "timestamp": payload.get("timestamp")
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar webhook") 