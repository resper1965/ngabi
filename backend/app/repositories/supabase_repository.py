from typing import Optional, List, Any, Dict
from app.database import get_supabase

class SupabaseRepository:
    """
    Repositório base usando Supabase.
    Substitui o SQLAlchemy por operações diretas no Supabase.
    """
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.supabase = get_supabase()
    
    def get(self, id: str) -> Optional[Dict]:
        """Buscar por ID"""
        try:
            response = self.supabase.table(self.table_name).select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar {self.table_name}: {e}")
            return None
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Buscar múltiplos registros"""
        try:
            response = self.supabase.table(self.table_name).select('*').range(skip, skip + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Erro ao buscar múltiplos {self.table_name}: {e}")
            return []
    
    def create(self, data: Dict) -> Optional[Dict]:
        """Criar novo registro"""
        try:
            response = self.supabase.table(self.table_name).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao criar {self.table_name}: {e}")
            return None
    
    def update(self, id: str, data: Dict) -> Optional[Dict]:
        """Atualizar registro"""
        try:
            response = self.supabase.table(self.table_name).update(data).eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao atualizar {self.table_name}: {e}")
            return None
    
    def delete(self, id: str) -> bool:
        """Deletar registro"""
        try:
            response = self.supabase.table(self.table_name).delete().eq('id', id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Erro ao deletar {self.table_name}: {e}")
            return False
    
    def filter_by(self, **kwargs) -> List[Dict]:
        """Filtrar por campos específicos"""
        try:
            query = self.supabase.table(self.table_name).select('*')
            for field, value in kwargs.items():
                query = query.eq(field, value)
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Erro ao filtrar {self.table_name}: {e}")
            return []
    
    def get_by_field(self, field: str, value: Any) -> Optional[Dict]:
        """Buscar por campo específico"""
        try:
            response = self.supabase.table(self.table_name).select('*').eq(field, value).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar por campo {self.table_name}: {e}")
            return None
    
    def count(self) -> int:
        """Contar registros"""
        try:
            response = self.supabase.table(self.table_name).select('*', count='exact').execute()
            return response.count or 0
        except Exception as e:
            print(f"Erro ao contar {self.table_name}: {e}")
            return 0

class TenantSupabaseRepository(SupabaseRepository):
    """
    Repositório específico para tenants com isolamento.
    """
    
    def __init__(self, tenant_id: Optional[str] = None):
        super().__init__('tenants')
        self.tenant_id = tenant_id
    
    def get_tenant_data(self, table_name: str, **filters) -> List[Dict]:
        """Buscar dados de uma tabela com filtro de tenant"""
        try:
            query = self.supabase.table(table_name).select('*')
            
            # Adicionar filtro de tenant se especificado
            if self.tenant_id:
                query = query.eq('tenant_id', self.tenant_id)
            
            # Adicionar filtros adicionais
            for field, value in filters.items():
                query = query.eq(field, value)
            
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Erro ao buscar dados de tenant {table_name}: {e}")
            return [] 