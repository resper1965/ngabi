# Gerenciamento de Secrets - HashiCorp Vault e AWS Secrets Manager

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [HashiCorp Vault](#hashicorp-vault)
3. [AWS Secrets Manager](#aws-secrets-manager)
4. [Implementação no Backend](#implementação-no-backend)
5. [Configuração de Ambiente](#configuração-de-ambiente)
6. [Exemplos de Uso](#exemplos-de-uso)
7. [Monitoramento e Logs](#monitoramento-e-logs)
8. [Segurança](#segurança)

## 🎯 Visão Geral

Este documento descreve como gerenciar secrets sensíveis (`OPENAI_API_KEY`, `PINECONE_API_KEY`, `JWT_SECRET`) usando HashiCorp Vault ou AWS Secrets Manager, e como o backend FastAPI consome esses secrets de forma segura.

### Secrets Gerenciados

| Secret | Descrição | Uso |
|--------|-----------|-----|
| `OPENAI_API_KEY` | Chave da API OpenAI | Integração com GPT-4, embeddings |
| `PINECONE_API_KEY` | Chave da API Pinecone | Busca vetorial e similaridade |
| `JWT_SECRET` | Chave secreta para JWT | Autenticação e autorização |

## 🔐 HashiCorp Vault

### Instalação e Configuração

#### 1. Instalar Vault

```bash
# Ubuntu/Debian
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault

# macOS
brew install vault

# Docker
docker run -d --name vault -p 8200:8200 vault:latest
```

#### 2. Inicializar Vault

```bash
# Inicializar Vault
vault operator init

# Exemplo de saída:
# Unseal Key 1: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Unseal Key 2: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Unseal Key 3: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Unseal Key 4: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Unseal Key 5: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Initial Root Token: hvs.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Desbloquear Vault (usar 3 chaves)
vault operator unseal xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
vault operator unseal xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
vault operator unseal xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3. Configurar Secrets Engine

```bash
# Habilitar KV secrets engine
vault secrets enable -path=chat-app kv-v2

# Configurar política de acesso
cat > chat-app-policy.hcl << EOF
path "chat-app/data/*" {
  capabilities = ["read"]
}

path "chat-app/metadata/*" {
  capabilities = ["read"]
}
EOF

vault policy write chat-app-policy chat-app-policy.hcl
```

#### 4. Criar Token de Acesso

```bash
# Criar token para aplicação
vault token create -policy=chat-app-policy

# Exemplo de saída:
# Key                  Value
# ---                  -----
# token               hvs.CAESIIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# token_accessor      xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# token_duration      768h
# token_renewable     true
# token_policies      ["chat-app-policy" "default"]
```

#### 5. Armazenar Secrets

```bash
# Configurar token de acesso
export VAULT_TOKEN=hvs.CAESIIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export VAULT_ADDR=http://localhost:8200

# Armazenar secrets
vault kv put chat-app/secrets \
  openai_api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  pinecone_api_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  jwt_secret="super-secret-jwt-key-for-chat-app-2024"

# Verificar secrets
vault kv get chat-app/secrets
```

### Configuração com Docker Compose

```yaml
# docker-compose.vault.yml
version: '3.8'

services:
  vault:
    image: vault:latest
    container_name: vault
    ports:
      - "8200:8200"
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=hvs.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    volumes:
      - vault_data:/vault/file
    command: vault server -dev -dev-root-token-id=hvs.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

volumes:
  vault_data:
```

## ☁️ AWS Secrets Manager

### Configuração

#### 1. Configurar AWS CLI

```bash
# Instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configurar credenciais
aws configure
# AWS Access Key ID: AKIAXXXXXXXXXXXXXXXX
# AWS Secret Access Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Default region name: us-east-1
# Default output format: json
```

#### 2. Criar Secrets

```bash
# Criar secret para OpenAI
aws secretsmanager create-secret \
  --name "chat-app/openai-api-key" \
  --description "OpenAI API Key for Chat Application" \
  --secret-string '{"api_key":"sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}'

# Criar secret para Pinecone
aws secretsmanager create-secret \
  --name "chat-app/pinecone-api-key" \
  --description "Pinecone API Key for Chat Application" \
  --secret-string '{"api_key":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}'

# Criar secret para JWT
aws secretsmanager create-secret \
  --name "chat-app/jwt-secret" \
  --description "JWT Secret for Chat Application" \
  --secret-string '{"secret":"super-secret-jwt-key-for-chat-app-2024"}'
```

#### 3. Configurar IAM Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-east-1:123456789012:secret:chat-app/*"
      ]
    }
  ]
}
```

### Configuração com Terraform

```hcl
# secrets.tf
resource "aws_secretsmanager_secret" "openai_api_key" {
  name        = "chat-app/openai-api-key"
  description = "OpenAI API Key for Chat Application"
  
  tags = {
    Environment = "production"
    Application = "chat-app"
  }
}

resource "aws_secretsmanager_secret_version" "openai_api_key" {
  secret_id     = aws_secretsmanager_secret.openai_api_key.id
  secret_string = jsonencode({
    api_key = var.openai_api_key
  })
}

resource "aws_secretsmanager_secret" "pinecone_api_key" {
  name        = "chat-app/pinecone-api-key"
  description = "Pinecone API Key for Chat Application"
  
  tags = {
    Environment = "production"
    Application = "chat-app"
  }
}

resource "aws_secretsmanager_secret_version" "pinecone_api_key" {
  secret_id     = aws_secretsmanager_secret.pinecone_api_key.id
  secret_string = jsonencode({
    api_key = var.pinecone_api_key
  })
}

resource "aws_secretsmanager_secret" "jwt_secret" {
  name        = "chat-app/jwt-secret"
  description = "JWT Secret for Chat Application"
  
  tags = {
    Environment = "production"
    Application = "chat-app"
  }
}

resource "aws_secretsmanager_secret_version" "jwt_secret" {
  secret_id     = aws_secretsmanager_secret.jwt_secret.id
  secret_string = jsonencode({
    secret = var.jwt_secret
  })
}
```

## 🔧 Implementação no Backend

### 1. Instalar Dependências

```bash
# Adicionar ao requirements.txt
hvac==1.2.0
boto3==1.34.0
```

### 2. Criar Módulo de Secrets

```python
# app/core/secrets.py
import os
import json
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

import hvac
import boto3
from botocore.exceptions import ClientError

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
```

### 3. Integração com Configurações

```python
# app/core/config.py
import os
from typing import Optional
from pydantic import BaseSettings

from app.core.secrets import secrets_service

class Settings(BaseSettings):
    """Configurações da aplicação com suporte a secrets."""
    
    # Configurações básicas
    app_name: str = "Chat Multi-Agente API"
    debug: bool = False
    environment: str = "development"
    
    # Secrets (serão carregados dinamicamente)
    openai_api_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    
    # Configurações de secrets
    secrets_provider: str = "vault"  # vault ou aws
    vault_url: str = "http://localhost:8200"
    vault_token: Optional[str] = None
    aws_region: str = "us-east-1"
    
    class Config:
        env_file = ".env"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_secrets()
    
    def _load_secrets(self):
        """Carrega secrets do provedor configurado."""
        try:
            # Carregar secrets do provedor
            secrets = secrets_service.get_all_secrets()
            
            # Atualizar configurações
            if secrets.get('OPENAI_API_KEY'):
                self.openai_api_key = secrets['OPENAI_API_KEY']
            
            if secrets.get('PINECONE_API_KEY'):
                self.pinecone_api_key = secrets['PINECONE_API_KEY']
            
            if secrets.get('JWT_SECRET'):
                self.jwt_secret = secrets['JWT_SECRET']
            
            # Fallback para variáveis de ambiente
            if not self.openai_api_key:
                self.openai_api_key = os.getenv('OPENAI_API_KEY')
            
            if not self.pinecone_api_key:
                self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
            
            if not self.jwt_secret:
                self.jwt_secret = os.getenv('JWT_SECRET')
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar secrets: {e}")
            # Usar apenas variáveis de ambiente como fallback
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
            self.jwt_secret = os.getenv('JWT_SECRET')
    
    def validate_secrets(self) -> bool:
        """Valida se todos os secrets necessários estão disponíveis."""
        required_secrets = [
            ('openai_api_key', 'OPENAI_API_KEY'),
            ('pinecone_api_key', 'PINECONE_API_KEY'),
            ('jwt_secret', 'JWT_SECRET')
        ]
        
        missing_secrets = []
        
        for attr_name, secret_name in required_secrets:
            if not getattr(self, attr_name):
                missing_secrets.append(secret_name)
        
        if missing_secrets:
            print(f"❌ Secrets faltando: {', '.join(missing_secrets)}")
            return False
        
        print("✅ Todos os secrets estão configurados")
        return True

# Instância global das configurações
settings = Settings()
```

### 4. Uso nos Serviços

```python
# app/services/openai_service.py
from app.core.config import settings
import openai

class OpenAIService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        openai.api_key = settings.openai_api_key
    
    async def generate_response(self, prompt: str) -> str:
        """Gera resposta usando OpenAI."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao gerar resposta OpenAI: {e}")
            raise

# app/services/pinecone_service.py
from app.core.config import settings
import pinecone

class PineconeService:
    def __init__(self):
        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY não configurada")
        
        pinecone.init(api_key=settings.pinecone_api_key, environment="us-east-1-aws")
    
    def search_similar(self, vector, top_k=5):
        """Busca vetores similares no Pinecone."""
        try:
            index = pinecone.Index("chat-embeddings")
            results = index.query(vector=vector, top_k=top_k)
            return results
        except Exception as e:
            print(f"Erro na busca Pinecone: {e}")
            raise

# app/core/auth.py
from app.core.config import settings
import jwt
from datetime import datetime, timedelta

class JWTAuth:
    def __init__(self):
        if not settings.jwt_secret:
            raise ValueError("JWT_SECRET não configurado")
        
        self.secret = settings.jwt_secret
    
    def create_token(self, user_id: str, tenant_id: str) -> str:
        """Cria token JWT."""
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> dict:
        """Verifica token JWT."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")
```

## ⚙️ Configuração de Ambiente

### 1. Variáveis de Ambiente

```bash
# .env
# Provedor de secrets (vault ou aws)
SECRETS_PROVIDER=vault

# HashiCorp Vault
VAULT_URL=http://localhost:8200
VAULT_TOKEN=hvs.CAESIIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# AWS Secrets Manager
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Fallback (apenas para desenvolvimento)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
JWT_SECRET=super-secret-jwt-key-for-chat-app-2024
```

### 2. Docker Compose Completo

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRETS_PROVIDER=vault
      - VAULT_URL=http://vault:8200
      - VAULT_TOKEN=${VAULT_TOKEN}
    depends_on:
      - vault
      - redis
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  vault:
    image: vault:latest
    container_name: vault
    ports:
      - "8200:8200"
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=${VAULT_TOKEN}
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    volumes:
      - vault_data:/vault/file
    command: vault server -dev -dev-root-token-id=${VAULT_TOKEN}

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  vault_data:
  redis_data:
```

### 3. Script de Inicialização

```bash
#!/bin/bash
# scripts/init-secrets.sh

set -e

echo "🔐 Inicializando secrets..."

# Verificar se Vault está rodando
if [ "$SECRETS_PROVIDER" = "vault" ]; then
    echo "📦 Configurando HashiCorp Vault..."
    
    # Aguardar Vault estar pronto
    until curl -s http://localhost:8200/v1/sys/health > /dev/null; do
        echo "⏳ Aguardando Vault..."
        sleep 2
    done
    
    # Configurar secrets no Vault
    vault kv put chat-app/secrets \
        openai_api_key="$OPENAI_API_KEY" \
        pinecone_api_key="$PINECONE_API_KEY" \
        jwt_secret="$JWT_SECRET"
    
    echo "✅ Secrets configurados no Vault"
fi

# Verificar se AWS Secrets Manager está configurado
if [ "$SECRETS_PROVIDER" = "aws" ]; then
    echo "☁️ Configurando AWS Secrets Manager..."
    
    # Criar secrets no AWS
    aws secretsmanager create-secret \
        --name "chat-app/openai-api-key" \
        --description "OpenAI API Key" \
        --secret-string "{\"api_key\":\"$OPENAI_API_KEY\"}" \
        --region "$AWS_REGION" || true
    
    aws secretsmanager create-secret \
        --name "chat-app/pinecone-api-key" \
        --description "Pinecone API Key" \
        --secret-string "{\"api_key\":\"$PINECONE_API_KEY\"}" \
        --region "$AWS_REGION" || true
    
    aws secretsmanager create-secret \
        --name "chat-app/jwt-secret" \
        --description "JWT Secret" \
        --secret-string "{\"secret\":\"$JWT_SECRET\"}" \
        --region "$AWS_REGION" || true
    
    echo "✅ Secrets configurados no AWS Secrets Manager"
fi

echo "🎉 Inicialização de secrets concluída!"
```

## 📝 Exemplos de Uso

### 1. Uso Direto do Serviço

```python
from app.core.secrets import secrets_service

# Recuperar secrets individuais
openai_key = secrets_service.get_openai_api_key()
pinecone_key = secrets_service.get_pinecone_api_key()
jwt_secret = secrets_service.get_jwt_secret()

# Recuperar todos os secrets
all_secrets = secrets_service.get_all_secrets()
print(f"Secrets disponíveis: {list(all_secrets.keys())}")
```

### 2. Uso nas Configurações

```python
from app.core.config import settings

# Verificar se secrets estão configurados
if settings.validate_secrets():
    print("✅ Aplicação pronta para usar")
else:
    print("❌ Falta configurar secrets")

# Usar secrets nos serviços
openai_service = OpenAIService()  # Usa settings.openai_api_key
pinecone_service = PineconeService()  # Usa settings.pinecone_api_key
jwt_auth = JWTAuth()  # Usa settings.jwt_secret
```

### 3. Endpoint de Health Check

```python
@app.get("/health/secrets")
async def check_secrets_health():
    """Verifica saúde dos secrets."""
    try:
        secrets = secrets_service.get_all_secrets()
        
        health_status = {
            "status": "healthy",
            "secrets_provider": settings.secrets_provider,
            "secrets_available": list(secrets.keys()),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Verificar se todos os secrets estão disponíveis
        required_secrets = ['OPENAI_API_KEY', 'PINECONE_API_KEY', 'JWT_SECRET']
        missing_secrets = [s for s in required_secrets if s not in secrets]
        
        if missing_secrets:
            health_status["status"] = "unhealthy"
            health_status["missing_secrets"] = missing_secrets
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

## 📊 Monitoramento e Logs

### 1. Logs Estruturados

```python
import logging
import json
from datetime import datetime

class SecretsLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_secret_access(self, secret_name: str, success: bool, error: str = None):
        """Log de acesso a secrets."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "secret_access",
            "secret_name": secret_name,
            "success": success,
            "provider": settings.secrets_provider
        }
        
        if error:
            log_data["error"] = error
        
        self.logger.info(json.dumps(log_data))
    
    def log_secret_rotation(self, secret_name: str):
        """Log de rotação de secrets."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "secret_rotation",
            "secret_name": secret_name,
            "provider": settings.secrets_provider
        }
        
        self.logger.info(json.dumps(log_data))

secrets_logger = SecretsLogger()
```

### 2. Métricas de Secrets

```python
from prometheus_client import Counter, Histogram
import time

# Métricas Prometheus
SECRET_ACCESS_TOTAL = Counter(
    'secret_access_total',
    'Total de acessos a secrets',
    ['secret_name', 'provider', 'status']
)

SECRET_ACCESS_DURATION = Histogram(
    'secret_access_duration_seconds',
    'Duração do acesso a secrets',
    ['secret_name', 'provider']
)

class MetricsSecretsManager:
    """Wrapper para métricas de secrets."""
    
    def __init__(self, secrets_manager: SecretsManager):
        self.secrets_manager = secrets_manager
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        start_time = time.time()
        
        try:
            secret = self.secrets_manager.get_secret(secret_name)
            
            # Registrar métricas
            SECRET_ACCESS_TOTAL.labels(
                secret_name=secret_name,
                provider=settings.secrets_provider,
                status="success" if secret else "not_found"
            ).inc()
            
            SECRET_ACCESS_DURATION.labels(
                secret_name=secret_name,
                provider=settings.secrets_provider
            ).observe(time.time() - start_time)
            
            return secret
            
        except Exception as e:
            # Registrar erro
            SECRET_ACCESS_TOTAL.labels(
                secret_name=secret_name,
                provider=settings.secrets_provider,
                status="error"
            ).inc()
            
            raise
```

## 🔒 Segurança

### 1. Boas Práticas

- **Rotação de Secrets**: Implementar rotação automática
- **Princípio do Menor Privilégio**: Usar políticas restritivas
- **Auditoria**: Logs de todos os acessos a secrets
- **Criptografia**: Secrets sempre criptografados em trânsito e repouso
- **Isolamento**: Secrets separados por ambiente (dev, staging, prod)

### 2. Políticas de Segurança

```hcl
# vault-policy.hcl
# Política restritiva para produção
path "chat-app/data/*" {
  capabilities = ["read"]
  allowed_parameters = {
    "version" = []
  }
}

path "chat-app/metadata/*" {
  capabilities = ["read"]
}

# Negar acesso a outros paths
path "*" {
  capabilities = ["deny"]
}
```

### 3. Rotação Automática

```python
import schedule
import time
from datetime import datetime

def rotate_secrets():
    """Rotaciona secrets automaticamente."""
    try:
        # Implementar lógica de rotação
        secrets_service.refresh_cache()
        secrets_logger.log_secret_rotation("all")
        print(f"🔄 Secrets rotacionados em {datetime.utcnow()}")
    except Exception as e:
        print(f"❌ Erro na rotação de secrets: {e}")

# Agendar rotação diária
schedule.every().day.at("02:00").do(rotate_secrets)

# Executar scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 4. Validação de Secrets

```python
def validate_secret_format(secret_name: str, secret_value: str) -> bool:
    """Valida formato dos secrets."""
    validators = {
        'OPENAI_API_KEY': lambda x: x.startswith('sk-') and len(x) > 20,
        'PINECONE_API_KEY': lambda x: len(x) == 36 and '-' in x,
        'JWT_SECRET': lambda x: len(x) >= 32
    }
    
    validator = validators.get(secret_name)
    if validator:
        return validator(secret_value)
    
    return True
```

## 🚀 Deploy em Produção

### 1. Kubernetes

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: vault-token
type: Opaque
data:
  token: <base64-encoded-vault-token>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chat-app
  template:
    metadata:
      labels:
        app: chat-app
    spec:
      containers:
      - name: chat-app
        image: chat-app:latest
        env:
        - name: SECRETS_PROVIDER
          value: "vault"
        - name: VAULT_URL
          value: "http://vault:8200"
        - name: VAULT_TOKEN
          valueFrom:
            secretKeyRef:
              name: vault-token
              key: token
        ports:
        - containerPort: 8000
```

### 2. AWS ECS

```json
{
  "family": "chat-app",
  "taskRoleArn": "arn:aws:iam::123456789012:role/chat-app-task-role",
  "executionRoleArn": "arn:aws:iam::123456789012:role/chat-app-execution-role",
  "containerDefinitions": [
    {
      "name": "chat-app",
      "image": "chat-app:latest",
      "environment": [
        {
          "name": "SECRETS_PROVIDER",
          "value": "aws"
        },
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
        }
      ],
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

Esta documentação fornece uma implementação completa e segura para gerenciamento de secrets usando HashiCorp Vault ou AWS Secrets Manager no backend FastAPI! 🎉 