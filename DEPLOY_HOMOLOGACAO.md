# 🚀 Deploy em Homologação - n.Gabi

## 📋 **Checklist de Preparação**

### **✅ Pré-requisitos Verificados**
- [x] Backend APIs implementadas
- [x] Frontend conectado com backend
- [x] LangChain integrado
- [x] Base vetorial de estilo de voz
- [x] Supabase configurado
- [x] Redis configurado
- [x] OpenAI integrada

### **🔧 Configurações Necessárias**

#### **1. Variáveis de Ambiente - Backend**
```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OpenAI
OPENAI_API_KEY=your-openai-key

# Redis (EasyUIPanel)
REDIS_URL=redis://default:6cebb38271cd2fea746a@ngabi_ngabi-redis:6379
REDIS_HOST=ngabi_ngabi-redis
REDIS_PORT=6379
REDIS_PASSWORD=6cebb38271cd2fea746a
REDIS_USERNAME=default

# App Config
APP_NAME=nGabi
APP_VERSION=1.0.0
ENVIRONMENT=homologacao
DEBUG=false
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_CHAT=100
RATE_LIMIT_AUTH=50
```

#### **2. Variáveis de Ambiente - Frontend**
```bash
# API Base URL
VITE_API_BASE_URL=https://ngabi.ness.tec.br/backend

# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# OpenAI (para testes diretos)
VITE_OPENAI_API_KEY=your-openai-key
```

## 🏗️ **Estrutura de Deploy**

### **Backend (FastAPI)**
```
Porta: 8000
Health Check: /health
Documentação: /docs
URL: https://ngabi.ness.tec.br/backend
```

### **Frontend (React)**
```
Porta: 3000
Build: npm run build
Serve: nginx
URL: https://ngabi.ness.tec.br
```

### **Redis (Cache)**
```
Porta: 6379
Host: ngabi_ngabi-redis
```

## 🚀 **Passos para Deploy**

### **1. Preparar EasyUIPanel**

#### **Configurar Projeto**
```bash
# 1. Acessar EasyUIPanel
# 2. Criar novo projeto: "ngabi-homologacao"
# 3. Configurar domínio: ngabi.ness.tec.br
# 4. Habilitar SSL automático
```

#### **Configurar Backend**
```bash
# 1. Criar aplicação: "backend"
# 2. Tipo: Python
# 3. Porta: 8000
# 4. Build Command: pip install -r requirements.txt
# 5. Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
# 6. Path: /backend
```

#### **Configurar Frontend**
```bash
# 1. Criar aplicação: "frontend"
# 2. Tipo: Node.js
# 3. Porta: 3000
# 4. Build Command: npm install && npm run build
# 5. Start Command: npm run preview
# 6. Path: /
```

#### **Configurar Redis**
```bash
# 1. Criar banco: "redis"
# 2. Tipo: Redis
# 3. Porta: 6379
# 4. Credenciais fornecidas pelo EasyUIPanel
```

### **2. Configurar Variáveis de Ambiente**

#### **Backend - EasyUIPanel**
```bash
# Copiar todas as variáveis de ambiente do backend
# Configurar no painel do EasyUIPanel
```

#### **Frontend - EasyUIPanel**
```bash
# Copiar todas as variáveis de ambiente do frontend
# Configurar no painel do EasyUIPanel
```

### **3. Deploy Automático**

#### **Backend**
```bash
# 1. Conectar repositório GitHub
# 2. Branch: main
# 3. Auto-deploy habilitado
# 4. Build automático
# 5. Path: /backend
```

#### **Frontend**
```bash
# 1. Conectar repositório GitHub
# 2. Branch: main
# 3. Auto-deploy habilitado
# 4. Build automático
# 5. Path: /
```

## 🔍 **Testes de Homologação**

### **1. Health Checks**
```bash
# Backend Health
curl https://ngabi.ness.tec.br/backend/health

# Frontend Health
curl https://ngabi.ness.tec.br

# Redis Health
curl https://ngabi.ness.tec.br/backend/health/redis
```

### **2. Testes de Funcionalidade**

#### **Autenticação**
```bash
# Testar login
curl -X POST "https://ngabi.ness.tec.br/backend/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'
```

#### **Chat API**
```bash
# Testar chat básico
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como posso ajudar?"}'
```

#### **Agentes Especialistas**
```bash
# Testar agente especialista
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/agents/specialists/customer-support/langchain" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test_message": "Tenho um problema técnico"}'
```

#### **Estilo de Voz**
```bash
# Inicializar base de estilo
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/agents/voice-style/initialize" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"organization_name": "Empresa Teste", "tenant_id": "empresa-teste"}'

# Testar estilo de voz
curl -X POST "https://ngabi.ness.tec.br/backend/api/v1/agents/voice-style/test" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test_message": "Olá!", "organization_name": "Empresa Teste", "tenant_id": "empresa-teste"}'
```

### **3. Testes de Frontend**

#### **Acessar Interface**
```bash
# URL: https://ngabi.ness.tec.br
# Verificar:
# - Login funcionando
# - Chat interface carregando
# - Agentes especialistas disponíveis
# - Estilo de voz aplicado
```

## 📊 **Monitoramento**

### **1. Logs**
```bash
# Backend logs
# Acessar logs no EasyUIPanel

# Frontend logs
# Acessar logs no EasyUIPanel

# Redis logs
# Acessar logs no EasyUIPanel
```

### **2. Métricas**
```bash
# Health checks automáticos
# Response time
# Error rate
# Memory usage
# CPU usage
```

### **3. Alertas**
```bash
# Configurar alertas para:
# - Health check failures
# - High error rate
# - High response time
# - Memory/CPU usage
```

## 🔧 **Configurações Específicas**

### **1. CORS (Backend)**
```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ngabi.ness.tec.br"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **2. Rate Limiting**
```python
# Configurar rate limiting para homologação
RATE_LIMIT_CHAT=200  # Mais permissivo para testes
RATE_LIMIT_AUTH=100
```

### **3. Logging**
```python
# Configurar logging para homologação
LOG_LEVEL=DEBUG  # Mais detalhado para debug
```

## 🚨 **Rollback Plan**

### **1. Backup**
```bash
# Backup do banco Supabase
# Backup das configurações
# Backup dos logs
```

### **2. Rollback Steps**
```bash
# 1. Parar aplicações
# 2. Restaurar versão anterior
# 3. Verificar health checks
# 4. Testar funcionalidades críticas
```

## 📋 **Checklist de Lançamento**

### **MVP (1 mês)**
- [ ] Chat funcional com OpenAI
- [ ] Sistema de autenticação
- [ ] Multi-tenancy básico
- [ ] Interface responsiva
- [ ] Deploy em produção
- [ ] Monitoramento básico

### **Beta (2 meses)**
- [ ] Sistema de agentes
- [ ] Analytics básico
- [ ] Testes automatizados
- [ ] Documentação completa
- [ ] Suporte ao cliente
- [ ] Feedback loop

### **GA (3 meses)**
- [ ] Funcionalidades avançadas
- [ ] Sistema de pagamentos
- [ ] Marketing automation
- [ ] Parcerias estratégicas
- [ ] Expansão de mercado
- [ ] Otimização contínua

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

## 🚀 **Próximos Passos**

1. **Configurar EasyUIPanel** com as configurações acima
2. **Deploy automático** conectando o repositório
3. **Testes completos** de todas as funcionalidades
4. **Monitoramento** ativo durante homologação
5. **Feedback** e ajustes baseados nos testes

**O deploy está pronto para ser executado!** 🎉 