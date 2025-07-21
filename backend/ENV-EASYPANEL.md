# 🔧 Variáveis de Ambiente para Easypanel

## 📋 **Configuração do Backend n.Gabi com Supabase**

### **🔑 Variáveis OBRIGATÓRIAS:**

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# Redis Configuration (opcional, para cache)
REDIS_URL=redis://ngabi-redis:6379

# CORS Configuration
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br

# Application Configuration
APP_NAME=n.Gabi Backend
APP_VERSION=2.0.0
```

### **🔑 Variáveis OPCIONAIS:**

```env
# Logging
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Metrics
ENABLE_METRICS=true
```

## 🎯 **Como Configurar no Easypanel:**

### **1. Acessar o Projeto**
1. Vá para o Easypanel Dashboard
2. Acesse o projeto `ngabi`
3. Vá para o serviço `ngabi-backend`

### **2. Configurar Variáveis**
1. Clique em **"Environment Variables"**
2. Adicione cada variável:

| **Variável** | **Valor** | **Descrição** |
|--------------|-----------|---------------|
| `SUPABASE_URL` | `https://your-project.supabase.co` | URL do seu projeto Supabase |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Chave anônima do Supabase |
| `REDIS_URL` | `redis://ngabi-redis:6379` | URL do Redis (se usar) |
| `CORS_ORIGINS` | `https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br` | Domínios permitidos |
| `APP_NAME` | `n.Gabi Backend` | Nome da aplicação |
| `APP_VERSION` | `2.0.0` | Versão da aplicação |

### **3. Obter Credenciais do Supabase**

#### **A. Acessar Supabase Dashboard**
1. Vá para [supabase.com](https://supabase.com)
2. Faça login na sua conta
3. Acesse o projeto `ngabi`

#### **B. Obter URL e Chave**
1. Vá para **Settings** → **API**
2. Copie:
   - **Project URL**: `https://your-project.supabase.co`
   - **anon public**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### **4. Configurar Domínio**
- **Host**: `api.ngabi.ness.tec.br`
- **Porta**: `8000`
- **Protocolo**: `HTTP`
- **HTTPS**: Habilitado

## ✅ **Checklist de Deploy:**

- [ ] Variáveis de ambiente configuradas
- [ ] Supabase URL e chave anônima definidas
- [ ] CORS configurado para o domínio correto
- [ ] Redis configurado (se usar cache)
- [ ] Domínio configurado no Easypanel
- [ ] Deploy iniciado

## 🧪 **Testar após Deploy:**

### **1. Health Check**
```bash
curl https://api.ngabi.ness.tec.br/health
```

### **2. Testar Autenticação**
```bash
# Testar endpoint de autenticação
curl https://api.ngabi.ness.tec.br/api/v1/auth/check
```

### **3. Verificar Logs**
- Acesse os logs do container no Easypanel
- Verifique se há erros de conexão com Supabase

## 🚨 **Problemas Comuns:**

### **Erro: "Supabase não configurado"**
- Verificar se `SUPABASE_URL` e `SUPABASE_ANON_KEY` estão corretos
- Verificar se as credenciais do Supabase são válidas

### **Erro: "CORS"**
- Verificar se `CORS_ORIGINS` inclui o domínio correto
- Verificar se o frontend está acessando a URL correta

### **Erro: "Redis não disponível"**
- Verificar se o serviço Redis está rodando
- Verificar se `REDIS_URL` está correto

## 🎉 **Sucesso!**

Após configurar todas as variáveis e fazer o deploy, o n.Gabi estará rodando com:
- ✅ **Supabase** como banco de dados
- ✅ **Supabase Auth** para autenticação
- ✅ **API REST** automática
- ✅ **Real-time** habilitado
- ✅ **Segurança** com RLS

**Agora é só fazer o deploy no Easypanel!** 🚀 