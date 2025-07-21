from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from supabase import create_client, Client

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Cliente Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuração do banco de dados (PostgreSQL do Supabase)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/chat_agents")

# Criar engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL debugging
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Middleware para isolamento por tenant
class TenantSession:
    def __init__(self, db: Session, tenant_id: str = None):
        self.db = db
        self.tenant_id = tenant_id
    
    def __enter__(self):
        if self.tenant_id:
            # Configurar filtro de tenant para todas as queries
            self.db.execute("SET app.current_tenant_id = :tenant_id", {"tenant_id": self.tenant_id})
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tenant_id:
            # Limpar configuração do tenant
            self.db.execute("RESET app.current_tenant_id")
        self.db.close()

# Dependency para injeção de sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency para sessão com tenant
def get_tenant_db(tenant_id: str):
    db = SessionLocal()
    try:
        with TenantSession(db, tenant_id) as tenant_db:
            yield tenant_db
    finally:
        db.close()

# Função para obter cliente Supabase
def get_supabase() -> Client:
    if not supabase:
        raise Exception("Supabase não configurado. Configure SUPABASE_URL e SUPABASE_ANON_KEY")
    return supabase 