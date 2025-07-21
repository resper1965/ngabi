# 🔧 Variáveis de Ambiente COMPLETAS para Supabase

## 📋 **Todas as Variáveis Necessárias para ngabi-supabase:**

```env
# ========================================
# CONFIGURAÇÃO BÁSICA
# ========================================
SUPABASE_PUBLIC_URL=https://sup.ngabi.ness.tec.br
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

# ========================================
# POSTGRES CONFIGURATION
# ========================================
POSTGRES_HOST=ngabi-supabase-db
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# ========================================
# JWT CONFIGURATION
# ========================================
JWT_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
JWT_EXPIRY=3600
JWT_REFRESH_EXPIRY=2592000

# ========================================
# API CONFIGURATION
# ========================================
API_EXTERNAL_URL=https://sup.ngabi.ness.tec.br
SITE_URL=https://sup.ngabi.ness.tec.br

# ========================================
# DASHBOARD CONFIGURATION
# ========================================
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=ngabi2024!

# ========================================
# AUTH CONFIGURATION
# ========================================
ENABLE_SIGNUP=true
ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=true
ENABLE_PHONE_SIGNUP=false
ENABLE_PHONE_AUTOCONFIRM=false
ENABLE_ANONYMOUS_USERS=false
DISABLE_SIGNUP=false

# ========================================
# MAILER CONFIGURATION
# ========================================
MAILER_URLPATHS_CONFIRMATION=https://sup.ngabi.ness.tec.br/auth/confirm
MAILER_URLPATHS_RECOVERY=https://sup.ngabi.ness.tec.br/auth/recovery
MAILER_URLPATHS_INVITE=https://sup.ngabi.ness.tec.br/auth/invite
MAILER_URLPATHS_EMAIL_CHANGE=https://sup.ngabi.ness.tec.br/auth/email-change

# ========================================
# STUDIO CONFIGURATION
# ========================================
STUDIO_DEFAULT_ORGANIZATION=ngabi
STUDIO_DEFAULT_PROJECT=ngabi

# ========================================
# LOGFLARE CONFIGURATION
# ========================================
LOGFLARE_API_KEY=

# ========================================
# SECURITY CONFIGURATION
# ========================================
SECRET_KEY_BASE=your-super-secret-key-base-with-at-least-64-characters-long-for-production-use
VAULT_ENC_KEY=your-vault-encryption-key-with-at-least-32-characters

# ========================================
# FUNCTIONS CONFIGURATION
# ========================================
FUNCTIONS_VERIFY_JWT=true

# ========================================
# POOLER CONFIGURATION
# ========================================
POOLER_DEFAULT_POOL_SIZE=15
POOLER_MAX_CLIENT_CONN=100
POOLER_TENANT_ID=ngabi

# ========================================
# PGRST CONFIGURATION
# ========================================
PGRST_DB_SCHEMAS=public,storage,graphql_public

# ========================================
# IMGPROXY CONFIGURATION
# ========================================
IMGPROXY_ENABLE_WEBP_DETECTION=true

# ========================================
# DOCKER CONFIGURATION
# ========================================
DOCKER_SOCKET_LOCATION=/var/run/docker.sock

# ========================================
# ADDITIONAL CONFIGURATION
# ========================================
ADDITIONAL_REDIRECT_URLS=https://chat.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br
```

## 🎯 **Como Configurar no Easypanel:**

### **1. Acessar o Serviço Supabase**
1. Vá para o Easypanel Dashboard
2. Acesse o projeto `ngabi`
3. Vá para o serviço `ngabi-supabase`
4. Clique em **"Environment Variables"**

### **2. Adicionar Todas as Variáveis**
Copie e cole todas as variáveis acima no campo de variáveis de ambiente.

### **3. Configuração Específica**
- **Domínio**: `sup.ngabi.ness.tec.br`
- **Porta**: `54321`
- **Protocolo**: `HTTPS`

## ✅ **Checklist de Configuração:**

- [ ] ✅ Todas as variáveis básicas configuradas
- [ ] ✅ PostgreSQL configurado
- [ ] ✅ JWT configurado
- [ ] ✅ Dashboard configurado
- [ ] ✅ Auth configurado
- [ ] ✅ Mailer configurado
- [ ] ✅ Security configurado
- [ ] ✅ Deploy realizado

## 🧪 **Testar após Configuração:**

```bash
# Testar Supabase
curl https://sup.ngabi.ness.tec.br/rest/v1/

# Testar Dashboard
curl https://sup.ngabi.ness.tec.br/auth/v1/health

# Testar API
curl https://sup.ngabi.ness.tec.br/rest/v1/tenants
```

## 🚨 **Notas Importantes:**

1. **SECRET_KEY_BASE**: Deve ter pelo menos 64 caracteres
2. **VAULT_ENC_KEY**: Deve ter pelo menos 32 caracteres
3. **JWT_SECRET**: Deve ter pelo menos 32 caracteres
4. **POSTGRES_HOST**: Deve ser o nome do container do banco
5. **DOCKER_SOCKET_LOCATION**: Deve apontar para o socket do Docker

**Configure todas essas variáveis e faça o deploy novamente!** 🚀 