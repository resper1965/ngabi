# 🔧 Variáveis CORRIGIDAS para Deploy do Supabase

## 📋 **Variáveis para ngabi-supabase (CORRIGIDAS):**

```env
# ========================================
# CONFIGURAÇÃO BÁSICA
# ========================================
SUPABASE_PUBLIC_URL=https://sup.ngabi.ness.tec.br
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

# ========================================
# POSTGRES CONFIGURATION (CORRIGIDO)
# ========================================
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# ========================================
# SECURITY CONFIGURATION
# ========================================
SECRET_KEY_BASE=ngabi-super-secret-key-base-with-at-least-64-characters-long-for-production-use-2024
VAULT_ENC_KEY=ngabi-vault-encryption-key-32-chars-2024

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

# ========================================
# LOGFLARE CONFIGURATION
# ========================================
LOGFLARE_API_KEY=
```

## 🎯 **Principais Correções:**

### **1. POSTGRES_HOST**
- **ANTES**: `ngabi-supabase-db` ❌
- **DEPOIS**: `localhost` ✅

### **2. POSTGRES_PORT**
- **MANTIDO**: `5432` ✅

## 🔧 **Como Aplicar:**

### **1. Acessar Easypanel**
1. Vá para o serviço `ngabi-supabase`
2. Clique em **"Environment Variables"**

### **2. Atualizar Variáveis**
1. **REMOVER** a variável `POSTGRES_HOST=ngabi-supabase-db`
2. **ADICIONAR** `POSTGRES_HOST=localhost`
3. **MANTER** todas as outras variáveis

### **3. Fazer Deploy**
1. Clique em **"Deploy"**
2. Aguarde o build
3. Verifique se o erro de conexão desapareceu

## ✅ **Checklist:**

- [ ] 🔧 Atualizar `POSTGRES_HOST=localhost`
- [ ] 🔄 Fazer deploy do Supabase
- [ ] 🧪 Verificar se erro de conexão desapareceu
- [ ] 🗄️ Criar tabelas no Supabase
- [ ] 🧪 Testar todas as conexões

**Agora atualize a variável POSTGRES_HOST e faça o deploy!** 🚀 