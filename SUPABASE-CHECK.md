# 🔍 Verificação do Supabase no Easypanel

## 📋 **O que verificar no Easypanel:**

### **1. Serviço Supabase**
- ✅ **Status**: Rodando (verde)
- ✅ **Porta**: 8000 (Kong HTTP)
- ✅ **Porta**: 8443 (Kong HTTPS)

### **2. Variáveis de Ambiente do Supabase**
Verificar se estas variáveis estão configuradas:

```env
# Secrets
POSTGRES_PASSWORD=NgabiSupabase2024!SecurePassword123
JWT_SECRET=NgabiJWT2024!SuperSecretKeyWithAtLeast32CharactersLong
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q

# URLs
SITE_URL=https://ngabi.ness.tec.br
API_EXTERNAL_URL=https://api.ngabi.ness.tec.br
SUPABASE_PUBLIC_URL=https://api.ngabi.ness.tec.br
```

### **3. URLs de Acesso**
- **Dashboard**: https://api.ngabi.ness.tec.br
- **API**: https://api.ngabi.ness.tec.br/rest/v1/
- **Auth**: https://api.ngabi.ness.tec.br/auth/v1/

### **4. Teste de Conexão**

#### **Teste 1: Health Check**
```bash
curl https://api.ngabi.ness.tec.br/rest/v1/
```

#### **Teste 2: Auth Status**
```bash
curl https://api.ngabi.ness.tec.br/auth/v1/health
```

#### **Teste 3: Dashboard**
Acesse: https://api.ngabi.ness.tec.br

## 🔧 **Configuração do Backend n.Gabi**

### **Variáveis para ngabi-backend:**
```env
SUPABASE_URL=https://api.ngabi.ness.tec.br
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
REDIS_URL=redis://ngabi-redis:6379
JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKeyWithAtLeast32CharactersLong
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br
```

## 🚨 **Problemas Comuns**

### **1. Supabase não responde**
- Verificar se o serviço está rodando no Easypanel
- Verificar logs do container Supabase
- Verificar se as portas estão corretas

### **2. Erro de autenticação**
- Verificar se `ANON_KEY` está correto
- Verificar se `SERVICE_ROLE_KEY` está correto
- Verificar se as URLs estão corretas

### **3. Backend não conecta**
- Verificar se `SUPABASE_URL` aponta para o serviço correto
- Verificar se `SUPABASE_ANON_KEY` está correto
- Verificar logs do backend

## ✅ **Checklist de Verificação**

- [ ] Supabase rodando no Easypanel
- [ ] URLs configuradas corretamente
- [ ] Chaves de autenticação configuradas
- [ ] Backend com variáveis corretas
- [ ] Teste de conexão funcionando
- [ ] Dashboard acessível
- [ ] API respondendo

## 🎯 **Próximos Passos**

1. **Verificar status** do Supabase no Easypanel
2. **Configurar variáveis** do backend
3. **Testar conexão** entre serviços
4. **Deploy do backend** com Supabase 