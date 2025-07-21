from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import get_supabase, get_current_user, is_authenticated
from typing import Optional

router = APIRouter(prefix="/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class AuthResponse(BaseModel):
    user: dict
    session: dict
    message: str

@router.post("/login")
async def login(request: LoginRequest):
    """Login com email e senha"""
    try:
        supabase = get_supabase()
        
        # Fazer login
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if response.user:
            return AuthResponse(
                user=response.user.model_dump(),
                session=response.session.model_dump() if response.session else {},
                message="Login realizado com sucesso"
            )
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro no login: {str(e)}")

@router.post("/signup")
async def signup(request: SignupRequest):
    """Cadastro de novo usuário"""
    try:
        supabase = get_supabase()
        
        # Criar usuário
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "name": request.name
                }
            }
        })
        
        if response.user:
            return AuthResponse(
                user=response.user.model_dump(),
                session=response.session.model_dump() if response.session else {},
                message="Usuário criado com sucesso"
            )
        else:
            raise HTTPException(status_code=400, detail="Erro ao criar usuário")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no cadastro: {str(e)}")

@router.post("/logout")
async def logout():
    """Logout do usuário"""
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
        return {"message": "Logout realizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no logout: {str(e)}")

@router.get("/me")
async def get_current_user_info():
    """Obter informações do usuário atual"""
    user = get_current_user()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    return {
        "user": user.model_dump(),
        "authenticated": True
    }

@router.get("/check")
async def check_auth():
    """Verificar se usuário está autenticado"""
    return {
        "authenticated": is_authenticated(),
        "user": get_current_user().model_dump() if get_current_user() else None
    }

# Dependency para verificar autenticação
def require_auth():
    """Dependency para rotas que requerem autenticação"""
    if not is_authenticated():
        raise HTTPException(status_code=401, detail="Autenticação necessária")
    return get_current_user() 