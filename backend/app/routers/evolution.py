"""
Router para integração com Evolution API (WhatsApp).
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/evolution", tags=["evolution"])

# Configuração da Evolution API
EVOLUTION_API_URL = "http://localhost:8080"
EVOLUTION_API_KEY = "NgabiEvolution2024!SecureKey"

@router.get("/health")
async def evolution_health():
    """Verificar saúde da Evolution API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{EVOLUTION_API_URL}/health")
            return {"status": "healthy", "evolution_api": response.json()}
    except Exception as e:
        logger.error(f"Erro ao verificar Evolution API: {e}")
        return {"status": "unhealthy", "error": str(e)}

@router.post("/webhook")
async def evolution_webhook(request: Request):
    """Webhook para receber eventos da Evolution API."""
    try:
        data = await request.json()
        logger.info(f"Webhook recebido: {data}")
        
        # Processar diferentes tipos de eventos
        event_type = data.get("event")
        
        if event_type == "messages.upsert":
            await process_message(data)
        elif event_type == "connection.update":
            await process_connection_update(data)
        elif event_type == "qrcode.updated":
            await process_qrcode_update(data)
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/instance/create")
async def create_instance(instance_name: str):
    """Criar nova instância do WhatsApp."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{EVOLUTION_API_URL}/instance/create",
                json={"instanceName": instance_name},
                headers={"apikey": EVOLUTION_API_KEY}
            )
            return response.json()
    except Exception as e:
        logger.error(f"Erro ao criar instância: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instance/{instance_name}/qr")
async def get_qr_code(instance_name: str):
    """Obter QR code para conectar WhatsApp."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{EVOLUTION_API_URL}/instance/connect/{instance_name}",
                headers={"apikey": EVOLUTION_API_KEY}
            )
            return response.json()
    except Exception as e:
        logger.error(f"Erro ao obter QR code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/instance/{instance_name}/send")
async def send_message(instance_name: str, message_data: Dict[str, Any]):
    """Enviar mensagem via WhatsApp."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{EVOLUTION_API_URL}/message/sendText/{instance_name}",
                json=message_data,
                headers={"apikey": EVOLUTION_API_KEY}
            )
            return response.json()
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_message(data: Dict[str, Any]):
    """Processar mensagem recebida."""
    try:
        messages = data.get("data", [])
        for message in messages:
            # Extrair informações da mensagem
            key = message.get("key", {})
            message_content = message.get("message", {})
            
            # Log da mensagem
            logger.info(f"Mensagem recebida: {key.get('remoteJid')} - {message_content}")
            
            # Aqui você pode integrar com a lógica do n.Gabi
            # Por exemplo, processar com IA, salvar no banco, etc.
            
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")

async def process_connection_update(data: Dict[str, Any]):
    """Processar atualização de conexão."""
    try:
        connection_data = data.get("data", {})
        state = connection_data.get("state")
        logger.info(f"Status da conexão: {state}")
        
        # Aqui você pode atualizar o status no banco de dados
        
    except Exception as e:
        logger.error(f"Erro ao processar atualização de conexão: {e}")

async def process_qrcode_update(data: Dict[str, Any]):
    """Processar atualização do QR code."""
    try:
        qr_data = data.get("data", {})
        qr_code = qr_data.get("qrcode")
        logger.info(f"QR Code atualizado: {qr_code[:50]}...")
        
        # Aqui você pode salvar o QR code ou notificar o frontend
        
    except Exception as e:
        logger.error(f"Erro ao processar QR code: {e}")

@router.get("/instances")
async def list_instances():
    """Listar todas as instâncias."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{EVOLUTION_API_URL}/instance/fetchInstances",
                headers={"apikey": EVOLUTION_API_KEY}
            )
            return response.json()
    except Exception as e:
        logger.error(f"Erro ao listar instâncias: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/instance/{instance_name}")
async def delete_instance(instance_name: str):
    """Deletar instância."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{EVOLUTION_API_URL}/instance/delete/{instance_name}",
                headers={"apikey": EVOLUTION_API_KEY}
            )
            return response.json()
    except Exception as e:
        logger.error(f"Erro ao deletar instância: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 