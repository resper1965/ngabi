# 🔧 Variáveis de Ambiente - EasyUIPanel

## 📋 **Configuração do Backend**

### **Variáveis Obrigatórias:**
```bash
# Supabase (Database + Auth)
SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd
SUPABASE_SERVICE_ROLE_KEY=sb_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5ZWlmeHZ4aWZocmFwZmR2ZnJ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMzQ5NzI5MCwiZXhwIjoyMDQ5MDczMjkwfQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8

# OpenAI (LLM)
OPENAI_API_KEY=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

# Redis (Cache - EasyUIPanel)
REDIS_URL=redis://default:6cebb38271cd2fea746a@ngabi_ngabi-redis:6379
REDIS_HOST=ngabi_ngabi-redis
REDIS_PORT=6379
REDIS_PASSWORD=6cebb38271cd2fea746a
REDIS_USERNAME=default

# Aplicação
APP_NAME=n.Gabi
APP_VERSION=2.0.0
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### **Variáveis Opcionais:**
```bash
# Cache
CACHE_ENABLED=true
CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT=100
RATE_LIMIT_CHAT=20
CHAT_RATE_LIMIT=10/minute

# CORS
CORS_ORIGINS=https://ngabi.ness.tec.br,http://localhost:3000

# AI/Chat
DEFAULT_CHAT_MODEL=gpt-3.5-turbo
MAX_TOKENS=2048
TEMPERATURE=0.7

# Eventos
EVENTS_ENABLED=true
WEBHOOKS_ENABLED=true

# Logs
LOG_FORMAT=json
```

## 📋 **Configuração do Frontend**

### **Variáveis Obrigatórias:**
```bash
# API Backend
VITE_API_BASE_URL=https://api.ngabi.ness.tec.br

# Supabase
VITE_SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd

# OpenAI (para testes diretos)
VITE_OPENAI_API_KEY=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
```

### **Variáveis Opcionais:**
```bash
# Aplicação
VITE_APP_NAME=n.Gabi
VITE_APP_VERSION=2.0.0
VITE_ENVIRONMENT=production

# Debug
VITE_DEBUG=false
VITE_LOG_LEVEL=info

# Features
VITE_CHAT_ENABLED=true
VITE_AGENTS_ENABLED=true
VITE_STREAMING_ENABLED=true
```

## 🚀 **Como Configurar no EasyUIPanel**

### **1. Backend Service:**
1. **Nome**: `ngabi-backend`
2. **Repositório**: `https://github.com/seu-usuario/ngabi`
3. **Branch**: `main`
4. **Dockerfile**: `backend/Dockerfile`
5. **Porta**: `8000`
6. **Domínio**: `api.ngabi.ness.tec.br`

### **2. Frontend Service:**
1. **Nome**: `ngabi-frontend`
2. **Repositório**: `https://github.com/seu-usuario/ngabi`
3. **Branch**: `main`
4. **Dockerfile**: `frontend/Dockerfile`
5. **Porta**: `3000`
6. **Domínio**: `ngabi.ness.tec.br`

### **3. Redis Service:**
1. **Nome**: `ngabi-redis`
2. **Imagem**: `redis:7-alpine`
3. **Porta**: `6379`
4. **Usuário**: `default`
5. **Senha**: `6cebb38271cd2fea746a`

## 🔗 **URLs de Conexão**

### **Backend APIs:**
- **Base URL**: `https://api.ngabi.ness.tec.br`
- **Health Check**: `https://api.ngabi.ness.tec.br/health`
- **Docs**: `https://api.ngabi.ness.tec.br/docs`

### **Frontend:**
- **URL**: `https://ngabi.ness.tec.br`
- **Admin**: `https://ngabi.ness.tec.br/admin`

### **Redis:**
- **URL Interna**: `redis://default:6cebb38271cd2fea746a@ngabi_ngabi-redis:6379`
- **Host**: `ngabi_ngabi-redis`
- **Porta**: `6379`

## ✅ **Verificação de Configuração**

### **Teste Backend:**
```bash
# Health Check
curl https://api.ngabi.ness.tec.br/health

# Teste Chat
curl -X POST https://api.ngabi.ness.tec.br/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!", "agent_id": "default"}'
```

### **Teste Frontend:**
```bash
# Verificar se carrega
curl https://ngabi.ness.tec.br

# Verificar variáveis
curl https://ngabi.ness.tec.br/api/config
```

### **Teste Redis:**
```bash
# Via container
docker exec ngabi_ngabi-redis redis-cli -a 6cebb38271cd2fea746a ping

# Via aplicação
curl https://api.ngabi.ness.tec.br/api/v1/health/cache
```

## 🎯 **Próximos Passos**

1. **Configurar variáveis** no EasyUIPanel
2. **Fazer deploy** dos serviços
3. **Testar conexões** entre serviços
4. **Verificar SSL** automático
5. **Monitorar logs** e performance

**✅ Tudo configurado para o EasyUIPanel!** 🚀✨ 