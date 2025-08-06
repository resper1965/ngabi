"""
Schemas para agentes - n.Gabi
Validação de dados para CRUD de agentes
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AgentBase(BaseModel):
    """Schema base para agentes."""
    name: str = Field(..., description="Nome do agente", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Descrição do agente", max_length=500)
    system_prompt: str = Field(..., description="Prompt do sistema", min_length=10)
    model: Optional[str] = Field("gpt-3.5-turbo", description="Modelo de IA a ser usado")
    temperature: Optional[float] = Field(0.7, description="Temperatura para geração", ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(2048, description="Máximo de tokens", ge=1, le=8192)
    is_active: Optional[bool] = Field(True, description="Se o agente está ativo")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")

class AgentCreate(AgentBase):
    """Schema para criação de agente."""
    pass

class AgentUpdate(BaseModel):
    """Schema para atualização de agente."""
    name: Optional[str] = Field(None, description="Nome do agente", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Descrição do agente", max_length=500)
    system_prompt: Optional[str] = Field(None, description="Prompt do sistema", min_length=10)
    model: Optional[str] = Field(None, description="Modelo de IA a ser usado")
    temperature: Optional[float] = Field(None, description="Temperatura para geração", ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, description="Máximo de tokens", ge=1, le=8192)
    is_active: Optional[bool] = Field(None, description="Se o agente está ativo")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")

class AgentResponse(AgentBase):
    """Schema para resposta de agente."""
    id: str = Field(..., description="ID único do agente")
    created_by: str = Field(..., description="ID do usuário que criou")
    created_at: str = Field(..., description="Data de criação")
    updated_at: str = Field(..., description="Data de atualização")
    
    class Config:
        from_attributes = True

class AgentList(BaseModel):
    """Schema para lista de agentes."""
    agents: List[AgentResponse] = Field(..., description="Lista de agentes")
    total: int = Field(..., description="Total de agentes")
    limit: int = Field(..., description="Limite por página")
    offset: int = Field(..., description="Offset da página")

class AgentTemplate(BaseModel):
    """Schema para template de agente."""
    id: str = Field(..., description="ID do template")
    name: str = Field(..., description="Nome do template")
    description: str = Field(..., description="Descrição do template")
    system_prompt: str = Field(..., description="Prompt do sistema")
    model: str = Field(..., description="Modelo de IA")
    temperature: float = Field(..., description="Temperatura")
    max_tokens: int = Field(..., description="Máximo de tokens")

class AgentTestRequest(BaseModel):
    """Schema para teste de agente."""
    test_message: str = Field(..., description="Mensagem de teste", min_length=1)

class AgentTestResponse(BaseModel):
    """Schema para resposta de teste de agente."""
    agent_id: str = Field(..., description="ID do agente")
    agent_name: str = Field(..., description="Nome do agente")
    test_message: str = Field(..., description="Mensagem de teste")
    response: str = Field(..., description="Resposta do agente")
    timestamp: str = Field(..., description="Timestamp do teste") 