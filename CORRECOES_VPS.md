# 🔧 Correções para VPS - n.Gabi

## 🚨 **Problemas Identificados**

### **1. Erro do Vault Token**
```
ValueError: VAULT_TOKEN é obrigatório para usar HashiCorp Vault
```

### **2. Erro do Redis**
```
❌ Erro ao conectar ao Redis: Error -2 connecting to redis-host:6379. Name does not resolve.
```

### **3. Erro do Secrets Provider**
```
ValueError: Provedor de secrets não suportado: env
```

## ✅ **Correções Aplicadas**

### **1. Sistema de Secrets (backend/app/core/secrets.py)**

#### **Problema:**
- Sistema tentava usar HashiCorp Vault por padrão
- Não tinha VAULT_TOKEN configurado
- Classe `EnvSecretsManager` não estava sendo reconhecida
- Causava erro fatal na inicialização

#### **Solução:**
- **Reorganizada ordem das classes** - `EnvSecretsManager` definida antes de ser usada
- **Adicionado tratamento de exceções** no `_initialize_secrets_manager`
- **Fallback automático** para variáveis de ambiente quando qualquer erro ocorre
- **Múltiplos nomes de secrets** para maior compatibilidade
- **Mapeamento de secrets** para variáveis de ambiente:

```python
env_mapping = {
    'openai-api-key': 'OPENAI_API_KEY',
    'pinecone-api-key': 'PINECONE_API_KEY',
    'jwt-secret': 'JWT_SECRET_KEY',
    'supabase-url': 'SUPABASE_URL',
    'supabase-anon-key': 'SUPABASE_ANON_KEY',
    'supabase-service-role-key': 'SUPABASE_SERVICE_ROLE_KEY',
    'redis-url': 'REDIS_URL',
    'redis-host': 'REDIS_HOST',
    'redis-port': 'REDIS_PORT',
    'redis-password': 'REDIS_PASSWORD',
    'redis-username': 'REDIS_USERNAME'
}
```

### **2. Sistema de Cache Redis (backend/app/core/cache.py)**

#### **Problema:**
- Redis configurado para conectar em `ngabi_ngabi-redis:6379`
- No ambiente local/VPS não existe esse host
- Causava erro de conexão recusada

#### **Solução:**
- **Configuração dinâmica** do Redis URL via variável de ambiente
- **Fallback para localhost** quando REDIS_URL não está configurada
- **Tratamento tolerante de erros** - aplicação continua funcionando sem cache
- **Logs de warning** em vez de erro fatal

```python
# Usar variável de ambiente ou fallback para localhost
self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379')
```

## 🌍 **Variáveis de Ambiente para VPS**

### **Backend (EasyPanel)**
```bash
# Secrets Provider
SECRETS_PROVIDER=env

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OpenAI
OPENAI_API_KEY=your-openai-key

# Redis (EasyPanel)
REDIS_URL=redis://default:password@redis-host:6379
REDIS_HOST=redis-host
REDIS_PORT=6379
REDIS_PASSWORD=password
REDIS_USERNAME=default

# App Config
APP_NAME=nGabi
APP_VERSION=1.0.0
ENVIRONMENT=homologacao
DEBUG=false
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_CHAT=200
RATE_LIMIT_AUTH=100
RATE_LIMIT_API=500

# CORS
CORS_ORIGINS=https://ngabi.ness.tec.br,http://localhost:3000
```

### **Frontend (EasyPanel)**
```bash
# API Base URL
VITE_API_BASE_URL=https://ngabi.ness.tec.br/backend

# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# OpenAI (para testes diretos)
VITE_OPENAI_API_KEY=your-openai-key

# Environment
NODE_ENV=production
```

## 🚀 **Configuração EasyPanel**

### **1. Backend**
- **Dockerfile Path:** `backend/Dockerfile`
- **Porta:** 8000
- **Path:** `/backend`
- **Build Command:** `docker build -t ngabi-backend .`
- **Start Command:** `docker run -p 8000:8000 ngabi-backend`

### **2. Frontend**
- **Dockerfile Path:** `frontend/Dockerfile`
- **Porta:** 3000
- **Path:** `/`
- **Build Command:** `docker build -t ngabi-frontend .`
- **Start Command:** `docker run -p 3000:3000 ngabi-frontend`

### **3. Redis**
- **Tipo:** Redis
- **Porta:** 6379
- **Credenciais:** Fornecidas pelo EasyPanel

## 📋 **Checklist de Deploy**

### **✅ Pré-Deploy**
- [x] Dockerfiles criados
- [x] Sistema de secrets corrigido
- [x] Sistema de cache corrigido
- [x] Variáveis de ambiente documentadas
- [x] Código commitado no GitHub

### **✅ EasyPanel**
- [ ] Criar projeto `ngabi-homologacao`
- [ ] Configurar domínio `ngabi.ness.tec.br`
- [ ] Conectar repositório GitHub
- [ ] Configurar variáveis de ambiente
- [ ] Configurar Dockerfiles
- [ ] Habilitar auto-deploy

### **✅ Pós-Deploy**
- [ ] Testar health checks
- [ ] Testar funcionalidades
- [ ] Verificar logs
- [ ] Configurar monitoramento

## 🎯 **URLs de Homologação**

- **Frontend:** `https://ngabi.ness.tec.br`
- **Backend API:** `https://ngabi.ness.tec.br/backend`
- **Documentação:** `https://ngabi.ness.tec.br/backend/docs`
- **Health Check:** `https://ngabi.ness.tec.br/backend/health`

## 🔧 **Comandos de Teste**

### **Health Checks**
```bash
# Backend
curl https://ngabi.ness.tec.br/backend/health

# Frontend
curl https://ngabi.ness.tec.br

# Redis
curl https://ngabi.ness.tec.br/backend/health/redis
```

### **Testes de Funcionalidade**
```bash
# Chat API
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como posso ajudar?"}'

# Agentes Especialistas
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/agents/specialists/customer-support/langchain" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test_message": "Tenho um problema técnico"}'
```

## 🎉 **Status Final**

**✅ Problemas Corrigidos:**
- [x] Erro do Vault Token resolvido
- [x] Erro do Redis resolvido
- [x] Erro do Secrets Provider resolvido
- [x] Sistema tolerante a falhas
- [x] Logs informativos
- [x] Fallbacks configurados
- [x] Múltiplos nomes de secrets suportados

**🚀 Pronto para Deploy:**
- [x] Dockerfiles otimizados
- [x] Variáveis de ambiente documentadas
- [x] Configuração EasyPanel pronta
- [x] Sistema robusto e tolerante
- [x] Tratamento de exceções melhorado

**Agora é só configurar no EasyPanel e fazer o deploy!** 🎯 