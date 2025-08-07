# 🔧 Variáveis de Ambiente do Backend - n.Gabi

## 🔐 **Variáveis Obrigatórias:**

### **OpenAI (Chat AI):**
```bash
# OpenAI API Key (obrigatório para chat)
OPENAI_API_KEY=your-openai-api-key
```

### **Supabase (Infraestrutura Principal):**
```bash
# URL do Supabase (obrigatório)
SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co

# Chave anônima do Supabase (obrigatório)
SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd

# Chave de serviço do Supabase (opcional)
SUPABASE_SERVICE_ROLE_KEY=sb_service_role_key_here
```

### **JWT (Autenticação):**
```bash
# JWT é gerenciado automaticamente pelo Supabase Auth
# Não é necessário configurar JWT_SECRET
```

## ⚙️ **Variáveis Opcionais:**

### **Configurações da Aplicação:**
```bash
# Nome da aplicação
APP_NAME="n.Gabi"

# Versão da aplicação
APP_VERSION="2.0.0"

# Modo debug
DEBUG=false

# Ambiente
ENVIRONMENT=production
```

### **Cache Redis:**
```bash
# URL do Redis
REDIS_URL=redis://localhost:6379/0

# Habilitar cache
CACHE_ENABLED=true

# TTL do cache (em segundos)
CACHE_TTL=3600
```

### **Rate Limiting:**
```bash
# Habilitar rate limiting
RATE_LIMIT_ENABLED=true

# Rate limit padrão (req/min)
RATE_LIMIT_DEFAULT=100

# Rate limit para chat (req/min)
RATE_LIMIT_CHAT=20

# Rate limit específico para chat
CHAT_RATE_LIMIT=10/minute
```

### **CORS:**
```bash
# Origens permitidas (CORS)
CORS_ORIGINS=http://localhost:3000,https://ngabi.ness.tec.br
```

### **Configurações de IA:**
```bash
# Modelo padrão do chat
DEFAULT_CHAT_MODEL=gpt-3.5-turbo

# Máximo de tokens
MAX_TOKENS=2048

# Temperatura do modelo
TEMPERATURE=0.7
```

### **Sistema de Eventos:**
```bash
# Habilitar eventos
EVENTS_ENABLED=true

# Habilitar webhooks
WEBHOOKS_ENABLED=true
```

### **Logging:**
```bash
# Nível de log
LOG_LEVEL=INFO

# Formato de log
LOG_FORMAT=json
```

## 🔐 **Variáveis de Secrets (Opcional):**

### **Hashicorp Vault:**
```bash
# Provedor de secrets
SECRETS_PROVIDER=vault

# URL do Vault
VAULT_URL=http://localhost:8200

# Token do Vault
VAULT_TOKEN=hvs.CAESIIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### **AWS Secrets Manager:**
```bash
# Região AWS
AWS_REGION=us-east-1

# Credenciais AWS
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### **Pinecone (Vector DB):**
```bash
# Pinecone API Key
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## 📋 **Arquivo .env Completo:**

```bash
# =============================================================================
# CONFIGURAÇÕES OBRIGATÓRIAS
# =============================================================================

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key

# Supabase
SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd

# JWT é gerenciado pelo Supabase Auth (não necessário)
# JWT_SECRET=super-secret-jwt-key-for-chat-app-2024

# =============================================================================
# CONFIGURAÇÕES OPCIONAIS
# =============================================================================

# Aplicação
APP_NAME="n.Gabi"
APP_VERSION="2.0.0"
DEBUG=false
ENVIRONMENT=production

# Cache Redis
REDIS_URL=redis://localhost:6379/0
CACHE_ENABLED=true
CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT=100
RATE_LIMIT_CHAT=20
CHAT_RATE_LIMIT=10/minute

# CORS
CORS_ORIGINS=http://localhost:3000,https://ngabi.ness.tec.br

# IA
DEFAULT_CHAT_MODEL=gpt-3.5-turbo
MAX_TOKENS=2048
TEMPERATURE=0.7

# Eventos
EVENTS_ENABLED=true
WEBHOOKS_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 🐳 **Para Docker:**

### **Docker Compose:**
```yaml
environment:
  - OPENAI_API_KEY=your-openai-api-key
  - SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
  - SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd
  # JWT_SECRET - gerenciado pelo Supabase Auth
  - REDIS_URL=redis://redis:6379/0
  - DEBUG=false
  - ENVIRONMENT=production
```

### **Docker Run:**
```bash
docker run -e OPENAI_API_KEY=your-openai-api-key \
  -e SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co \
  -e SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd \
  # JWT é gerenciado pelo Supabase Auth \
  -e REDIS_URL=redis://redis:6379/0 \
  -e DEBUG=false \
  -e ENVIRONMENT=production \
  ngabi-backend
```

## 🎯 **Variáveis Mínimas para Funcionar:**

```bash
# Mínimo necessário
OPENAI_API_KEY=your-openai-api-key
SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd
# JWT_SECRET - gerenciado automaticamente pelo Supabase Auth
```

## ✅ **Status das Variáveis:**

**🔐 Obrigatórias (3):**
- ✅ **OPENAI_API_KEY**: Configurada
- ✅ **SUPABASE_URL**: Configurada  
- ✅ **SUPABASE_ANON_KEY**: Configurada

**⚙️ Opcionais (15+):**
- ✅ **Cache Redis**: Configurado
- ✅ **Rate Limiting**: Configurado
- ✅ **CORS**: Configurado
- ✅ **IA**: Configurado
- ✅ **Eventos**: Configurado

**Todas as variáveis necessárias estão prontas!** 🚀✨ 