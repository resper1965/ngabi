"""
Sistema de eventos híbrido para n.Gabi.
Combina processamento em tempo real com persistência seletiva de eventos críticos.
"""

import asyncio
import logging
from enum import Enum
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from app.database import get_supabase
from app.core.webhooks import webhook_system

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Tipos de eventos suportados pelo sistema"""
    CHAT_MESSAGE = "chat_message"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    AGENT_CREATED = "agent_created"
    AGENT_UPDATED = "agent_updated"
    AGENT_DELETED = "agent_deleted"
    TENANT_CREATED = "tenant_created"
    TENANT_UPDATED = "tenant_updated"
    ERROR_OCCURRED = "error_occurred"
    CACHE_CLEARED = "cache_cleared"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    WEBHOOK_SENT = "webhook_sent"
    NOTIFICATION_SENT = "notification_sent"

class EventSystem:
    """
    Sistema de eventos híbrido que combina processamento em tempo real
    com persistência seletiva de eventos críticos.
    """
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.supabase = get_supabase()
        self.persist_critical_events = True
        self._critical_events = {
            EventType.CHAT_MESSAGE,
            EventType.USER_LOGIN,
            EventType.USER_LOGOUT,
            EventType.AGENT_CREATED,
            EventType.AGENT_UPDATED,
            EventType.AGENT_DELETED,
            EventType.TENANT_CREATED,
            EventType.TENANT_UPDATED,
            EventType.ERROR_OCCURRED,
            EventType.RATE_LIMIT_EXCEEDED
        }
    
    def on(self, event_type: str):
        """
        Decorator para registrar listeners de eventos.
        
        Args:
            event_type: Tipo do evento a ser escutado
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable):
            if event_type not in self.listeners:
                self.listeners[event_type] = []
            self.listeners[event_type].append(func)
            logger.info(f"Listener registrado para evento: {event_type}")
            return func
        return decorator
    
    async def emit(self, event_type: str, data: Dict[str, Any], persist: Optional[bool] = None):
        """
        Emite um evento e processa todos os listeners registrados.
        
        Args:
            event_type: Tipo do evento
            data: Dados do evento
            persist: Se deve persistir o evento (None = automático)
        """
        try:
            # Adiciona metadados ao evento
            event_data = {
                **data,
                "event_type": event_type,
                "timestamp": datetime.now().isoformat(),
                "tenant_id": data.get("tenant_id"),
                "user_id": data.get("user_id")
            }
            
            # Decide se deve persistir
            should_persist = persist if persist is not None else self.should_persist_event(event_type)
            
            # Persiste se necessário
            if should_persist:
                await self.persist_event(event_data)
                logger.info(f"Evento persistido: {event_type}")
            
            # Processa listeners em paralelo
            await self.process_listeners(event_type, data)
            
            # Processa webhooks em background
            asyncio.create_task(webhook_system.process_event_webhooks(event_type, data))
            
            logger.info(f"Evento processado: {event_type}")
            
        except Exception as e:
            logger.error(f"Erro ao emitir evento {event_type}: {e}")
            # Emite evento de erro
            await self.emit_error("event_processing_error", {
                "original_event": event_type,
                "error": str(e),
                "data": data
            })
    
    async def persist_event(self, event_data: Dict[str, Any]):
        """
        Persiste evento no banco de dados.
        
        Args:
            event_data: Dados do evento a serem persistidos
        """
        try:
            # Prepara dados para persistência
            persist_data = {
                "event_type": event_data["event_type"],
                "data": event_data,
                "timestamp": event_data["timestamp"],
                "tenant_id": event_data.get("tenant_id"),
                "user_id": event_data.get("user_id"),
                "processed": False,
                "retry_count": 0
            }
            
            # Insere no banco
            response = self.supabase.table("events").insert(persist_data).execute()
            
            if response.data:
                logger.debug(f"Evento persistido com ID: {response.data[0]['id']}")
            else:
                logger.warning("Falha ao persistir evento - resposta vazia")
                
        except Exception as e:
            logger.error(f"Erro ao persistir evento: {e}")
            # Não falha a aplicação se a persistência falhar
    
    async def process_listeners(self, event_type: str, data: Dict[str, Any]):
        """
        Processa todos os listeners registrados para um evento.
        
        Args:
            event_type: Tipo do evento
            data: Dados do evento
        """
        if event_type not in self.listeners:
            return
        
        # Processa listeners em paralelo
        tasks = []
        for listener in self.listeners[event_type]:
            task = asyncio.create_task(self._safe_listener_call(listener, data))
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _safe_listener_call(self, listener: Callable, data: Dict[str, Any]):
        """
        Chama um listener de forma segura, capturando exceções.
        
        Args:
            listener: Função listener
            data: Dados do evento
        """
        try:
            if asyncio.iscoroutinefunction(listener):
                await listener(data)
            else:
                listener(data)
        except Exception as e:
            logger.error(f"Erro no listener {listener.__name__}: {e}")
            # Emite evento de erro do listener
            await self.emit_error("listener_error", {
                "listener": listener.__name__,
                "error": str(e),
                "data": data
            })
    
    def should_persist_event(self, event_type: str) -> bool:
        """
        Determina se um evento deve ser persistido.
        
        Args:
            event_type: Tipo do evento
            
        Returns:
            True se deve persistir, False caso contrário
        """
        return event_type in [e.value for e in self._critical_events]
    
    async def emit_error(self, error_type: str, error_data: Dict[str, Any]):
        """
        Emite evento de erro de forma segura.
        
        Args:
            error_type: Tipo do erro
            error_data: Dados do erro
        """
        try:
            # Sempre persiste erros
            await self.emit(EventType.ERROR_OCCURRED.value, {
                "error_type": error_type,
                "error_data": error_data,
                "timestamp": datetime.now().isoformat()
            }, persist=True)
        except Exception as e:
            logger.error(f"Erro ao emitir evento de erro: {e}")
    
    async def get_event_history(self, tenant_id: str, event_type: Optional[str] = None, limit: int = 100):
        """
        Recupera histórico de eventos de um tenant.
        
        Args:
            tenant_id: ID do tenant
            event_type: Tipo específico de evento (opcional)
            limit: Limite de eventos a retornar
            
        Returns:
            Lista de eventos
        """
        try:
            query = self.supabase.table("events").select("*").eq("tenant_id", tenant_id)
            
            if event_type:
                query = query.eq("event_type", event_type)
            
            response = query.order("timestamp", desc=True).limit(limit).execute()
            return response.data
            
        except Exception as e:
            logger.error(f"Erro ao recuperar histórico de eventos: {e}")
            return []
    
    async def reprocess_failed_events(self, max_retries: int = 3):
        """
        Reprocessa eventos que falharam.
        
        Args:
            max_retries: Número máximo de tentativas
        """
        try:
            # Busca eventos não processados
            response = self.supabase.table("events").select("*").eq("processed", False).lte("retry_count", max_retries).execute()
            
            for event in response.data:
                try:
                    # Reprocessa o evento
                    await self.process_listeners(event["data"]["event_type"], event["data"])
                    
                    # Marca como processado
                    self.supabase.table("events").update({
                        "processed": True,
                        "processed_at": datetime.now().isoformat()
                    }).eq("id", event["id"]).execute()
                    
                    logger.info(f"Evento reprocessado: {event['id']}")
                    
                except Exception as e:
                    # Incrementa contador de tentativas
                    retry_count = event.get("retry_count", 0) + 1
                    self.supabase.table("events").update({
                        "retry_count": retry_count,
                        "error_message": str(e)
                    }).eq("id", event["id"]).execute()
                    
                    logger.error(f"Erro ao reprocessar evento {event['id']}: {e}")
                    
        except Exception as e:
            logger.error(f"Erro ao reprocessar eventos falhados: {e}")
    
    def get_registered_events(self) -> List[str]:
        """
        Retorna lista de eventos que têm listeners registrados.
        
        Returns:
            Lista de tipos de eventos
        """
        return list(self.listeners.keys())
    
    def get_critical_events(self) -> List[str]:
        """
        Retorna lista de eventos críticos que são persistidos.
        
        Returns:
            Lista de tipos de eventos críticos
        """
        return [e.value for e in self._critical_events]

# Instância global do sistema de eventos
event_system = EventSystem()

# Listeners padrão para funcionalidades básicas
@event_system.on(EventType.ERROR_OCCURRED.value)
async def log_error_event(data: Dict[str, Any]):
    """Listener padrão para log de erros"""
    logger.error(f"Evento de erro: {data}")

@event_system.on(EventType.CHAT_MESSAGE.value)
async def log_chat_event(data: Dict[str, Any]):
    """Listener padrão para log de mensagens de chat"""
    logger.info(f"Chat message: User {data.get('user_id')} -> Agent {data.get('agent_id')}")

@event_system.on(EventType.USER_LOGIN.value)
async def log_user_login(data: Dict[str, Any]):
    """Listener padrão para log de login de usuário"""
    logger.info(f"User login: {data.get('user_id')} in tenant {data.get('tenant_id')}") 