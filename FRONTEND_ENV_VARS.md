# 🔧 Variáveis de Ambiente do Frontend - n.Gabi

## 📋 **Variáveis Obrigatórias:**

### **🌐 URLs da API:**
```bash
# URL base da API (desenvolvimento)
VITE_API_BASE_URL=http://localhost:8000

# URL base da API (produção)
VITE_API_BASE_URL=https://api.ngabi.ness.tec.br
```

### **🔐 Supabase (Obrigatório):**
```bash
# URL do Supabase
VITE_SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co

# Chave anônima do Supabase
VITE_SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd
```

### **🤖 OpenAI (Obrigatório para Chat):**
```bash
# OpenAI API Key
VITE_OPENAI_API_KEY=your-openai-api-key

# Modelo OpenAI padrão
VITE_OPENAI_MODEL=gpt-3.5-turbo

# Temperatura do modelo (0.0 a 2.0)
VITE_OPENAI_TEMPERATURE=0.7

# Máximo de tokens por resposta
VITE_OPENAI_MAX_TOKENS=2048
```

## 📋 **Variáveis Opcionais:**

### **🏭 Configurações de Produção:**
```bash
# Domínio de produção
VITE_PRODUCTION_DOMAIN=ngabi.ness.tec.br

# Protocolo de produção
VITE_PRODUCTION_PROTOCOL=https

# URL da API de produção
VITE_PRODUCTION_API_URL=https://api.ngabi.ness.tec.br
```

### **🛠️ Configurações de Desenvolvimento:**
```bash
# Domínio de desenvolvimento
VITE_DEVELOPMENT_DOMAIN=localhost:3000

# Protocolo de desenvolvimento
VITE_DEVELOPMENT_PROTOCOL=http

# URL da API de desenvolvimento
VITE_DEVELOPMENT_API_URL=http://localhost:8000
```

### **⚙️ Configurações do App:**
```bash
# Nome da aplicação
VITE_APP_NAME=n.Gabi

# Versão da aplicação
VITE_APP_VERSION=1.0.0

# Ambiente
VITE_NODE_ENV=development
```

### **🐛 Configurações de Debug:**
```bash
# Habilitar debug
VITE_DEBUG=true

# Nível de log
VITE_LOG_LEVEL=debug
```

### **🚀 Configurações de Features:**
```bash
# Habilitar chat em streaming
VITE_ENABLE_STREAMING=true

# Habilitar cache local
VITE_ENABLE_CACHE=true

# Habilitar analytics
VITE_ENABLE_ANALYTICS=false
```

### **🔒 Configurações de Segurança:**
```bash
# Timeout das requisições (em ms)
VITE_API_TIMEOUT=30000

# Habilitar HTTPS em produção
VITE_FORCE_HTTPS=true
```

### **⚡ Configurações de Performance:**
```bash
# Tamanho do cache (em MB)
VITE_CACHE_SIZE=50

# TTL do cache (em segundos)
VITE_CACHE_TTL=3600
```

### **🎨 Configurações de UI/UX:**
```bash
# Tema padrão (light, dark, system)
VITE_DEFAULT_THEME=system

# Habilitar animações
VITE_ENABLE_ANIMATIONS=true

# Habilitar transições suaves
VITE_ENABLE_TRANSITIONS=true
```

### **📊 Configurações de Monitoramento:**
```bash
# Habilitar error tracking
VITE_ENABLE_ERROR_TRACKING=false

# URL do serviço de monitoramento
VITE_MONITORING_URL=
```

### **🧪 Configurações de Teste:**
```bash
# Habilitar modo de teste
VITE_TEST_MODE=false

# URL da API de teste
VITE_TEST_API_URL=http://localhost:8001
```

## 🚀 **Como Configurar:**

### **1. Desenvolvimento Local:**
```bash
# Copiar arquivo de exemplo
cp frontend/env.example frontend/.env

# Editar variáveis necessárias
nano frontend/.env
```

### **2. Produção:**
```bash
# Criar arquivo .env na produção
VITE_API_BASE_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd
VITE_PRODUCTION_DOMAIN=ngabi.ness.tec.br
VITE_PRODUCTION_PROTOCOL=https
VITE_NODE_ENV=production
VITE_DEBUG=false
```

### **3. Docker:**
```yaml
# docker-compose.yml
environment:
  - VITE_API_BASE_URL=http://backend:8000
  - VITE_SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
  - VITE_SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd
```

## 📝 **Exemplo de .env Completo:**

```bash
# =============================================================================
# CONFIGURAÇÕES DO FRONTEND - n.Gabi
# =============================================================================

# URLs DA API
VITE_API_BASE_URL=http://localhost:8000
VITE_PRODUCTION_API_URL=https://api.ngabi.ness.tec.br

# SUPABASE CONFIGURAÇÃO
VITE_SUPABASE_URL=https://hyeifxvxifhrapfdvfry.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd

# OPENAI CONFIGURAÇÃO
VITE_OPENAI_API_KEY=your-openai-api-key
VITE_OPENAI_MODEL=gpt-3.5-turbo
VITE_OPENAI_TEMPERATURE=0.7
VITE_OPENAI_MAX_TOKENS=2048

# CONFIGURAÇÕES DE PRODUÇÃO
VITE_PRODUCTION_DOMAIN=ngabi.ness.tec.br
VITE_PRODUCTION_PROTOCOL=https

# CONFIGURAÇÕES DE DESENVOLVIMENTO
VITE_DEVELOPMENT_DOMAIN=localhost:3000
VITE_DEVELOPMENT_PROTOCOL=http

# CONFIGURAÇÕES DO APP
VITE_APP_NAME=n.Gabi
VITE_APP_VERSION=1.0.0
VITE_NODE_ENV=development

# CONFIGURAÇÕES DE DEBUG
VITE_DEBUG=true
VITE_LOG_LEVEL=debug

# CONFIGURAÇÕES DE FEATURES
VITE_ENABLE_STREAMING=true
VITE_ENABLE_CACHE=true
VITE_ENABLE_ANALYTICS=false

# CONFIGURAÇÕES DE SEGURANÇA
VITE_API_TIMEOUT=30000
VITE_FORCE_HTTPS=true

# CONFIGURAÇÕES DE PERFORMANCE
VITE_CACHE_SIZE=50
VITE_CACHE_TTL=3600

# CONFIGURAÇÕES DE UI/UX
VITE_DEFAULT_THEME=system
VITE_ENABLE_ANIMATIONS=true
VITE_ENABLE_TRANSITIONS=true

# CONFIGURAÇÕES DE MONITORAMENTO
VITE_ENABLE_ERROR_TRACKING=false
VITE_MONITORING_URL=

# CONFIGURAÇÕES DE TESTE
VITE_TEST_MODE=false
VITE_TEST_API_URL=http://localhost:8001
```

## ⚠️ **Importante:**

### **🔐 Segurança:**
- ✅ **NUNCA** commitar arquivos `.env` no Git
- ✅ **SEMPRE** usar `.env.example` como template
- ✅ **PROTEGER** chaves do Supabase
- ✅ **VALIDAR** URLs em produção

### **🔄 Ambiente:**
- ✅ **Desenvolvimento**: `VITE_NODE_ENV=development`
- ✅ **Produção**: `VITE_NODE_ENV=production`
- ✅ **Teste**: `VITE_NODE_ENV=test`

### **📱 Funcionalidades:**
- ✅ **Chat**: Funciona com streaming
- ✅ **Autenticação**: Supabase Auth
- ✅ **Tema**: Claro/escuro/sistema
- ✅ **Cache**: Local e remoto
- ✅ **Performance**: Otimizado

## 🎉 **Conclusão:**

**✅ Todas as variáveis documentadas!**
**✅ Configuração flexível por ambiente!**
**✅ Segurança e performance otimizadas!**
**✅ Fácil de configurar e manter!**

**O frontend está pronto para qualquer ambiente!** 🚀✨ 