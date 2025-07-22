"""
Router de autenticação otimizado - delega completamente para Supabase Auth.
Remove redundâncias e foca na integração eficiente.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.database import get_supabase, get_current_user, is_authenticated
import logging

router = APIRouter(prefix="/auth", tags=["authentication"])
logger = logging.getLogger(__name__)

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    tenant_id: Optional[str] = None

class AuthResponse(BaseModel):
    user: Dict[str, Any]
    session: Dict[str, Any]
    message: str

class UserProfile(BaseModel):
    id: str
    email: str
    name: Optional[str]
    tenant_id: Optional[str]
    role: Optional[str]
    created_at: str

# =============================================================================
# AUTHENTICATION ENDPOINTS (Delegados para Supabase)
# =============================================================================

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login via Supabase Auth."""
    try:
        supabase = get_supabase()
        
        # Delegar login para Supabase
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if response.user:
            logger.info(f"✅ Login realizado: {request.email}")
            return AuthResponse(
                user=response.user.model_dump(),
                session=response.session.model_dump() if response.session else {},
                message="Login realizado com sucesso"
            )
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
            
    except Exception as e:
        logger.error(f"❌ Erro no login: {e}")
        raise HTTPException(status_code=401, detail=f"Erro no login: {str(e)}")

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Cadastro via Supabase Auth."""
    try:
        supabase = get_supabase()
        
        # Preparar dados do usuário
        user_data = {
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "name": request.name,
                    "tenant_id": request.tenant_id,
                    "role": "user"  # Role padrão
                }
            }
        }
        
        # Delegar signup para Supabase
        response = supabase.auth.sign_up(user_data)
        
        if response.user:
            logger.info(f"✅ Usuário criado: {request.email}")
            return AuthResponse(
                user=response.user.model_dump(),
                session=response.session.model_dump() if response.session else {},
                message="Usuário criado com sucesso"
            )
        else:
            raise HTTPException(status_code=400, detail="Erro ao criar usuário")
            
    except Exception as e:
        logger.error(f"❌ Erro no signup: {e}")
        raise HTTPException(status_code=400, detail=f"Erro no cadastro: {str(e)}")

@router.post("/logout")
async def logout():
    """Logout via Supabase Auth."""
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
        logger.info("✅ Logout realizado")
        return {"message": "Logout realizado com sucesso"}
    except Exception as e:
        logger.error(f"❌ Erro no logout: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no logout: {str(e)}")

@router.get("/me", response_model=UserProfile)
async def get_current_user_info():
    """Obter perfil do usuário atual via Supabase."""
    user = get_current_user()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    try:
        # Obter dados completos do usuário
        user_data = user.model_dump()
        
        return UserProfile(
            id=user_data.get('id'),
            email=user_data.get('email'),
            name=user_data.get('user_metadata', {}).get('name'),
            tenant_id=user_data.get('user_metadata', {}).get('tenant_id'),
            role=user_data.get('user_metadata', {}).get('role', 'user'),
            created_at=user_data.get('created_at')
        )
    except Exception as e:
        logger.error(f"❌ Erro ao obter perfil: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter perfil")

@router.get("/check")
async def check_auth():
    """Verificar status de autenticação via Supabase."""
    try:
        user = get_current_user()
        return {
            "authenticated": user is not None,
            "user_id": user.id if user else None,
            "email": user.email if user else None
        }
    except Exception as e:
        logger.error(f"❌ Erro ao verificar auth: {e}")
        return {"authenticated": False, "error": str(e)}

# =============================================================================
# PASSWORD MANAGEMENT (Delegado para Supabase)
# =============================================================================

@router.post("/reset-password")
async def reset_password(email: str):
    """Reset de senha via Supabase Auth."""
    try:
        supabase = get_supabase()
        supabase.auth.reset_password_email(email)
        logger.info(f"✅ Reset de senha enviado: {email}")
        return {"message": "Email de reset enviado com sucesso"}
    except Exception as e:
        logger.error(f"❌ Erro no reset de senha: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar reset: {str(e)}")

@router.post("/update-password")
async def update_password(password: str):
    """Atualizar senha via Supabase Auth."""
    try:
        supabase = get_supabase()
        supabase.auth.update_user({"password": password})
        logger.info("✅ Senha atualizada")
        return {"message": "Senha atualizada com sucesso"}
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar senha: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar senha: {str(e)}")

# =============================================================================
# OAUTH ENDPOINTS (Delegados para Supabase)
# =============================================================================

@router.post("/oauth/{provider}")
async def oauth_login(provider: str, request: Request):
    """Login OAuth via Supabase Auth."""
    try:
        supabase = get_supabase()
        
        # Obter URL de autorização do provider
        auth_url = supabase.auth.sign_in_with_oauth({
            "provider": provider,
            "options": {
                "redirect_to": str(request.url_for("oauth_callback"))
            }
        })
        
        return {"auth_url": auth_url.url}
    except Exception as e:
        logger.error(f"❌ Erro no OAuth {provider}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no OAuth: {str(e)}")

@router.get("/oauth/callback")
async def oauth_callback(code: str, state: str):
    """Callback OAuth via Supabase Auth."""
    try:
        supabase = get_supabase()
        response = supabase.auth.exchange_code_for_session(code)
        
        if response.user:
            logger.info(f"✅ OAuth login realizado: {response.user.email}")
            return {"message": "Login OAuth realizado com sucesso"}
        else:
            raise HTTPException(status_code=400, detail="Erro no callback OAuth")
    except Exception as e:
        logger.error(f"❌ Erro no callback OAuth: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no callback: {str(e)}")

# =============================================================================
# DEPENDENCY INJECTION
# =============================================================================

def require_auth():
    """Dependency para verificar autenticação."""
    def auth_dependency():
        if not is_authenticated():
            raise HTTPException(status_code=401, detail="Autenticação necessária")
        return get_current_user()
    return auth_dependency 