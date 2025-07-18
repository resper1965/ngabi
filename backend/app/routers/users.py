from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

class User(BaseModel):
    id: str
    email: str
    name: str
    tenant_id: str
    role: str
    active: bool = True

class UserCreate(BaseModel):
    email: str
    name: str
    tenant_id: str
    role: str = "user"
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Cria um novo usuário"""
    try:
        # TODO: Implementar criação no banco de dados com hash da senha
        return User(
            id="user_123",
            email=user.email,
            name=user.name,
            tenant_id=user.tenant_id,
            role=user.role
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Obtém informações de um usuário"""
    # TODO: Implementar busca no banco de dados
    return User(
        id=user_id,
        email="usuario@exemplo.com",
        name="Usuário Exemplo",
        tenant_id="tenant_123",
        role="user"
    )

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate):
    """Atualiza um usuário"""
    # TODO: Implementar atualização no banco de dados
    return User(
        id=user_id,
        email="usuario@exemplo.com",
        name=user_update.name or "Usuário Exemplo",
        tenant_id="tenant_123",
        role=user_update.role or "user"
    )

@router.get("/tenant/{tenant_id}")
async def get_users_by_tenant(tenant_id: str):
    """Lista usuários de um tenant"""
    # TODO: Implementar busca no banco de dados
    return [
        User(
            id="user_123",
            email="usuario@exemplo.com",
            name="Usuário Exemplo",
            tenant_id=tenant_id,
            role="user"
        )
    ] 