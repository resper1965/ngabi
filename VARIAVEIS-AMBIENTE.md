# 🔧 Variáveis de Ambiente - n.Gabi

## 📋 Arquivo .env Completo

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```bash
# =============================================================================
# SUPABASE (BaaS - Backend as a Service)
# =============================================================================
SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5NzI5NzQsImV4cCI6MjA1MDU0ODk3NH0.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDk3Mjk3NCwiZXhwIjoyMDUwNTQ4OTc0fQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8

# =============================================================================
# JWT (JSON Web Tokens) - OBRIGATÓRIO
# =============================================================================
JWT_SECRET_KEY=ngabi-super-secret-jwt-key-2024-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# =============================================================================
# REDIS (Cache e Rate Limiting)
# =============================================================================
REDIS_PASSWORD=ngabi-redis-secure-password-2024
REDIS_URL=redis://ngabi-redis:6379

# =============================================================================
# CACHE
# =============================================================================
CACHE_ENABLED=true
CACHE_TTL=3600

# =============================================================================
# RATE LIMITING
# =============================================================================
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# =============================================================================
# AI/CHAT (Opcional - para funcionalidades de IA)
# =============================================================================
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_MODEL=gpt-3.5-turbo
MAX_TOKENS=2048
TEMPERATURE=0.7

# =============================================================================
# SEGURANÇA
# =============================================================================
SECRET_KEY=ngabi-super-secret-key-2024-change-in-production
ENVIRONMENT=development
DEBUG=true

# =============================================================================
# LOGGING
# =============================================================================
LOG_LEVEL=INFO
LOG_FORMAT=json

# =============================================================================
# CORS (Cross-Origin Resource Sharing)
# =============================================================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://ngabi.ness.tec.br

# =============================================================================
# APP INFO
# =============================================================================
APP_NAME=n.Gabi
APP_VERSION=2.0.0
```

## 🚨 Variáveis OBRIGATÓRIAS

### **1. JWT_SECRET_KEY (CRÍTICA)**
```bash
JWT_SECRET_KEY=ngabi-super-secret-jwt-key-2024-change-in-production
```
**Por que é obrigatória**: Sem ela, o backend não inicia
**O que fazer**: Use o valor acima ou gere uma nova chave secreta

### **2. SUPABASE_URL**
```bash
SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co
```
**Por que é obrigatória**: Conecta ao banco de dados Supabase
**O que fazer**: Use o valor fornecido (já configurado)

### **3. SUPABASE_ANON_KEY**
```bash
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
**Por que é obrigatória**: Autenticação com Supabase
**O que fazer**: Use o valor fornecido (já configurado)

## 🔧 Como Criar o Arquivo .env

### **Método 1: Copiar e Colar**
```bash
# No terminal, na pasta do projeto
nano .env
# Cole todo o conteúdo acima
# Salve com Ctrl+X, Y, Enter
```

### **Método 2: Comando Direto**
```bash
# Criar o arquivo .env
cat > .env << 'EOF'
SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5NzI5NzQsImV4cCI6MjA1MDU0ODk3NH0.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDk3Mjk3NCwiZXhwIjoyMDUwNTQ4OTc0fQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8
JWT_SECRET_KEY=ngabi-super-secret-jwt-key-2024-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_PASSWORD=ngabi-redis-secure-password-2024
REDIS_URL=redis://ngabi-redis:6379
CACHE_ENABLED=true
CACHE_TTL=3600
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_MODEL=gpt-3.5-turbo
MAX_TOKENS=2048
TEMPERATURE=0.7
SECRET_KEY=ngabi-super-secret-key-2024-change-in-production
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
LOG_FORMAT=json
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://ngabi.ness.tec.br
APP_NAME=n.Gabi
APP_VERSION=2.0.0
EOF
```

### **Método 3: Arquivo por Arquivo**
```bash
# Criar arquivo vazio
touch .env

# Adicionar variáveis uma por uma
echo "SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co" >> .env
echo "SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5NzI5NzQsImV4cCI6MjA1MDU0ODk3NH0.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8" >> .env
echo "JWT_SECRET_KEY=ngabi-super-secret-jwt-key-2024-change-in-production" >> .env
# ... continuar com as outras variáveis
```

## ✅ Verificação

### **1. Verificar se o arquivo foi criado**
```bash
ls -la .env
```

### **2. Verificar conteúdo**
```bash
cat .env
```

### **3. Testar a aplicação**
```bash
# Iniciar com as variáveis
docker-compose up -d

# Verificar logs
docker logs ngabi-backend
```

## 🚨 Problemas Comuns

### **1. "JWT_SECRET_KEY Field required"**
**Solução**: Adicione a variável `JWT_SECRET_KEY` no arquivo `.env`

### **2. "SUPABASE_ANON_KEY variable is not set"**
**Solução**: Verifique se o arquivo `.env` está na raiz do projeto

### **3. "Permission denied"**
**Solução**: Verifique as permissões do arquivo `.env`

## 🔒 Segurança

### **⚠️ IMPORTANTE**
- **NUNCA** commite o arquivo `.env` no Git
- **SEMPRE** use chaves secretas diferentes em produção
- **MUDE** as chaves padrão antes de usar em produção

### **Para Produção**
```bash
# Gerar chave JWT segura
openssl rand -hex 32

# Gerar chave secreta
openssl rand -hex 64
```

## 📊 Resumo das Variáveis

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `JWT_SECRET_KEY` | ✅ **SIM** | Chave para JWT tokens |
| `SUPABASE_URL` | ✅ **SIM** | URL do projeto Supabase |
| `SUPABASE_ANON_KEY` | ✅ **SIM** | Chave anônima do Supabase |
| `REDIS_PASSWORD` | ❌ Não | Senha do Redis |
| `OPENAI_API_KEY` | ❌ Não | Chave da API OpenAI |
| `CORS_ORIGINS` | ❌ Não | Domínios permitidos |

**Crie o arquivo `.env` com essas variáveis e a aplicação funcionará!** 🚀 