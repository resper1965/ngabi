# 🚀 Sistema de Eventos Híbrido e Webhooks - n.Gabi

## 📋 Visão Geral

O n.Gabi agora possui um **sistema de eventos híbrido** que combina:
- ✅ **Processamento em tempo real** (sem persistência)
- ✅ **Persistência seletiva** (apenas eventos críticos)
- ✅ **Sistema de webhooks** para integrações externas
- ✅ **Reprocessamento automático** de eventos falhados

## 🏗️ Arquitetura

### Sistema de Eventos Híbrido

```python
# Eventos CRÍTICOS (são persistidos)
- chat_message
- user_login
- user_logout
- agent_created
- agent_updated
- agent_deleted
- tenant_created
- tenant_updated
- error_occurred
- rate_limit_exceeded

# Eventos NÃO-CRÍTICOS (não são persistidos)
- cache_cleared
- webhook_sent
- notification_sent
```

### Fluxo de Processamento

```
1. Evento acontece → event_system.emit()
2. Sistema decide se persiste (baseado no tipo)
3. Se crítico → Salva no banco (tabela events)
4. Processa listeners em paralelo
5. Envia webhooks em background
6. Log do resultado
```

## 📊 Tabelas do Banco

### Tabela `events`
```sql
CREATE TABLE events (
    id UUID PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE,
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID,
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT
);
```

### Tabela `webhooks`
```sql
CREATE TABLE webhooks (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    event_type VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    secret TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## 🔧 Como Usar

### 1. Emitir Eventos

```python
from app.core.events import event_system, EventType

# Emitir evento (persistência automática)
await event_system.emit(EventType.CHAT_MESSAGE.value, {
    'tenant_id': tenant_id,
    'user_id': user_id,
    'agent_id': agent_id,
    'message': message,
    'response': response
})

# Emitir evento sem persistir
await event_system.emit(EventType.CACHE_CLEARED.value, {
    'tenant_id': tenant_id,
    'cache_type': 'chat'
}, persist=False)
```

### 2. Registrar Listeners

```python
from app.core.events import event_system

@event_system.on("chat_message")
async def handle_chat_message(data):
    # Processar mensagem de chat
    print(f"Chat message: {data['message']}")

@event_system.on("user_login")
async def handle_user_login(data):
    # Processar login de usuário
    print(f"User login: {data['user_id']}")
```

### 3. Configurar Webhooks

```bash
# Registrar webhook
curl -X POST http://localhost:8000/api/v1/webhooks/register \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "chat_message",
    "url": "https://meu-sistema.com/webhook",
    "secret": "minha-chave-secreta"
  }'

# Listar webhooks
curl http://localhost:8000/api/v1/webhooks/list

# Testar webhook
curl -X POST http://localhost:8000/api/v1/webhooks/test \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://meu-sistema.com/webhook",
    "secret": "minha-chave-secreta"
  }'
```

## 📡 Endpoints da API

### Eventos (`/api/v1/events`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/history` | Histórico de eventos |
| GET | `/stats` | Estatísticas de eventos |
| POST | `/reprocess` | Reprocessar eventos falhados |
| GET | `/types` | Tipos de eventos disponíveis |
| POST | `/test` | Testar sistema de eventos |
| DELETE | `/clear` | Limpar histórico antigo |

### Webhooks (`/api/v1/webhooks`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/register` | Registrar webhook |
| DELETE | `/unregister/{id}` | Remover webhook |
| GET | `/list` | Listar webhooks |
| POST | `/test` | Testar webhook |
| GET | `/events` | Eventos disponíveis |
| POST | `/receive` | Receber webhook (exemplo) |

## 🔍 Monitoramento

### Health Check de Eventos
```bash
curl http://localhost:8000/api/v1/events/stats?days=7
```

### Verificar Eventos Falhados
```bash
curl -X POST http://localhost:8000/api/v1/events/reprocess
```

### Estatísticas de Webhooks
```bash
curl http://localhost:8000/api/v1/webhooks/list
```

## 🛡️ Segurança

### Assinatura de Webhooks
Os webhooks são assinados com HMAC-SHA256:

```python
# Headers enviados
{
    "Content-Type": "application/json",
    "User-Agent": "nGabi-Webhook/1.0",
    "X-nGabi-Signature": "sha256=abc123..."
}
```

### Row Level Security (RLS)
- Eventos só são visíveis para o tenant correspondente
- Webhooks só são acessíveis pelo tenant proprietário
- Autenticação obrigatória para todas as operações

## 📈 Benefícios

### Para Desenvolvedores
- ✅ **Desacoplamento**: Adicionar funcionalidades sem modificar código existente
- ✅ **Testabilidade**: Fácil testar cada parte separadamente
- ✅ **Flexibilidade**: Sistema extensível e configurável

### Para Operações
- ✅ **Auditoria**: Histórico completo de eventos críticos
- ✅ **Monitoramento**: Métricas e estatísticas detalhadas
- ✅ **Recuperação**: Reprocessamento automático de falhas

### Para Integrações
- ✅ **Webhooks**: Notificações em tempo real para sistemas externos
- ✅ **Escalabilidade**: Processamento assíncrono e paralelo
- ✅ **Confiabilidade**: Retry automático e tratamento de erros

## 🚀 Exemplos Práticos

### 1. Sistema de Notificações
```python
@event_system.on("chat_message")
async def send_notification(data):
    # Enviar email quando usuário envia mensagem
    await send_email_notification(data)

@event_system.on("error_occurred")
async def alert_admin(data):
    # Alertar admin sobre erros
    await send_admin_alert(data)
```

### 2. Analytics em Tempo Real
```python
@event_system.on("user_login")
async def track_user_activity(data):
    # Atualizar analytics
    await update_user_analytics(data)

@event_system.on("chat_message")
async def track_chat_metrics(data):
    # Calcular métricas de chat
    await update_chat_metrics(data)
```

### 3. Integração com Sistemas Externos
```python
# Webhook para Slack
{
    "event_type": "chat_message",
    "url": "https://hooks.slack.com/services/...",
    "secret": "slack-secret"
}

# Webhook para CRM
{
    "event_type": "user_login",
    "url": "https://meu-crm.com/webhook",
    "secret": "crm-secret"
}
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Configurações de eventos (opcional)
EVENT_PERSISTENCE_ENABLED=true
EVENT_RETRY_MAX_ATTEMPTS=3
EVENT_CLEANUP_DAYS=30

# Configurações de webhooks (opcional)
WEBHOOK_TIMEOUT_SECONDS=10
WEBHOOK_MAX_RETRIES=3
```

### Inicialização
O sistema é inicializado automaticamente no startup da aplicação:

```python
# Em app/main.py
@app.on_event("startup")
async def startup_event():
    # Sistema de eventos já está pronto
    logger.info("✅ Sistema de eventos inicializado")
```

## 📚 Próximos Passos

### Melhorias Futuras
- [ ] **Fila de Processamento**: Redis/Celery para eventos pesados
- [ ] **Filtros Avançados**: Condições complexas para webhooks
- [ ] **Métricas Avançadas**: Grafana dashboard
- [ ] **Notificações Push**: WebSockets para notificações em tempo real
- [ ] **Templates de Webhooks**: Configurações pré-definidas

### Integrações Sugeridas
- [ ] **Slack**: Notificações de chat
- [ ] **Email**: Notificações por email
- [ ] **SMS**: Alertas críticos
- [ ] **Analytics**: Google Analytics, Mixpanel
- [ ] **CRM**: Salesforce, HubSpot

---

**Sistema implementado e pronto para uso!** 🎉

O sistema de eventos híbrido e webhooks está totalmente funcional e integrado ao n.Gabi. Permite monitoramento completo, integrações externas e escalabilidade para o futuro. 