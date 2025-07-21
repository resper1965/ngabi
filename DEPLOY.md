# 🚀 Guia de Deploy - n.Gabi no Easypanel

## 📋 Configurações dos Serviços

### **1. ngabi-frontend**

**Configuração de Fonte:**
- **Tipo**: GitHub
- **Proprietário**: `resper1965`
- **Repositório**: `ngabi`
- **Branch**: `main`
- **Caminho**: `/frontend`

**Configuração de Build:**
- **Tipo de Construção**: Dockerfile
- **Arquivo**: `Dockerfile`
- **Caminho de Build**: `/frontend`

**Variáveis de Ambiente:**
```env
VITE_API_BASE_URL=https://api.ngabi.ness.tec.br
VITE_N8N_URL=https://n8n.ngabi.ness.tec.br
VITE_CHATWOOT_URL=https://chatwoot.ngabi.ness.tec.br
```

**Configuração de Domínio:**
- **Host**: `ngabi.ness.tec.br`
- **Porta**: `3000`
- **Protocolo**: `HTTP`
- **HTTPS**: Habilitado

---

### **2. ngabi-backend (COM CHATWOOT INTEGRADO)**

**Configuração de Fonte:**
- **Tipo**: GitHub
- **Proprietário**: `resper1965`
- **Repositório**: `ngabi`
- **Branch**: `main`
- **Caminho**: `/backend`

**Configuração de Build:**
- **Tipo de Construção**: Dockerfile
- **Arquivo**: `Dockerfile`
- **Caminho de Build**: `/backend`

**Variáveis de Ambiente:**
```env
DATABASE_URL=postgresql://postgres:NgabiDB2024!Secure@localhost:5432/chat_agents
POSTGRES_USER=postgres
POSTGRES_PASSWORD=NgabiDB2024!Secure
POSTGRES_DB=chat_agents
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=NgabiN8n2024!Admin
WEBHOOK_URL=https://n8n.ngabi.ness.tec.br
JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKey123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br
```

**Configuração de Domínio:**
- **API Host**: `api.ngabi.ness.tec.br`
- **API Porta**: `8000`
- **Chatwoot Host**: `chatwoot.ngabi.ness.tec.br`
- **Chatwoot Porta**: `3000`
- **Protocolo**: `HTTP`
- **HTTPS**: Habilitado

---

### **3. ngabi-n8n**

**Configuração de Fonte:**
- **Tipo**: Image
- **Image**: `n8nio/n8n:latest`

**Variáveis de Ambiente:**
```env
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=NgabiN8n2024!Admin
WEBHOOK_URL=https://n8n.ngabi.ness.tec.br
```

**Configuração de Domínio:**
- **Host**: `n8n.ngabi.ness.tec.br`
- **Porta**: `5678`
- **Protocolo**: `HTTP`
- **HTTPS**: Habilitado

---

## 🌐 Configuração de DNS

### **Entradas A necessárias:**
```
ngabi.ness.tec.br          → 62.72.8.164
api.ngabi.ness.tec.br      → 62.72.8.164
chatwoot.ngabi.ness.tec.br → 62.72.8.164
n8n.ngabi.ness.tec.br      → 62.72.8.164
```

---

## 🔧 Serviços Integrados

### **ngabi-backend inclui:**
- ✅ **FastAPI** (porta 8000)
- ✅ **Chatwoot** (porta 3000)
- ✅ **PostgreSQL** (porta 5432)
- ✅ **Redis** (porta 6379)
- ✅ **Elasticsearch** (porta 9200)
- ✅ **Sidekiq** (workers do Chatwoot)

### **Acessos:**
- **Frontend**: https://ngabi.ness.tec.br
- **API**: https://api.ngabi.ness.tec.br
- **Chatwoot**: https://chatwoot.ngabi.ness.tec.br
- **n8n**: https://n8n.ngabi.ness.tec.br

---

## 📊 Recursos Utilizados

### **Total de Serviços no Easypanel: 3**
1. **ngabi-frontend** - Interface do usuário
2. **ngabi-backend** - Backend + Chatwoot + Bancos integrados
3. **ngabi-n8n** - Automação de workflows

### **Economia:**
- **Antes**: 8+ serviços separados
- **Agora**: 3 serviços integrados
- **Redução**: ~60% menos complexidade

---

## 🚀 Ordem de Deploy

1. **ngabi-backend** (primeiro - contém os bancos)
2. **ngabi-n8n** (segundo - depende do backend)
3. **ngabi-frontend** (terceiro - depende da API)

---

## ✅ Checklist de Deploy

- [ ] Configurar DNS (4 entradas A)
- [ ] Deploy ngabi-backend
- [ ] Verificar logs do backend
- [ ] Deploy ngabi-n8n
- [ ] Deploy ngabi-frontend
- [ ] Testar acesso aos serviços
- [ ] Configurar HTTPS (automático via Traefik)
- [ ] Testar integração entre serviços 