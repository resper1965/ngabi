"""
Service de LLM/OpenAI para o n.Gabi
Integração com OpenAI API para processamento de chat
"""

import asyncio
import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.cache import get_cached_response, set_cached_response

logger = logging.getLogger(__name__)

class LLMService:
    """Service para integração com OpenAI e outros LLMs."""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa o cliente OpenAI."""
        try:
            api_key = self._get_openai_api_key()
            if not api_key:
                logger.warning("⚠️ OpenAI API key não encontrada")
                return
            
            self.client = AsyncOpenAI(api_key=api_key)
            logger.info("✅ Cliente OpenAI inicializado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar OpenAI: {e}")
            self.client = None
    
    def _get_openai_api_key(self) -> Optional[str]:
        """Recupera a chave da API OpenAI diretamente do .env."""
        # Usar diretamente variável de ambiente
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            logger.info("✅ OpenAI API key obtida do .env")
            return api_key
        
        # Fallback para settings
        api_key = settings.openai_api_key
        if api_key:
            logger.info("✅ OpenAI API key obtida das settings")
            return api_key
        
        logger.warning("⚠️ OpenAI API key não encontrada")
        return None
    
    async def process_chat_message(
        self,
        message: str,
        system_prompt: str,
        chat_history: List[Dict[str, str]] = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        tenant_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Processa uma mensagem de chat usando OpenAI.
        
        Args:
            message: Mensagem do usuário
            system_prompt: Prompt do sistema
            chat_history: Histórico da conversa
            model: Modelo a ser usado
            temperature: Temperatura para geração
            max_tokens: Máximo de tokens
            tenant_id: Identificador do tenant (para cache)
            agent_id: Identificador do agente (para cache)
            **kwargs: Parâmetros adicionais
        
        Returns:
            Resposta gerada pela IA
        """
        if not self.client:
            return self._fallback_response(message)
        
        try:
            # Preparar mensagens
            messages = self._prepare_messages(message, system_prompt, chat_history)
            
            # Configurar parâmetros
            params = {
                "model": model or settings.default_chat_model,
                "messages": messages,
                "temperature": temperature or settings.temperature,
                "max_tokens": max_tokens or settings.max_tokens,
                **kwargs
            }
            
            # Verificar cache (quando houver contexto suficiente)
            cache_tenant = tenant_id or "global"
            cache_agent = agent_id or "llm"
            cached_entry = get_cached_response(cache_tenant, cache_agent, message)
            if cached_entry and isinstance(cached_entry, dict) and cached_entry.get("response"):
                logger.info("🎯 Cache hit para resposta de IA (service)")
                return cached_entry["response"]
            
            # Chamar OpenAI
            logger.info(f"🤖 Chamando OpenAI: {params['model']}")
            response = await self.client.chat.completions.create(**params)
            
            ai_response = response.choices[0].message.content
            
            # Cache da resposta
            set_cached_response(cache_tenant, cache_agent, message, ai_response, ttl=3600)
            
            logger.info(f"✅ Resposta gerada: {len(ai_response)} chars")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar mensagem: {e}")
            return self._fallback_response(message)
    
    async def process_chat_stream(
        self,
        message: str,
        system_prompt: str,
        chat_history: List[Dict[str, str]] = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        tenant_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        **kwargs
    ):
        """
        Processa mensagem em streaming.
        
        Yields:
            Chunks da resposta em streaming
        """
        if not self.client:
            yield self._fallback_response(message)
            return
        
        try:
            messages = self._prepare_messages(message, system_prompt, chat_history)
            
            params = {
                "model": model or settings.default_chat_model,
                "messages": messages,
                "temperature": temperature or settings.temperature,
                "max_tokens": max_tokens or settings.max_tokens,
                "stream": True,
                **kwargs
            }
            
            logger.info(f"🤖 Streaming OpenAI: {params['model']}")
            
            async for chunk in self.client.chat.completions.create(**params):
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"❌ Erro no streaming: {e}")
            yield self._fallback_response(message)
    
    def _prepare_messages(
        self,
        message: str,
        system_prompt: str,
        chat_history: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        """Prepara as mensagens para enviar ao OpenAI."""
        messages = []
        
        # Adicionar prompt do sistema
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Adicionar histórico
        if chat_history:
            for hist in chat_history[-10:]:  # Últimas 10 mensagens
                if "user" in hist:
                    messages.append({
                        "role": "user",
                        "content": hist["user"]
                    })
                if "assistant" in hist:
                    messages.append({
                        "role": "assistant",
                        "content": hist["assistant"]
                    })
        
        # Adicionar mensagem atual
        messages.append({
            "role": "user",
            "content": message
        })
        
        return messages
    
    def _generate_cache_key(self, message: str, system_prompt: str, params: Dict[str, Any]) -> str:
        """Gera chave de cache para a resposta."""
        import hashlib
        
        content = f"{message}:{system_prompt}:{params['model']}:{params['temperature']}"
        return f"llm_response:{hashlib.md5(content.encode()).hexdigest()}"
    
    def _fallback_response(self, message: str) -> str:
        """Resposta de fallback quando OpenAI não está disponível."""
        return f"Desculpe, estou temporariamente indisponível. Sua mensagem foi: '{message}'. Por favor, tente novamente em alguns instantes."
    
    async def test_connection(self) -> bool:
        """Testa a conexão com OpenAI."""
        if not self.client:
            return False
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Teste"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"❌ Teste de conexão falhou: {e}")
            return False

# Função para obter instância do service (lazy loading)
_llm_service_instance = None

def get_llm_service() -> LLMService:
    """Retorna a instância do LLMService (singleton)."""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance 