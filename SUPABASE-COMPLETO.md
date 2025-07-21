# 🔐 Configuração Completa n.Gabi - Easypanel

## 📋 **VARIÁVEIS PARA O SERVIÇO SUPABASE**

### **Todas as variáveis necessárias para o Supabase:**

```env
############
# Secrets
# YOU MUST CHANGE THESE BEFORE GOING INTO PRODUCTION
############

POSTGRES_PASSWORD=your-super-secret-and-long-postgres-password
JWT_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
DASHBOARD_USERNAME=supabase
DASHBOARD_PASSWORD=this_password_is_insecure_and_should_be_updated
SECRET_KEY_BASE=UpNVntn3cDxHJpq99YMc1T1AQgQpc8kfYTuRgBiYa15BLrx8etQoXz3gZv1/u2oq
VAULT_ENC_KEY=your-encryption-key-32-chars-min

############
# Database - You can change these to any PostgreSQL database that has logical replication enabled.
############

POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
# default user is postgres

############
# Supavisor -- Database pooler
############

POOLER_PROXY_PORT_TRANSACTION=6543
POOLER_DEFAULT_POOL_SIZE=20
POOLER_MAX_CLIENT_CONN=100
POOLER_TENANT_ID=your-tenant-id

############
# API Proxy - Configuration for the Kong Reverse proxy.
############

KONG_HTTP_PORT=8000
KONG_HTTPS_PORT=8443

############
# API - Configuration for PostgREST.
############

PGRST_DB_SCHEMAS=public,storage,graphql_public

############
# Auth - Configuration for the GoTrue authentication server.
############

## General
SITE_URL=http://localhost:3000
ADDITIONAL_REDIRECT_URLS=
JWT_EXPIRY=3600
DISABLE_SIGNUP=false
API_EXTERNAL_URL=http://localhost:8000

## Mailer Config
MAILER_URLPATHS_CONFIRMATION="/auth/v1/verify"
MAILER_URLPATHS_INVITE="/auth/v1/verify"
MAILER_URLPATHS_RECOVERY="/auth/v1/verify"
MAILER_URLPATHS_EMAIL_CHANGE="/auth/v1/verify"

## Email auth
ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=false
SMTP_ADMIN_EMAIL=admin@example.com
SMTP_HOST=supabase-mail
SMTP_PORT=2500
SMTP_USER=fake_mail_user
SMTP_PASS=fake_mail_password
SMTP_SENDER_NAME=fake_sender
ENABLE_ANONYMOUS_USERS=false

## Phone auth
ENABLE_PHONE_SIGNUP=true
ENABLE_PHONE_AUTOCONFIRM=true

############
# Studio - Configuration for the Dashboard
############

STUDIO_DEFAULT_ORGANIZATION=Default Organization
STUDIO_DEFAULT_PROJECT=Default Project

STUDIO_PORT=3000
# replace if you intend to use Studio outside of localhost
SUPABASE_PUBLIC_URL=http://localhost:8000

# Enable webp support
IMGPROXY_ENABLE_WEBP_DETECTION=true

# Add your OpenAI API key to enable SQL Editor Assistant
OPENAI_API_KEY=

############
# Functions - Configuration for Functions
############
# NOTE: VERIFY_JWT applies to all functions. Per-function VERIFY_JWT is not supported yet.
FUNCTIONS_VERIFY_JWT=false

############
# Logs - Configuration for Logflare
# Please refer to https://supabase.com/docs/reference/self-hosting-analytics/introduction
############

LOGFLARE_LOGGER_BACKEND_API_KEY=your-super-secret-and-long-logflare-key

# Change vector.toml sinks to reflect this change
LOGFLARE_API_KEY=your-super-secret-and-long-logflare-key

# Docker socket location - this value will differ depending on your OS
DOCKER_SOCKET_LOCATION=/var/run/docker.sock
```

## 📋 **VARIÁVEIS PARA O SERVIÇO ngabi-backend**

```env
SUPABASE_URL=http://supabase:8000
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
REDIS_URL=redis://ngabi-redis:6379
JWT_SECRET_KEY=your-super-secret-jwt-token-with-at-least-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br
```

## 📋 **VARIÁVEIS PARA O SERVIÇO ngabi-frontend**

```env
VITE_API_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
```

## 📋 **VARIÁVEIS PARA O SERVIÇO ngabi-n8n**

```env
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=NgabiN8n2024!Admin
WEBHOOK_URL=https://n8n.ngabi.ness.tec.br
```

## 🌐 **CONFIGURAÇÃO DE DOMÍNIOS**

### **DNS Records (A Records)**
```
ngabi.ness.tec.br → SEU_IP_DA_VPS
api.ngabi.ness.tec.br → SEU_IP_DA_VPS
n8n.ngabi.ness.tec.br → SEU_IP_DA_VPS
```

### **Traefik Labels (para cada serviço)**
```yaml
# Frontend
- "traefik.enable=true"
- "traefik.http.routers.ngabi-frontend.rule=Host(`ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-frontend.tls=true"

# Backend
- "traefik.enable=true"
- "traefik.http.routers.ngabi-backend.rule=Host(`api.ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-backend.tls=true"

# n8n
- "traefik.enable=true"
- "traefik.http.routers.ngabi-n8n.rule=Host(`n8n.ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-n8n.tls=true"
```

## 📦 **ORDEM DE DEPLOY**

### **1. Supabase (já instalado)**
- ✅ Copiar todas as variáveis do bloco acima
- ✅ Verificar se está rodando

### **2. Serviços n.Gabi**
```bash
1. ngabi-redis (Redis: redis:7-alpine, Porta: 6379)
2. ngabi-backend (GitHub: resper1965/ngabi, Caminho: /backend, Porta: 8000)
3. ngabi-frontend (GitHub: resper1965/ngabi, Caminho: /frontend, Porta: 3000)
4. ngabi-n8n (Docker: n8nio/n8n:latest, Porta: 5678)
```

## 🎯 **PONTOS IMPORTANTES**

- **SUPABASE_URL**: Use `http://supabase:8000` para conexão interna
- **JWT_SECRET**: Mesmo valor para Supabase e ngabi-backend
- **ANON_KEY**: Mantenha exatamente como fornecido
- **Domínios**: Configure DNS A Records antes do deploy

## ✅ **CHECKLIST FINAL**

- [ ] Supabase com todas as variáveis configuradas
- [ ] DNS A Records configurados
- [ ] ngabi-redis deployado
- [ ] ngabi-backend com variáveis corretas
- [ ] ngabi-frontend com variáveis corretas
- [ ] ngabi-n8n com variáveis corretas
- [ ] Traefik labels configurados
- [ ] Teste de conexão funcionando

## 🚀 **RESULTADO FINAL**

```
✅ ngabi.ness.tec.br → Frontend React
✅ api.ngabi.ness.tec.br → Backend FastAPI + Supabase
✅ n8n.ngabi.ness.tec.br → n8n Workflows
```

**Todos os serviços funcionando e conectados!** 🎉 