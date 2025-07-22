# 🚀 n.Gabi - Deploy EasyPanel

## 📋 Visão Geral

O **n.Gabi** é uma plataforma SaaS de chat multi-agente que agora está otimizada para deploy no **EasyPanel**, aproveitando todas as funcionalidades da plataforma: deploy automatizado, SSL automático, backups e monitoramento.

## ✨ Funcionalidades

### 🎯 **Core Features**
- ✅ **Chat Multi-Agente** com IA
- ✅ **Sistema de Eventos Híbrido** (tempo real + persistência)
- ✅ **Webhooks** para integrações externas
- ✅ **Multi-tenancy** com isolamento completo
- ✅ **Rate Limiting** inteligente
- ✅ **Cache Redis** distribuído

### 🚀 **EasyPanel Features**
- ✅ **Deploy Automatizado** com zero-downtime
- ✅ **SSL Automático** com Let's Encrypt
- ✅ **Backup Automático** do banco de dados
- ✅ **Monitoramento** completo com logs
- ✅ **Escalabilidade** horizontal
- ✅ **Terminal Integrado** para debugging

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Redis         │
│   (React)       │    │   (FastAPI)     │    │   (Cache)       │
│   Porta 3000    │    │   Porta 8000    │    │   Porta 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Traefik       │
                    │   (Reverse      │
                    │   Proxy + SSL)  │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Supabase      │
                    │   (Database)    │
                    └─────────────────┘
```

## 🚀 Deploy Rápido

### 1. **Pré-requisitos**
- ✅ EasyPanel instalado e configurado
- ✅ Domínio configurado (ex: `ngabi.ness.tec.br`)
- ✅ Repositório GitHub com o código

### 2. **Configuração no EasyPanel**

#### A. Criar Projeto
1. Acesse o painel do EasyPanel
2. Clique em "New Project"
3. Nome: `ngabi`
4. Description: `Plataforma de Chat Multi-Agente`

#### B. Conectar GitHub
1. Selecione "GitHub" como fonte
2. Conecte sua conta GitHub
3. Selecione o repositório `ngabi`
4. Branch: `main`

#### C. Configurar Build
1. **Build Type**: `Docker Compose`
2. **Compose File**: `easypanel-config.yml`
3. **Environment File**: `easypanel.env`

#### D. Configurar Domínios
1. **Frontend**: `ngabi.ness.tec.br`
2. **Backend API**: `api.ngabi.ness.tec.br`
3. **Traefik Dashboard**: `traefik.ngabi.ness.tec.br`

#### E. Configurar SSL
1. ✅ **Enable SSL**: Ativado
2. **Provider**: Let's Encrypt
3. **Email**: `admin@ngabi.ness.tec.br`

### 3. **Variáveis de Ambiente**

Configure no painel do EasyPanel:

```bash
# Supabase (OBRIGATÓRIO)
SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# JWT (OBRIGATÓRIO)
JWT_SECRET_KEY=RGaK+1r6ckX1VqR27JGvEIgPOuOFmKulWYH6noPOG...

# Domínios
DOMAIN=ngabi.ness.tec.br
API_DOMAIN=api.ngabi.ness.tec.br
ADMIN_EMAIL=admin@ngabi.ness.tec.br

# Redis
REDIS_URL=redis://ngabi-redis:6379

# PostgreSQL (opcional)
POSTGRES_PASSWORD=ngabi_secure_password_2024
```

### 4. **Deploy**

1. Clique em "Deploy"
2. EasyPanel irá:
   - Clonar o repositório
   - Construir as imagens Docker
   - Configurar os serviços
   - Configurar SSL automaticamente
   - Fazer health checks

## 🔧 Configurações Avançadas

### 1. **Backup Automático**

```bash
# Configurar no EasyPanel
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
BACKUP_SCHEDULE=0 2 * * *  # Diariamente às 2h
```

### 2. **Monitoramento**

#### Logs em Tempo Real
- Acesse o painel do EasyPanel
- Vá em "Logs" para cada serviço
- Configure alertas por email

#### Métricas
```bash
# Métricas do Backend
curl https://api.ngabi.ness.tec.br/metrics

# Health Check
curl https://api.ngabi.ness.tec.br/health
```

### 3. **Escalabilidade**

```yaml
# No easypanel-config.yml
services:
  backend:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

## 📡 APIs Disponíveis

### **Eventos** (`/api/v1/events`)
- `GET /history` - Histórico de eventos
- `GET /stats` - Estatísticas
- `POST /reprocess` - Reprocessar eventos falhados
- `GET /types` - Tipos de eventos
- `POST /test` - Testar sistema

### **Webhooks** (`/api/v1/webhooks`)
- `POST /register` - Registrar webhook
- `DELETE /unregister/{id}` - Remover webhook
- `GET /list` - Listar webhooks
- `POST /test` - Testar webhook
- `GET /events` - Eventos disponíveis

### **Chat** (`/api/v1/chat`)
- `POST /` - Enviar mensagem
- `POST /stream` - Chat em streaming
- `POST /batch` - Múltiplas mensagens
- `GET /history` - Histórico de chat

## 🛡️ Segurança

### **SSL/TLS**
- ✅ Certificados Let's Encrypt automáticos
- ✅ Renovação automática
- ✅ HTTP/2 habilitado
- ✅ HSTS headers

### **Rate Limiting**
```python
# Configurado no backend
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### **Row Level Security (RLS)**
- Eventos só são visíveis para o tenant correspondente
- Webhooks só são acessíveis pelo tenant proprietário
- Autenticação obrigatória para todas as operações

## 📊 Monitoramento

### **Logs Estruturados**
```json
{
  "timestamp": "2024-07-22T12:00:00Z",
  "level": "INFO",
  "service": "backend",
  "message": "Evento emitido: chat_message",
  "tenant_id": "uuid",
  "user_id": "uuid"
}
```

### **Métricas Prometheus**
```bash
# Endpoint de métricas
curl https://api.ngabi.ness.tec.br/metrics

# Métricas disponíveis
- http_requests_total
- http_request_duration_seconds
- redis_operations_total
- event_emissions_total
```

## 🚨 Troubleshooting

### **Problemas Comuns**

#### A. Build Falha
```bash
# Verificar logs
docker-compose logs backend
docker-compose logs frontend

# Verificar dependências
docker-compose build --no-cache
```

#### B. SSL Não Funciona
```bash
# Verificar DNS
dig ngabi.ness.tec.br
dig api.ngabi.ness.tec.br

# Verificar Traefik
docker-compose logs traefik
```

#### C. Banco Não Conecta
```bash
# Verificar Supabase
curl -f https://tegbkyeqfrqkuxeilgpc.supabase.co/rest/v1/

# Verificar variáveis
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY
```

### **Comandos Úteis**

```bash
# Status dos serviços
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Health checks
curl -f https://api.ngabi.ness.tec.br/health

# Deploy manual
./scripts/deploy.sh

# Backup manual
./scripts/backup.sh
```

## 📈 Performance

### **Otimizações**

#### Redis
```bash
REDIS_MAX_MEMORY=256mb
REDIS_MAX_MEMORY_POLICY=allkeys-lru
```

#### Backend
```bash
WORKER_PROCESSES=4
CACHE_TTL=3600
```

#### Frontend
```bash
NODE_ENV=production
VITE_API_BASE_URL=https://api.ngabi.ness.tec.br
```

### **Benchmarks**
```bash
# Teste de carga
ab -n 1000 -c 10 https://api.ngabi.ness.tec.br/health

# Teste de latência
curl -w "@curl-format.txt" -o /dev/null -s https://api.ngabi.ness.tec.br/health
```

## 🎯 Próximos Passos

### **Melhorias Futuras**
- [ ] **CDN**: Cloudflare para assets estáticos
- [ ] **Load Balancer**: Múltiplas instâncias
- [ ] **Database**: Migração para PostgreSQL local
- [ ] **Monitoring**: Grafana + Prometheus
- [ ] **Backup**: S3 para backups remotos

### **Integrações**
- [ ] **Slack**: Notificações de deploy
- [ ] **Email**: Alertas de monitoramento
- [ ] **Analytics**: Google Analytics
- [ ] **Error Tracking**: Sentry

## 📚 Documentação

### **Arquivos Importantes**
- 📄 **`EASYPANEL-DEPLOY.md`** - Guia completo de deploy
- 📄 **`SISTEMA-EVENTOS-WEBHOOKS.md`** - Sistema de eventos
- 📄 **`easypanel-config.yml`** - Configuração Docker Compose
- 📄 **`easypanel.env`** - Variáveis de ambiente
- 📄 **`scripts/deploy.sh`** - Script de deploy
- 📄 **`scripts/backup.sh`** - Script de backup

### **URLs de Acesso**
- 🌐 **Frontend**: https://ngabi.ness.tec.br
- 🔧 **Backend API**: https://api.ngabi.ness.tec.br
- 📊 **Traefik Dashboard**: https://traefik.ngabi.ness.tec.br
- 📚 **API Docs**: https://api.ngabi.ness.tec.br/docs

## 🤝 Suporte

### **Comunidade**
- 📧 **Email**: admin@ngabi.ness.tec.br
- 🐛 **Issues**: GitHub Issues
- 📖 **Documentação**: README.md

### **Recursos**
- 🔗 **EasyPanel**: https://easypanel.io
- 🔗 **Supabase**: https://supabase.com
- 🔗 **Traefik**: https://traefik.io

---

## 🎉 **Deploy Concluído!**

O n.Gabi está agora rodando em produção no EasyPanel com:
- ✅ **Deploy automatizado** com zero-downtime
- ✅ **SSL automático** com Let's Encrypt
- ✅ **Backup automático** do banco de dados
- ✅ **Monitoramento completo** com logs e métricas
- ✅ **Sistema de eventos** e webhooks funcionando
- ✅ **Escalabilidade** preparada para crescimento

**🚀 Pronto para produção!** 