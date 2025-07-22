"""
Sistema de webhooks para n.Gabi.
Permite enviar notificações para URLs externas quando eventos acontecem.
"""

import asyncio
import logging
import httpx
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.database import get_supabase

logger = logging.getLogger(__name__)

class WebhookSystem:
    """
    Sistema de webhooks para enviar notificações externas.
    """
    
    def __init__(self):
        self.supabase = get_supabase()
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def register_webhook(self, tenant_id: str, event_type: str, url: str, secret: Optional[str] = None):
        """
        Registra um webhook para um tenant e tipo de evento.
        
        Args:
            tenant_id: ID do tenant
            event_type: Tipo de evento a ser monitorado
            url: URL para onde enviar o webhook
            secret: Secret para assinar o webhook (opcional)
        """
        try:
            webhook_data = {
                "tenant_id": tenant_id,
                "event_type": event_type,
                "url": url,
                "secret": secret,
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
            
            response = self.supabase.table("webhooks").insert(webhook_data).execute()
            
            if response.data:
                logger.info(f"Webhook registrado: {event_type} -> {url}")
                return response.data[0]
            else:
                logger.error("Falha ao registrar webhook")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao registrar webhook: {e}")
            return None
    
    async def unregister_webhook(self, webhook_id: str):
        """
        Remove um webhook registrado.
        
        Args:
            webhook_id: ID do webhook
        """
        try:
            response = self.supabase.table("webhooks").delete().eq("id", webhook_id).execute()
            
            if response.data:
                logger.info(f"Webhook removido: {webhook_id}")
                return True
            else:
                logger.error("Falha ao remover webhook")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao remover webhook: {e}")
            return False
    
    async def get_webhooks(self, tenant_id: str, event_type: Optional[str] = None):
        """
        Lista webhooks de um tenant.
        
        Args:
            tenant_id: ID do tenant
            event_type: Tipo de evento (opcional)
        """
        try:
            query = self.supabase.table("webhooks").select("*").eq("tenant_id", tenant_id).eq("is_active", True)
            
            if event_type:
                query = query.eq("event_type", event_type)
            
            response = query.execute()
            return response.data
            
        except Exception as e:
            logger.error(f"Erro ao listar webhooks: {e}")
            return []
    
    async def send_webhook(self, webhook_data: Dict[str, Any], event_data: Dict[str, Any]):
        """
        Envia webhook para uma URL específica.
        
        Args:
            webhook_data: Dados do webhook (URL, secret, etc.)
            event_data: Dados do evento
        """
        try:
            url = webhook_data["url"]
            secret = webhook_data.get("secret")
            
            # Preparar payload
            payload = {
                "event_type": event_data.get("event_type"),
                "timestamp": datetime.now().isoformat(),
                "data": event_data,
                "webhook_id": webhook_data.get("id")
            }
            
            # Adicionar assinatura se houver secret
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "nGabi-Webhook/1.0"
            }
            
            if secret:
                import hmac
                import hashlib
                signature = hmac.new(
                    secret.encode(),
                    str(payload).encode(),
                    hashlib.sha256
                ).hexdigest()
                headers["X-nGabi-Signature"] = f"sha256={signature}"
            
            # Enviar webhook
            response = await self.client.post(url, json=payload, headers=headers)
            
            # Log do resultado
            if response.status_code in [200, 201, 202]:
                logger.info(f"Webhook enviado com sucesso: {url}")
                return True
            else:
                logger.warning(f"Webhook falhou: {url} - Status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar webhook: {e}")
            return False
    
    async def process_event_webhooks(self, event_type: str, event_data: Dict[str, Any]):
        """
        Processa webhooks para um evento específico.
        
        Args:
            event_type: Tipo do evento
            event_data: Dados do evento
        """
        tenant_id = event_data.get("tenant_id")
        if not tenant_id:
            logger.warning("Evento sem tenant_id, ignorando webhooks")
            return
        
        try:
            # Buscar webhooks para este evento
            webhooks = await self.get_webhooks(tenant_id, event_type)
            
            if not webhooks:
                return
            
            # Enviar webhooks em paralelo
            tasks = []
            for webhook in webhooks:
                task = asyncio.create_task(self.send_webhook(webhook, event_data))
                tasks.append(task)
            
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Log dos resultados
                success_count = sum(1 for r in results if r is True)
                logger.info(f"Webhooks processados: {success_count}/{len(tasks)} sucessos")
                
        except Exception as e:
            logger.error(f"Erro ao processar webhooks: {e}")
    
    async def test_webhook(self, url: str, secret: Optional[str] = None):
        """
        Testa uma URL de webhook.
        
        Args:
            url: URL para testar
            secret: Secret para assinar (opcional)
        """
        try:
            test_data = {
                "event_type": "webhook_test",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "message": "Teste de webhook do n.Gabi",
                    "test": True
                }
            }
            
            webhook_data = {
                "url": url,
                "secret": secret,
                "id": "test"
            }
            
            success = await self.send_webhook(webhook_data, test_data)
            
            return {
                "success": success,
                "url": url,
                "timestamp": test_data["timestamp"]
            }
            
        except Exception as e:
            logger.error(f"Erro ao testar webhook: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()

# Instância global do sistema de webhooks
webhook_system = WebhookSystem() 