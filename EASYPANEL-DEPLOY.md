# 🚀 Deploy do n.Gabi no EasyPanel

## 📋 Visão Geral

Este guia mostra como fazer o deploy do n.Gabi usando o EasyPanel, aproveitando todas as funcionalidades da plataforma: deploy automatizado, SSL automático, backups e monitoramento.

## 🏗️ Arquitetura no EasyPanel

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
                    │   Domínios      │
                    │   ngabi.ness.   │
                    │   tec.br        │
                    └─────────────────┘
```

## 🚀 Passo a Passo do Deploy

### 1. **Preparação do Repositório**

#### Estrutura Necessária
```
ngabi/
├── frontend/                 # React SPA
├── backend/                  # FastAPI API
├── scripts/                  # Scripts de deploy
├── easypanel-config.yml      # Configuração EasyPanel
├── easypanel.env             # Variáveis de ambiente
├── docker-compose.yml        # Configuração local
└── README.md
```

#### Commits Necessários
```bash
# Adicionar arquivos de configuração
git add easypanel-config.yml easypanel.env scripts/
git commit -m "feat: Adicionar configuração EasyPanel"

# Push para o repositório
git push origin main
```

### 2. **Configuração no EasyPanel**

#### A. Criar Novo Projeto
1. Acesse o painel do EasyPanel
2. Clique em "New Project"
3. Nome: `ngabi`
4. Description: `Plataforma de Chat Multi-Agente`

#### B. Conectar Repositório GitHub
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

### 3. **Configuração de Variáveis de Ambiente**

#### No Painel do EasyPanel
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

### 4. **Deploy Automatizado**

#### A. Primeiro Deploy
1. Clique em "Deploy"
2. EasyPanel irá:
   - Clonar o repositório
   - Construir as imagens Docker
   - Configurar os serviços
   - Configurar SSL automaticamente
   - Fazer health checks

#### B. Deploy Contínuo
- A cada push para `main`, o EasyPanel fará deploy automático
- Zero-downtime deployment
- Rollback automático em caso de falha

### 5. **Verificação Pós-Deploy**

#### A. Health Checks
```bash
# Frontend
curl -f https://ngabi.ness.tec.br

# Backend
curl -f https://api.ngabi.ness.tec.br/health

# API Events
curl -f https://api.ngabi.ness.tec.br/api/v1/events/types

# API Webhooks
curl -f https://api.ngabi.ness.tec.br/api/v1/webhooks/events
```

#### B. SSL Verification
```bash
# Verificar certificados
openssl s_client -connect ngabi.ness.tec.br:443 -servername ngabi.ness.tec.br
openssl s_client -connect api.ngabi.ness.tec.br:443 -servername api.ngabi.ness.tec.br
```

## 🔧 Configurações Avançadas

### 1. **Backup Automático**

#### Configurar no EasyPanel
```bash
# Habilitar backup do PostgreSQL
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
BACKUP_SCHEDULE=0 2 * * *  # Diariamente às 2h
```

#### Backup Manual
```bash
# Via EasyPanel Terminal
docker-compose exec postgres pg_dump -U ngabi_user ngabi_backup > backup_$(date +%Y%m%d).sql
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

#### Auto-Scaling (Beta)
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
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 🛡️ Segurança

### 1. **SSL/TLS**
- ✅ Certificados Let's Encrypt automáticos
- ✅ Renovação automática
- ✅ HTTP/2 habilitado
- ✅ HSTS headers

### 2. **Firewall**
```bash
# Portas abertas
80   - HTTP (redirect para HTTPS)
443  - HTTPS
22   - SSH (se necessário)
```

### 3. **Rate Limiting**
```python
# Configurado no backend
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 📊 Monitoramento e Logs

### 1. **Logs Estruturados**
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

### 2. **Métricas Prometheus**
```bash
# Endpoint de métricas
curl https://api.ngabi.ness.tec.br/metrics

# Métricas disponíveis
- http_requests_total
- http_request_duration_seconds
- redis_operations_total
- event_emissions_total
```

### 3. **Alertas**
- CPU > 80%
- Memory > 80%
- Disk > 90%
- Service down
- SSL certificate expiring

## 🔄 CI/CD Pipeline

### 1. **GitHub Actions (Opcional)**
```yaml
# .github/workflows/easypanel-deploy.yml
name: Deploy to EasyPanel
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to EasyPanel
        run: |
          # EasyPanel faz deploy automático
          echo "Deploy iniciado automaticamente"
```

### 2. **Deploy Manual**
```bash
# Via EasyPanel Dashboard
1. Acesse o projeto
2. Clique em "Deploy"
3. Selecione branch/commit
4. Clique em "Deploy Now"
```

## 🚨 Troubleshooting

### 1. **Problemas Comuns**

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

### 2. **Comandos Úteis**

#### A. Logs
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### B. Status
```bash
# Status dos containers
docker-compose ps

# Health checks
docker-compose exec backend curl -f http://localhost:8000/health
```

#### C. Restart
```bash
# Restart específico
docker-compose restart backend

# Restart completo
docker-compose down && docker-compose up -d
```

## 📈 Performance

### 1. **Otimizações**

#### A. Redis
```bash
# Configuração otimizada
REDIS_MAX_MEMORY=256mb
REDIS_MAX_MEMORY_POLICY=allkeys-lru
```

#### B. Backend
```bash
# Workers
WORKER_PROCESSES=4

# Cache
CACHE_TTL=3600
```

#### C. Frontend
```bash
# Build otimizado
NODE_ENV=production
VITE_API_BASE_URL=https://api.ngabi.ness.tec.br
```

### 2. **Benchmarks**
```bash
# Teste de carga
ab -n 1000 -c 10 https://api.ngabi.ness.tec.br/health

# Teste de latência
curl -w "@curl-format.txt" -o /dev/null -s https://api.ngabi.ness.tec.br/health
```

## 🎯 Próximos Passos

### 1. **Melhorias Futuras**
- [ ] **CDN**: Cloudflare para assets estáticos
- [ ] **Load Balancer**: Múltiplas instâncias
- [ ] **Database**: Migração para PostgreSQL local
- [ ] **Monitoring**: Grafana + Prometheus
- [ ] **Backup**: S3 para backups remotos

### 2. **Integrações**
- [ ] **Slack**: Notificações de deploy
- [ ] **Email**: Alertas de monitoramento
- [ ] **Analytics**: Google Analytics
- [ ] **Error Tracking**: Sentry

---

## 🎉 **Deploy Concluído!**

O n.Gabi está agora rodando em produção no EasyPanel com:
- ✅ **Deploy automatizado** com zero-downtime
- ✅ **SSL automático** com Let's Encrypt
- ✅ **Backup automático** do banco de dados
- ✅ **Monitoramento completo** com logs e métricas
- ✅ **Sistema de eventos** e webhooks funcionando
- ✅ **Escalabilidade** preparada para crescimento

**URLs de Acesso:**
- 🌐 **Frontend**: https://ngabi.ness.tec.br
- 🔧 **Backend API**: https://api.ngabi.ness.tec.br
- 📊 **Traefik Dashboard**: https://traefik.ngabi.ness.tec.br
- 📚 **API Docs**: https://api.ngabi.ness.tec.br/docs

**Comandos Úteis:**
```bash
# Status dos serviços
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Deploy manual
./scripts/deploy.sh
``` 