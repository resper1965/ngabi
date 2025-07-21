# 🔧 Configuração CORRETA do Backend no Easypanel

## 🚨 **PROBLEMA IDENTIFICADO:**

O Easypanel está usando variáveis antigas (SQLAlchemy) ao invés das novas variáveis do Supabase.

## 📋 **Variáveis CORRETAS para ngabi-backend:**

### **🔑 Variáveis de Ambiente (Environment Variables):**

```env
# Supabase Configuration
SUPABASE_URL=https://sup.ngabi.ness.tec.br
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0

# Redis Configuration
REDIS_URL=redis://ngabi-redis:6379

# CORS Configuration
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://chat.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br,https://sup.ngabi.ness.tec.br

# Application Configuration
APP_NAME=n.Gabi Backend
APP_VERSION=2.0.0
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Metrics
ENABLE_METRICS=true
```

### **🔑 Build Args (REMOVER TODOS OS ANTIGOS):**

**❌ REMOVER estas variáveis antigas:**
- `DATABASE_URL`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `ELASTICSEARCH_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `N8N_BASIC_AUTH_USER`
- `N8N_BASIC_AUTH_PASSWORD`
- `WEBHOOK_URL`

**✅ MANTER apenas:**
- `GIT_SHA` (automático)

## 🎯 **Como Configurar no Easypanel:**

### **1. Acessar o Serviço Backend**
1. Vá para o Easypanel Dashboard
2. Acesse o projeto `ngabi`
3. Vá para o serviço `ngabi-backend`

### **2. Configurar Environment Variables**
1. Clique em **"Environment Variables"**
2. **REMOVER** todas as variáveis antigas
3. **ADICIONAR** apenas as variáveis do Supabase (acima)

### **3. Configurar Build Args**
1. Clique em **"Build Arguments"**
2. **REMOVER** todos os build args antigos
3. **MANTER** apenas `GIT_SHA` (se existir)

### **4. Configuração de Domínio**
- **Host**: `api.ngabi.ness.tec.br`
- **Porta**: `8000`
- **Protocolo**: `HTTP`
- **HTTPS**: Habilitado

## ✅ **Checklist de Correção:**

- [ ] ❌ Remover variáveis antigas (DATABASE_URL, POSTGRES_*, etc.)
- [ ] ✅ Adicionar variáveis Supabase (SUPABASE_URL, SUPABASE_ANON_KEY)
- [ ] ❌ Remover build args antigos
- [ ] ✅ Configurar CORS corretamente
- [ ] 🔄 Fazer deploy novamente

## 🧪 **Testar após Correção:**

```bash
# Health Check
curl https://api.ngabi.ness.tec.br/health

# Testar Supabase
curl https://api.ngabi.ness.tec.br/api/v1/auth/check
```

## 🚨 **Erro Atual:**
```
Command failed with exit code 1: docker buildx build --network host -f /etc/easypanel/projects/ngabi/ngabi-backend/code/backend/Dockerfile -t easypanel/ngabi/ngabi-backend --label 'keep=true' --build-arg 'DATABASE_URL=postgresql://postgres:NgabiDB2024!Secure@postgres:5432/chat_agents' --build-arg 'POSTGRES_USER=postgres' --build-arg 'POSTGRES_PASSWORD=NgabiDB2024!Secure' --build-arg 'POSTGRES_DB=chat_agents' --build-arg 'REDIS_URL=redis://redis:6379' --build-arg 'ELASTICSEARCH_URL=http://elasticsearch:9200' --build-arg 'N8N_BASIC_AUTH_USER=admin' --build-arg 'N8N_BASIC_AUTH_PASSWORD=NgabiN8n2024!Admin' --build-arg 'WEBHOOK_URL=https://n8n.ngabi.ness.tec.br' --build-arg 'JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKey123' --build-arg 'JWT_ALGORITHM=HS256' --build-arg 'ACCESS_TOKEN_EXPIRE_MINUTES=30' --build-arg 'CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br' --build-arg 'GIT_SHA=629a4af03d99afa79a2bd49a375136451c621de6'
```

**SOLUÇÃO: Remover TODOS os build args antigos e usar apenas as variáveis de ambiente do Supabase!** 🚀 