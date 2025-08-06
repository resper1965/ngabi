# 🐳 Dockerfiles e Deploy - n.Gabi

## 📁 **Caminhos dos Dockerfiles**

### **Frontend Dockerfiles:**
```
✅ frontend/Dockerfile
✅ frontend/Dockerfile.prod
```

### **Backend Dockerfiles:**
```
✅ backend/Dockerfile
✅ backend/Dockerfile.prod
```

## 🔧 **Configuração dos Dockerfiles**

### **Frontend - Dockerfile Principal:**
```dockerfile
# Localização: frontend/Dockerfile
FROM node:22-alpine
WORKDIR /app
# Configuração para desenvolvimento e produção
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000", "--mode", "production"]
```

### **Frontend - Dockerfile Produção:**
```dockerfile
# Localização: frontend/Dockerfile.prod
# Versão otimizada para produção
```

### **Backend - Dockerfile Principal:**
```dockerfile
# Localização: backend/Dockerfile
FROM alpine:3.22
# Python 3.13 + dependências
# Inclui OpenAI e outras dependências
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

### **Backend - Dockerfile Produção:**
```dockerfile
# Localização: backend/Dockerfile.prod
# Versão otimizada para produção
```

## 🚀 **Comandos de Deploy**

### **1. Build das Imagens:**
```bash
# Frontend
docker build -t resper1965/ngabi-frontend:latest ./frontend
docker build -t resper1965/ngabi-frontend:latest ./frontend -f ./frontend/Dockerfile.prod

# Backend
docker build -t resper1965/ngabi-backend:latest ./backend
docker build -t resper1965/ngabi-backend:latest ./backend -f ./backend/Dockerfile.prod
```

### **2. Push para Docker Hub:**
```bash
# Login no Docker Hub
docker login

# Push das imagens
docker push resper1965/ngabi-frontend:latest
docker push resper1965/ngabi-backend:latest
```

### **3. Deploy Local:**
```bash
# Usar docker-compose.production.yml
docker compose -f docker-compose.production.yml up -d --build
```

### **4. Deploy EasyUIPanel:**
```bash
# Usar easypanel-production.yml
docker compose -f easypanel-production.yml up -d
```

## 📋 **Configuração de Produção**

### **Variáveis de Ambiente Necessárias:**
```bash
# Supabase
SUPABASE_URL=sua_url_do_supabase
SUPABASE_ANON_KEY=sua_chave_anonima
SUPABASE_SERVICE_ROLE_KEY=sua_chave_service_role

# OpenAI
OPENAI_API_KEY=sua_chave_openai

# Redis
REDIS_URL=redis://ngabi-redis:6379

# App
APP_NAME=n.Gabi
APP_VERSION=3.0.0
ENVIRONMENT=production
DEBUG=false
```

### **Portas Utilizadas:**
- **Frontend**: 3000
- **Backend**: 8000
- **Redis**: 6379
- **Nginx**: 80, 443

## 🌐 **URLs de Produção**

### **EasyUIPanel:**
- **Frontend**: https://ngabi.ness.tec.br
- **Backend**: https://api.ngabi.ness.tec.br
- **Health Check**: https://api.ngabi.ness.tec.br/health

### **Local/Docker:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## 🔍 **Verificação do Deploy**

### **1. Health Checks:**
```bash
# Frontend
curl -f http://localhost:3000

# Backend
curl -f http://localhost:8000/health

# Redis
docker exec ngabi-redis redis-cli ping
```

### **2. Logs:**
```bash
# Ver logs dos containers
docker logs ngabi-frontend
docker logs ngabi-backend
docker logs ngabi-redis
```

### **3. Status dos Containers:**
```bash
docker ps
docker compose ps
```

## 🛠️ **Troubleshooting**

### **Problema: Docker Build Fails**
```bash
# Limpar cache do Docker
docker system prune -f
docker builder prune -f

# Rebuild sem cache
docker build --no-cache -t ngabi-frontend:latest ./frontend
```

### **Problema: Container não inicia**
```bash
# Verificar logs
docker logs <container_name>

# Verificar variáveis de ambiente
docker exec <container_name> env
```

### **Problema: Dependência OpenAI**
```bash
# Verificar se a dependência está instalada
docker exec ngabi-backend pip list | grep openai
```

## 📊 **Status Atual**

### **✅ Implementado:**
- ✅ Dockerfiles configurados
- ✅ Tema OKLCH aplicado
- ✅ Backend APIs implementadas
- ✅ Frontend funcionando
- ✅ Redis configurado

### **⚠️ Pendente:**
- ⚠️ Build das imagens Docker
- ⚠️ Push para Docker Hub
- ⚠️ Deploy em produção
- ⚠️ Configuração SSL

## 🎯 **Próximos Passos**

1. **Resolver problema do Docker** (contexts/meta)
2. **Build das imagens** com dependências atualizadas
3. **Push para Docker Hub**
4. **Deploy no EasyUIPanel**
5. **Configurar domínio e SSL**

**O n.Gabi está pronto para deploy!** 🚀 