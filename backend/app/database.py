import os
from supabase import create_client, Client

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Cliente Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para obter cliente Supabase
def get_supabase() -> Client:
    if not supabase:
        raise Exception("Supabase não configurado. Configure SUPABASE_URL e SUPABASE_ANON_KEY")
    return supabase

# Função para obter usuário autenticado
def get_current_user():
    """Obter usuário atual autenticado"""
    try:
        user = supabase.auth.get_user()
        return user.user if user else None
    except:
        return None

# Função para verificar se usuário está autenticado
def is_authenticated():
    """Verificar se usuário está autenticado"""
    return get_current_user() is not None 