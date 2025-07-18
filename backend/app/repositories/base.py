from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import Base
import uuid

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Repositório base com isolamento por tenant.
    Garante que todas as queries incluam o tenant_id para isolamento lógico.
    """
    
    def __init__(self, model: Type[ModelType], db: Session, tenant_id: Optional[str] = None):
        self.model = model
        self.db = db
        self.tenant_id = tenant_id
    
    def _add_tenant_filter(self, query):
        """Adicionar filtro de tenant se especificado"""
        if self.tenant_id and hasattr(self.model, 'tenant_id'):
            return query.filter(self.model.tenant_id == self.tenant_id)
        return query
    
    def get(self, id: str) -> Optional[ModelType]:
        """Buscar por ID com filtro de tenant"""
        query = self.db.query(self.model).filter(self.model.id == id)
        query = self._add_tenant_filter(query)
        return query.first()
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Buscar múltiplos registros com filtro de tenant"""
        query = self.db.query(self.model)
        query = self._add_tenant_filter(query)
        return query.offset(skip).limit(limit).all()
    
    def create(self, obj_in: dict) -> ModelType:
        """Criar novo registro com tenant_id"""
        if self.tenant_id and hasattr(self.model, 'tenant_id'):
            obj_in['tenant_id'] = self.tenant_id
        
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Atualizar registro"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: str) -> bool:
        """Deletar registro por ID com filtro de tenant"""
        query = self.db.query(self.model).filter(self.model.id == id)
        query = self._add_tenant_filter(query)
        db_obj = query.first()
        
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """Contar registros com filtro de tenant"""
        query = self.db.query(self.model)
        query = self._add_tenant_filter(query)
        return query.count()
    
    def exists(self, id: str) -> bool:
        """Verificar se registro existe com filtro de tenant"""
        query = self.db.query(self.model).filter(self.model.id == id)
        query = self._add_tenant_filter(query)
        return query.first() is not None
    
    def filter_by(self, **kwargs) -> List[ModelType]:
        """Filtrar por campos específicos com isolamento de tenant"""
        query = self.db.query(self.model).filter_by(**kwargs)
        query = self._add_tenant_filter(query)
        return query.all()
    
    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Buscar por campo específico com filtro de tenant"""
        if not hasattr(self.model, field):
            raise ValueError(f"Campo '{field}' não existe no modelo {self.model.__name__}")
        
        query = self.db.query(self.model).filter(getattr(self.model, field) == value)
        query = self._add_tenant_filter(query)
        return query.first() 