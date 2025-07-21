# 🚀 Deploy n.Gabi com Supabase - Easypanel

## 📋 **SERVIÇOS NECESSÁRIOS (SIMPLIFICADO)**

### **1. ngabi-redis (Redis)**
- **Tipo**: Docker Image
- **Imagem**: `redis:7-alpine`
- **Porta**: `6379`
- **Variáveis**: Nenhuma

### **2. ngabi-backend (FastAPI + Supabase)**
- **Tipo**: GitHub Source
- **Proprietário**: `resper1965`
- **Repositório**: `ngabi`
- **Branch**: `main`
- **Caminho**: `/backend`
- **Porta**: `8000`
- **Variáveis**:
  ```env
  SUPABASE_URL=https://api.ngabi.ness.tec.br
  SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
  REDIS_URL=redis://ngabi-redis:6379
  JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKeyWithAtLeast32CharactersLong
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br
  ```

### **3. ngabi-frontend (React)**
- **Tipo**: GitHub Source
- **Proprietário**: `resper1965`
- **Repositório**: `ngabi`
- **Branch**: `main`
- **Caminho**: `/frontend`
- **Porta**: `3000`
- **Variáveis**:
  ```env
  VITE_API_URL=https://api.ngabi.ness.tec.br
  VITE_SUPABASE_URL=https://api.ngabi.ness.tec.br
  VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
  ```

### **4. ngabi-n8n (n8n)**
- **Tipo**: Docker Image
- **Imagem**: `n8nio/n8n:latest`
- **Porta**: `5678`
- **Variáveis**:
  ```env
  N8N_BASIC_AUTH_ACTIVE=true
  N8N_BASIC_AUTH_USER=admin
  N8N_BASIC_AUTH_PASSWORD=NgabiN8n2024!Admin
  WEBHOOK_URL=https://n8n.ngabi.ness.tec.br
  ```

## 🌐 **DOMÍNIOS CONFIGURADOS**

### **DNS Records (A Records)**
```
ngabi.ness.tec.br → IP_DO_SERVIDOR
api.ngabi.ness.tec.br → IP_DO_SERVIDOR
n8n.ngabi.ness.tec.br → IP_DO_SERVIDOR
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

### **1. Serviços Base (Primeiro)**
```bash
1. ngabi-redis
```

### **2. Aplicações (Segundo)**
```bash
2. ngabi-backend
3. ngabi-frontend
4. ngabi-n8n
```

## 🔧 **CONFIGURAÇÃO PASSO A PASSO**

### **Passo 1: Criar Projeto**
1. Acesse Easypanel
2. Clique em "New Project"
3. Nome: `ngabi`

### **Passo 2: Deploy do Redis**
1. **ngabi-redis**:
   - New Service → Docker Image
   - Image: `redis:7-alpine`
   - Port: `6379`

### **Passo 3: Deploy das Aplicações**
1. **ngabi-backend**:
   - New Service → GitHub Source
   - Owner: `resper1965`
   - Repository: `ngabi`
   - Branch: `main`
   - Build Path: `/backend`
   - Port: `8000`
   - Environment Variables (conforme acima)

2. **ngabi-frontend**:
   - New Service → GitHub Source
   - Owner: `resper1965`
   - Repository: `ngabi`
   - Branch: `main`
   - Build Path: `/frontend`
   - Port: `3000`
   - Environment Variables (conforme acima)

3. **ngabi-n8n**:
   - New Service → Docker Image
   - Image: `n8nio/n8n:latest`
   - Port: `5678`
   - Environment Variables (conforme acima)

### **Passo 4: Configurar Domínios**
Para cada serviço que precisa de domínio:
1. Vá em "Settings" do serviço
2. Adicione as labels Traefik (conforme acima)

## ✅ **VERIFICAÇÃO**

### **Health Checks**
- **Frontend**: https://ngabi.ness.tec.br
- **Backend**: https://api.ngabi.ness.tec.br/health
- **n8n**: https://n8n.ngabi.ness.tec.br

### **Logs Importantes**
```bash
# Backend logs
docker logs ngabi-backend

# Verificar conexões
curl https://api.ngabi.ness.tec.br/health
```

## 🚨 **TROUBLESHOOTING**

### **Backend não conecta ao Supabase**
1. Verificar `SUPABASE_URL` e `SUPABASE_ANON_KEY`
2. Verificar se o Supabase está rodando
3. Verificar logs do backend

### **Frontend não carrega**
1. Verificar `VITE_API_URL`
2. Verificar CORS no backend
3. Verificar domínio configurado

### **n8n não acessa**
1. Verificar credenciais básicas
2. Verificar `WEBHOOK_URL`
3. Verificar domínio configurado

## 🎯 **RESULTADO FINAL**

```
✅ ngabi.ness.tec.br → Frontend React
✅ api.ngabi.ness.tec.br → Backend FastAPI + Supabase
✅ n8n.ngabi.ness.tec.br → n8n Workflows
```

## 🎉 **VANTAGENS DO SUPABASE**

- ✅ **PostgreSQL** + **Auth** + **Real-time** em um só lugar
- ✅ **Dashboard web** para gerenciar dados
- ✅ **API automática** (REST e GraphQL)
- ✅ **Muito mais simples** de configurar
- ✅ **Menos serviços** para gerenciar
- ✅ **Deploy mais rápido**

**Todos os serviços funcionando e conectados!** 🚀 