# 🚀 Deploy Completo n.Gabi - Easypanel

## 📋 **SERVIÇOS NECESSÁRIOS**

### **1. ngabi-postgres (PostgreSQL)**
- **Tipo**: Docker Image
- **Imagem**: `postgres:15-alpine`
- **Porta**: `5432`
- **Variáveis**:
  ```env
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=NgabiDB2024!Secure
  POSTGRES_DB=chat_agents
  ```

### **2. ngabi-redis (Redis)**
- **Tipo**: Docker Image
- **Imagem**: `redis:7-alpine`
- **Porta**: `6379`
- **Variáveis**: Nenhuma

### **3. ngabi-elasticsearch (Elasticsearch)**
- **Tipo**: Docker Image
- **Imagem**: `elasticsearch:7.17.0`
- **Porta**: `9200`
- **Variáveis**:
  ```env
  discovery.type=single-node
  xpack.security.enabled=false
  cluster.name=ngabi-cluster
  ```

### **4. ngabi-backend (FastAPI)**
- **Tipo**: GitHub Source
- **Proprietário**: `resper1965`
- **Repositório**: `ngabi`
- **Branch**: `main`
- **Caminho**: `/backend`
- **Porta**: `8000`
- **Variáveis**:
  ```env
  DATABASE_URL=postgresql://postgres:NgabiDB2024!Secure@ngabi-postgres:5432/chat_agents
  REDIS_URL=redis://ngabi-redis:6379
  ELASTICSEARCH_URL=http://ngabi-elasticsearch:9200
  JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKey123
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br
  ```

### **5. ngabi-frontend (React)**
- **Tipo**: GitHub Source
- **Proprietário**: `resper1965`
- **Repositório**: `ngabi`
- **Branch**: `main`
- **Caminho**: `/frontend`
- **Porta**: `3000`
- **Variáveis**:
  ```env
  VITE_API_URL=https://api.ngabi.ness.tec.br
  ```

### **6. ngabi-n8n (n8n)**
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

### **1. Bancos de Dados (Primeiro)**
```bash
1. ngabi-postgres
2. ngabi-redis  
3. ngabi-elasticsearch
```

### **2. Aplicações (Segundo)**
```bash
4. ngabi-backend
5. ngabi-frontend
6. ngabi-n8n
```

## 🔧 **CONFIGURAÇÃO PASSO A PASSO**

### **Passo 1: Criar Projeto**
1. Acesse Easypanel
2. Clique em "New Project"
3. Nome: `ngabi`

### **Passo 2: Deploy dos Bancos**
1. **ngabi-postgres**:
   - New Service → Docker Image
   - Image: `postgres:15-alpine`
   - Port: `5432`
   - Environment Variables (conforme acima)

2. **ngabi-redis**:
   - New Service → Docker Image
   - Image: `redis:7-alpine`
   - Port: `6379`

3. **ngabi-elasticsearch**:
   - New Service → Docker Image
   - Image: `elasticsearch:7.17.0`
   - Port: `9200`
   - Environment Variables (conforme acima)

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

### **Backend não conecta aos bancos**
1. Verificar se os bancos estão rodando
2. Verificar nomes dos serviços na rede
3. Verificar variáveis de ambiente

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
✅ api.ngabi.ness.tec.br → Backend FastAPI
✅ n8n.ngabi.ness.tec.br → n8n Workflows
```

**Todos os serviços funcionando e conectados!** 🚀 