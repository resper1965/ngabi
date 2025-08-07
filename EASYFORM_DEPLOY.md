# 🚀 Deploy no EasyPanel - n.Gabi

## 📋 **Pré-requisitos**

### **✅ Repositório GitHub**
- [x] Código commitado no GitHub
- [x] Dockerfiles criados
- [x] Variáveis de ambiente documentadas

### **📁 Estrutura do Repositório**
```
ngabi/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 **Dockerfiles**

### **Backend Dockerfile**
**Localização:** `backend/Dockerfile`
```dockerfile
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Frontend Dockerfile**
**Localização:** `frontend/Dockerfile`
```dockerfile
FROM node:18-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build
RUN npm install -g serve
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
RUN chown -R nextjs:nodejs /app
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1
CMD ["serve", "-s", "dist", "-l", "3000"]
```

## 🌍 **Variáveis de Ambiente**

### **Backend (EasyPanel)**
```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OpenAI
OPENAI_API_KEY=your-openai-key

# Redis (EasyPanel)
REDIS_URL=redis://default:password@redis-host:6379
REDIS_HOST=redis-host
REDIS_PORT=6379
REDIS_PASSWORD=password
REDIS_USERNAME=default

# App Config
APP_NAME=nGabi
APP_VERSION=1.0.0
ENVIRONMENT=homologacao
DEBUG=false
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_CHAT=200
RATE_LIMIT_AUTH=100
RATE_LIMIT_API=500

# CORS
CORS_ORIGINS=https://ngabi.ness.tec.br,http://localhost:3000
```

### **Frontend (EasyPanel)**
```bash
# API Base URL
VITE_API_BASE_URL=https://ngabi.ness.tec.br/backend

# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# OpenAI (para testes diretos)
VITE_OPENAI_API_KEY=your-openai-key

# Environment
NODE_ENV=production
```

## 🚀 **Configuração EasyPanel**

### **1. Criar Projeto**
- **Nome:** `ngabi-homologacao`
- **Domínio:** `ngabi.ness.tec.br`
- **SSL:** Automático

### **2. Configurar Backend**
- **Tipo:** Docker
- **Dockerfile Path:** `backend/Dockerfile`
- **Porta:** 8000
- **Path:** `/backend`
- **Build Command:** `docker build -t ngabi-backend .`
- **Start Command:** `docker run -p 8000:8000 ngabi-backend`

### **3. Configurar Frontend**
- **Tipo:** Docker
- **Dockerfile Path:** `frontend/Dockerfile`
- **Porta:** 3000
- **Path:** `/`
- **Build Command:** `docker build -t ngabi-frontend .`
- **Start Command:** `docker run -p 3000:3000 ngabi-frontend`

### **4. Configurar Redis**
- **Tipo:** Redis
- **Porta:** 6379
- **Credenciais:** Fornecidas pelo EasyPanel

## 📋 **Passos para Deploy**

### **1. Preparar Repositório**
```bash
# Verificar se tudo está commitado
git status
git add .
git commit -m "Preparar para deploy EasyPanel"
git push origin main
```

### **2. Configurar EasyPanel**
1. **Acessar EasyPanel**
2. **Criar novo projeto**
3. **Conectar repositório GitHub**
4. **Configurar variáveis de ambiente**
5. **Configurar Dockerfiles**
6. **Habilitar auto-deploy**

### **3. Deploy Automático**
```bash
# EasyPanel detecta mudanças no GitHub
# Build automático dos containers
# Deploy automático
# Health checks automáticos
```

## 🔍 **Testes Pós-Deploy**

### **1. Health Checks**
```bash
# Backend
curl https://ngabi.ness.tec.br/backend/health

# Frontend
curl https://ngabi.ness.tec.br

# Redis
curl https://ngabi.ness.tec.br/backend/health/redis
```

### **2. Testes de Funcionalidade**
```bash
# Chat API
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como posso ajudar?"}'

# Agentes Especialistas
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/agents/specialists/customer-support/langchain" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test_message": "Tenho um problema técnico"}'

# Estilo de Voz
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/agents/voice-style/initialize" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"organization_name": "Empresa Teste", "tenant_id": "empresa-teste"}'
```

## 📊 **Monitoramento**

### **1. Logs**
- **Backend logs:** EasyPanel Dashboard
- **Frontend logs:** EasyPanel Dashboard
- **Redis logs:** EasyPanel Dashboard

### **2. Métricas**
- **Response time**
- **Error rate**
- **Memory usage**
- **CPU usage**

### **3. Alertas**
- **Health check failures**
- **High error rate**
- **High response time**

## 🎯 **URLs de Homologação**

### **Backend API**
```
https://ngabi.ness.tec.br/backend
```

### **Frontend**
```
https://ngabi.ness.tec.br
```

### **Documentação API**
```
https://ngabi.ness.tec.br/backend/docs
```

### **Health Checks**
```
https://ngabi.ness.tec.br/backend/health
```

## 🚨 **Rollback Plan**

### **1. Backup**
- **Database:** Supabase backup
- **Configurações:** EasyPanel backup
- **Logs:** EasyPanel logs

### **2. Rollback Steps**
1. **Parar aplicações** no EasyPanel
2. **Restaurar versão anterior** do GitHub
3. **Redeploy automático**
4. **Verificar health checks**

## 📋 **Checklist Final**

### **✅ Pré-Deploy**
- [ ] Código commitado no GitHub
- [ ] Dockerfiles criados e testados
- [ ] Variáveis de ambiente documentadas
- [ ] EasyPanel configurado
- [ ] Domínio configurado

### **✅ Deploy**
- [ ] Backend deployado com sucesso
- [ ] Frontend deployado com sucesso
- [ ] Redis conectado e funcionando
- [ ] Health checks passando

### **✅ Pós-Deploy**
- [ ] Testes de funcionalidade
- [ ] Testes de performance
- [ ] Monitoramento ativo
- [ ] Documentação atualizada

## 🎉 **Deploy Pronto!**

**O projeto está 100% pronto para deploy no EasyPanel!** 🚀

### **📁 Localização dos Dockerfiles:**
- **Backend:** `backend/Dockerfile`
- **Frontend:** `frontend/Dockerfile`

### **🌍 Variáveis de Ambiente:**
- **Backend:** Configuradas no EasyPanel
- **Frontend:** Configuradas no EasyPanel

### **🔗 Repositório GitHub:**
- **URL:** `https://github.com/seu-usuario/ngabi`
- **Branch:** `main`
- **Auto-deploy:** Habilitado

**Agora é só configurar no EasyPanel e fazer o deploy!** 🎯 