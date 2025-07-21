"""
Sistema de gerenciamento de secrets para HashiCorp Vault e AWS Secrets Manager.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

try:
    import hvac
    HVAC_AVAILABLE = True
except ImportError:
    HVAC_AVAILABLE = False
    logging.warning("hvac não instalado. HashiCorp Vault não estará disponível.")

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    logging.warning("boto3 não instalado. AWS Secrets Manager não estará disponível.")

logger = logging.getLogger(__name__)

class SecretsManager(ABC):
    """Classe abstrata para gerenciamento de secrets."""
    
    @abstractmethod
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Recupera um secret."""
        pass
    
    @abstractmethod
    def get_secrets(self, secret_names: list) -> Dict[str, str]:
        """Recupera múltiplos secrets."""
        pass

class VaultSecretsManager(SecretsManager):
    """Implementação para HashiCorp Vault."""
    
    def __init__(self, vault_url: str, token: str, mount_point: str = "chat-app"):
        if not HVAC_AVAILABLE:
            raise ImportError("hvac não está instalado. Execute: pip install hvac")
        
        self.client = hvac.Client(url=vault_url, token=token)
        self.mount_point = mount_point
        self._validate_connection()
    
    def _validate_connection(self):
        """Valida conexão com Vault."""
        try:
            if not self.client.is_authenticated():
                raise Exception("Falha na autenticação com Vault")
            logger.info("✅ Conectado ao HashiCorp Vault")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao Vault: {e}")
            raise
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Recupera um secret do Vault."""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=secret_name,
                mount_point=self.mount_point
            )
            
            if response and 'data' in response and 'data' in response['data']:
                secret_data = response['data']['data']
                logger.info(f"🎯 Secret recuperado do Vault: {secret_name}")
                return secret_data.get(secret_name.split('/')[-1])
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao recuperar secret {secret_name} do Vault: {e}")
            return None
    
    def get_secrets(self, secret_names: list) -> Dict[str, str]:
        """Recupera múltiplos secrets do Vault."""
        secrets = {}
        
        try:
            # Recuperar todos os secrets de uma vez
            response = self.client.secrets.kv.v2.read_secret_version(
                path="secrets",
                mount_point=self.mount_point
            )
            
            if response and 'data' in response and 'data' in response['data']:
                secret_data = response['data']['data']
                
                for secret_name in secret_names:
                    secret_value = secret_data.get(secret_name)
                    if secret_value:
                        secrets[secret_name] = secret_value
                        logger.info(f"🎯 Secret recuperado: {secret_name}")
                    else:
                        logger.warning(f"⚠️ Secret não encontrado: {secret_name}")
            
        except Exception as e:
            logger.error(f"Erro ao recuperar secrets do Vault: {e}")
        
        return secrets

class AWSSecretsManager(SecretsManager):
    """Implementação para AWS Secrets Manager."""
    
    def __init__(self, region_name: str = "us-east-1"):
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 não está instalado. Execute: pip install boto3")
        
        self.client = boto3.client('secretsmanager', region_name=region_name)
        self._validate_connection()
    
    def _validate_connection(self):
        """Valida conexão com AWS Secrets Manager."""
        try:
            self.client.list_secrets(MaxResults=1)
            logger.info("✅ Conectado ao AWS Secrets Manager")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao AWS Secrets Manager: {e}")
            raise
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Recupera um secret do AWS Secrets Manager."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            
            if 'SecretString' in response:
                secret_data = json.loads(response['SecretString'])
                logger.info(f"🎯 Secret recuperado do AWS: {secret_name}")
                return secret_data.get('api_key') or secret_data.get('secret')
            
            return None
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                logger.warning(f"⚠️ Secret não encontrado: {secret_name}")
            else:
                logger.error(f"Erro ao recuperar secret {secret_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao recuperar secret {secret_name}: {e}")
            return None
    
    def get_secrets(self, secret_names: list) -> Dict[str, str]:
        """Recupera múltiplos secrets do AWS Secrets Manager."""
        secrets = {}
        
        for secret_name in secret_names:
            secret_value = self.get_secret(secret_name)
            if secret_value:
                secrets[secret_name] = secret_value
        
        return secrets

class SecretsService:
    """Serviço principal para gerenciamento de secrets."""
    
    def __init__(self):
        self.secrets_manager = self._initialize_secrets_manager()
        self._cache = {}
    
    def _initialize_secrets_manager(self) -> SecretsManager:
        """Inicializa o gerenciador de secrets apropriado."""
        secrets_provider = os.getenv('SECRETS_PROVIDER', 'vault').lower()
        
        if secrets_provider == 'vault':
            vault_url = os.getenv('VAULT_URL', 'http://localhost:8200')
            vault_token = os.getenv('VAULT_TOKEN')
            
            if not vault_token:
                raise ValueError("VAULT_TOKEN é obrigatório para usar HashiCorp Vault")
            
            return VaultSecretsManager(vault_url, vault_token)
        
        elif secrets_provider == 'aws':
            region_name = os.getenv('AWS_REGION', 'us-east-1')
            return AWSSecretsManager(region_name)
        
        else:
            raise ValueError(f"Provedor de secrets não suportado: {secrets_provider}")
    
    def get_openai_api_key(self) -> Optional[str]:
        """Recupera a chave da API OpenAI."""
        cache_key = 'openai_api_key'
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        if isinstance(self.secrets_manager, VaultSecretsManager):
            secret = self.secrets_manager.get_secret('secrets')
            if secret:
                self._cache[cache_key] = secret
                return secret
        else:
            secret = self.secrets_manager.get_secret('chat-app/openai-api-key')
            if secret:
                self._cache[cache_key] = secret
                return secret
        
        return None
    
    def get_pinecone_api_key(self) -> Optional[str]:
        """Recupera a chave da API Pinecone."""
        cache_key = 'pinecone_api_key'
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        if isinstance(self.secrets_manager, VaultSecretsManager):
            secret = self.secrets_manager.get_secret('secrets')
            if secret:
                self._cache[cache_key] = secret
                return secret
        else:
            secret = self.secrets_manager.get_secret('chat-app/pinecone-api-key')
            if secret:
                self._cache[cache_key] = secret
                return secret
        
        return None
    
    def get_jwt_secret(self) -> Optional[str]:
        """Recupera o secret JWT."""
        cache_key = 'jwt_secret'
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        if isinstance(self.secrets_manager, VaultSecretsManager):
            secret = self.secrets_manager.get_secret('secrets')
            if secret:
                self._cache[cache_key] = secret
                return secret
        else:
            secret = self.secrets_manager.get_secret('chat-app/jwt-secret')
            if secret:
                self._cache[cache_key] = secret
                return secret
        
        return None
    
    def refresh_cache(self):
        """Atualiza o cache de secrets."""
        self._cache.clear()
        logger.info("🔄 Cache de secrets atualizado")
    
    def get_all_secrets(self) -> Dict[str, str]:
        """Recupera todos os secrets."""
        secrets = {}
        
        openai_key = self.get_openai_api_key()
        if openai_key:
            secrets['OPENAI_API_KEY'] = openai_key
        
        pinecone_key = self.get_pinecone_api_key()
        if pinecone_key:
            secrets['PINECONE_API_KEY'] = pinecone_key
        
        jwt_secret = self.get_jwt_secret()
        if jwt_secret:
            secrets['JWT_SECRET'] = jwt_secret
        
        return secrets

# Instância global do serviço de secrets
secrets_service = SecretsService()

# Funções utilitárias para uso direto
def get_cached_response(tenant_id: str, agent_id: str, query: str) -> Optional[Dict[str, Any]]:
    """Função utilitária para buscar resposta cacheada."""
    return secrets_service.get_cached_response(tenant_id, agent_id, query)

def set_cached_response(
    tenant_id: str,
    agent_id: str,
    query: str,
    response: Dict[str, Any],
    ttl: Optional[int] = None
) -> bool:
    """Função utilitária para salvar resposta no cache."""
    return secrets_service.set_cached_response(tenant_id, agent_id, query, response, ttl)

def clear_tenant_cache(tenant_id: str) -> int:
    """Função utilitária para limpar cache de um tenant."""
    return secrets_service.clear_tenant_cache(tenant_id)

def get_cache_stats(tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Função utilitária para obter estatísticas do cache."""
    return secrets_service.get_cache_stats(tenant_id)

def cache_health_check() -> Dict[str, Any]:
    """Função utilitária para verificar saúde do cache."""
    return secrets_service.cache_health_check() 