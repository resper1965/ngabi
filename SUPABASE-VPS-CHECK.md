# 🔍 Verificação do Supabase na VPS (Easypanel)

## 📋 **O que verificar na VPS:**

### **1. Status do Supabase no Easypanel**
- ✅ **Serviço**: `supabase` ou `ngabi-supabase`
- ✅ **Status**: Rodando (verde)
- ✅ **Porta**: 8000 (Kong HTTP)
- ✅ **Porta**: 8443 (Kong HTTPS)

### **2. IP da VPS e Domínios**
- **IP da VPS**: `SEU_IP_DA_VPS`
- **Domínio**: `ngabi.ness.tec.br`
- **API**: `api.ngabi.ness.tec.br`

### **3. URLs de Acesso ao Supabase**
```
Dashboard: http://SEU_IP_DA_VPS:8000
API: http://SEU_IP_DA_VPS:8000/rest/v1/
Auth: http://SEU_IP_DA_VPS:8000/auth/v1/
```

### **4. Testes de Conexão**

#### **Teste 1: Health Check (via VPS)**
```bash
# Na VPS
curl http://localhost:8000/rest/v1/
```

#### **Teste 2: Auth Status (via VPS)**
```bash
# Na VPS
curl http://localhost:8000/auth/v1/health
```

#### **Teste 3: Dashboard (via navegador)**
```
http://SEU_IP_DA_VPS:8000
```

## 🔧 **Configuração do Backend n.Gabi**

### **Variáveis para ngabi-backend (Easypanel):**
```env
SUPABASE_URL=http://supabase:8000
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
REDIS_URL=redis://ngabi-redis:6379
JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKeyWithAtLeast32CharactersLong
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br
```

### **Variáveis para ngabi-frontend (Easypanel):**
```env
VITE_API_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
```

## 🌐 **Configuração de Domínios**

### **DNS Records (A Records)**
```
ngabi.ness.tec.br → SEU_IP_DA_VPS
api.ngabi.ness.tec.br → SEU_IP_DA_VPS
n8n.ngabi.ness.tec.br → SEU_IP_DA_VPS
```

### **Traefik Labels (Easypanel)**
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

## 📦 **Ordem de Deploy na VPS**

### **1. Supabase (já instalado)**
- ✅ Verificar se está rodando
- ✅ Verificar variáveis de ambiente

### **2. Serviços n.Gabi**
```bash
1. ngabi-redis (Redis)
2. ngabi-backend (FastAPI + Supabase)
3. ngabi-frontend (React)
4. ngabi-n8n (n8n)
```

## 🚨 **Problemas Comuns na VPS**

### **1. Supabase não responde**
```bash
# Na VPS, verificar logs
docker logs supabase-container-name

# Verificar se está rodando
docker ps | grep supabase
```

### **2. Backend não conecta ao Supabase**
- Verificar se `SUPABASE_URL=http://supabase:8000` (nome do serviço)
- Verificar se ambos estão na mesma rede Docker
- Verificar logs do backend

### **3. Domínios não funcionam**
- Verificar DNS A Records
- Verificar Traefik labels
- Verificar certificados SSL

## ✅ **Checklist de Verificação na VPS**

- [ ] Supabase rodando no Easypanel
- [ ] IP da VPS configurado no DNS
- [ ] Domínios apontando para VPS
- [ ] Traefik labels configurados
- [ ] Variáveis de ambiente corretas
- [ ] Rede Docker compartilhada
- [ ] Teste de conexão funcionando

## 🎯 **Próximos Passos**

1. **Verificar IP da VPS** e configurar DNS
2. **Configurar variáveis** do backend com `SUPABASE_URL=http://supabase:8000`
3. **Deploy dos serviços** n.Gabi no Easypanel
4. **Testar conexões** entre serviços
5. **Configurar domínios** e SSL

## 🔍 **Comandos Úteis na VPS**

```bash
# Verificar containers rodando
docker ps

# Verificar logs do Supabase
docker logs supabase-container-name

# Testar conexão interna
curl http://supabase:8000/rest/v1/

# Verificar rede Docker
docker network ls
docker network inspect easypanel_default
``` 