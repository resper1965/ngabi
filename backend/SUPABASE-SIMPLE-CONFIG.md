# 🔧 Configuração SIMPLIFICADA para Supabase com PostgreSQL Interno

## 📋 **Variáveis MÍNIMAS para ngabi-supabase:**

```env
# ========================================
# CONFIGURAÇÃO BÁSICA (OBRIGATÓRIO)
# ========================================
SUPABASE_PUBLIC_URL=https://sup.ngabi.ness.tec.br
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

# ========================================
# POSTGRES INTERNO (OBRIGATÓRIO)
# ========================================
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# ========================================
# SECURITY (OBRIGATÓRIO)
# ========================================
SECRET_KEY_BASE=ngabi-super-secret-key-base-with-at-least-64-characters-long-for-production-use-2024
VAULT_ENC_KEY=ngabi-vault-encryption-key-32-chars-2024

# ========================================
# DASHBOARD (OBRIGATÓRIO)
# ========================================
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=ngabi2024!

# ========================================
# AUTH (OBRIGATÓRIO)
# ========================================
ENABLE_SIGNUP=true
ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=true
ENABLE_PHONE_SIGNUP=false
ENABLE_PHONE_AUTOCONFIRM=false
ENABLE_ANONYMOUS_USERS=false
DISABLE_SIGNUP=false

# ========================================
# MAILER (OBRIGATÓRIO)
# ========================================
MAILER_URLPATHS_CONFIRMATION=https://sup.ngabi.ness.tec.br/auth/confirm
MAILER_URLPATHS_RECOVERY=https://sup.ngabi.ness.tec.br/auth/recovery
MAILER_URLPATHS_INVITE=https://sup.ngabi.ness.tec.br/auth/invite
MAILER_URLPATHS_EMAIL_CHANGE=https://sup.ngabi.ness.tec.br/auth/email-change

# ========================================
# STUDIO (OBRIGATÓRIO)
# ========================================
STUDIO_DEFAULT_ORGANIZATION=ngabi
STUDIO_DEFAULT_PROJECT=ngabi

# ========================================
# FUNCTIONS (OBRIGATÓRIO)
# ========================================
FUNCTIONS_VERIFY_JWT=true

# ========================================
# POOLER (OBRIGATÓRIO)
# ========================================
POOLER_DEFAULT_POOL_SIZE=15
POOLER_MAX_CLIENT_CONN=100
POOLER_TENANT_ID=ngabi

# ========================================
# PGRST (OBRIGATÓRIO)
# ========================================
PGRST_DB_SCHEMAS=public,storage,graphql_public

# ========================================
# IMGPROXY (OBRIGATÓRIO)
# ========================================
IMGPROXY_ENABLE_WEBP_DETECTION=true

# ========================================
# DOCKER (OBRIGATÓRIO)
# ========================================
DOCKER_SOCKET_LOCATION=/var/run/docker.sock

# ========================================
# ADDITIONAL (OBRIGATÓRIO)
# ========================================
ADDITIONAL_REDIRECT_URLS=https://chat.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br

# ========================================
# LOGFLARE (OPCIONAL - pode ficar vazio)
# ========================================
LOGFLARE_API_KEY=
```

## 🎯 **Principais Pontos:**

### **1. POSTGRES_HOST=localhost**
- ✅ Usa PostgreSQL interno do Supabase
- ✅ Não precisa de container separado

### **2. Configuração Mínima**
- ✅ Apenas variáveis essenciais
- ✅ Sem configurações complexas

### **3. Security Keys**
- ✅ Chaves seguras e longas
- ✅ Compatíveis com Supabase

## 🔧 **Como Aplicar:**

### **1. Acessar Easypanel**
1. Vá para o serviço `ngabi-supabase`
2. Clique em **"Environment Variables"**

### **2. Limpar e Adicionar**
1. **REMOVER** todas as variáveis antigas
2. **ADICIONAR** apenas as variáveis acima
3. **SALVAR** as alterações

### **3. Fazer Deploy**
1. Clique em **"Deploy"**
2. Aguarde o build completo
3. Verifique os logs

## ✅ **Checklist:**

- [ ] 🔧 Limpar todas as variáveis antigas
- [ ] ✅ Adicionar apenas as variáveis essenciais
- [ ] 🔄 Fazer deploy do Supabase
- [ ] 🧪 Verificar se PostgreSQL interno inicia
- [ ] 🗄️ Criar tabelas no Supabase
- [ ] 🧪 Testar todas as conexões

## 🚨 **Se ainda não funcionar:**

Se o PostgreSQL interno ainda não funcionar, podemos:
1. Verificar logs detalhados
2. Tentar configuração alternativa
3. Usar PostgreSQL separado como fallback

**Agora configure essas variáveis simplificadas e faça o deploy!** 🚀 