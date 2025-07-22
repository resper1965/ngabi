# 🚀 n.Gabi + Supabase - Integração Completa

## 📋 Visão Geral

O **n.Gabi** agora está totalmente integrado com o **Supabase**, aproveitando todas as funcionalidades da plataforma: PostgreSQL gerenciado, autenticação, realtime, storage e functions serverless.

## ✨ Funcionalidades Integradas

### 🎯 **Core Features**
- ✅ **PostgreSQL Gerenciado** com RLS (Row Level Security)
- ✅ **Autenticação Completa** com múltiplos providers
- ✅ **Realtime** para chat e eventos em tempo real
- ✅ **Storage** para arquivos e avatares
- ✅ **Functions Serverless** para processamento
- ✅ **Sistema de Eventos Híbrido** (tempo real + persistência)
- ✅ **Webhooks** para integrações externas
- ✅ **Multi-tenancy** com isolamento completo

### 🚀 **Supabase Features**
- ✅ **Backup Automático** e PITR (Point-in-Time Recovery)
- ✅ **SSL Automático** e segurança robusta
- ✅ **SDKs Multilinguagem** (JavaScript, Python, etc.)
- ✅ **Dashboard Unificado** para gerenciamento
- ✅ **Escalabilidade** automática
- ✅ **Open Source** e self-hosting disponível

## 🏗️ Arquitetura Integrada

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Supabase      │
│   (React)       │    │   (FastAPI)     │    │   (PostgreSQL)  │
│   Porta 3000    │    │   Porta 8000    │    │   + Auth        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Supabase      │
                    │   Realtime      │
                    │   + Storage     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Supabase      │
                    │   Functions     │
                    │   (Serverless)  │
                    └─────────────────┘
```

## 🚀 Deploy Rápido

### 1. **Pré-requisitos**
- ✅ Projeto Supabase criado
- ✅ Supabase CLI instalado (opcional)
- ✅ PostgreSQL client (psql)
- ✅ curl para testes

### 2. **Configuração de Variáveis**

```bash
# Supabase Configuration
SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OAuth Providers (opcional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### 3. **Migração Automática**

```bash
# Executar migração completa
./scripts/migrate-supabase.sh
```

O script irá:
- ✅ Migrar schema completo
- ✅ Configurar RLS (Row Level Security)
- ✅ Habilitar Realtime
- ✅ Configurar Storage
- ✅ Configurar autenticação
- ✅ Deploy de functions
- ✅ Inserir dados iniciais
- ✅ Executar testes de integração

## 🔧 Configurações Detalhadas

### 1. **Banco de Dados PostgreSQL**

#### Tabelas Principais
- **`tenants`** - Organizações/clientes
- **`users`** - Usuários (integração com auth.users)
- **`agents`** - Agentes de IA
- **`chat_history`** - Histórico de conversas
- **`events`** - Sistema de eventos híbrido
- **`webhooks`** - Configurações de webhooks
- **`files`** - Metadados de arquivos
- **`presence`** - Status online de usuários

#### Row Level Security (RLS)
```sql
-- Exemplo: Política para chat_history
CREATE POLICY "Chat history is viewable by tenant" ON chat_history
FOR SELECT USING (
    tenant_id IN (
        SELECT tenant_id FROM users WHERE id = auth.uid()
    )
);
```

### 2. **Autenticação**

#### Providers Suportados
- ✅ **Email/Password** - Login tradicional
- ✅ **Google OAuth** - Login com Google
- ✅ **GitHub OAuth** - Login com GitHub
- ✅ **Magic Links** - Login sem senha
- ✅ **Phone Auth** - Login por SMS

#### Configuração no Frontend
```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://tegbkyeqfrqkuxeilgpc.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
)

// Login
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password'
})

// Signup
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password',
  options: {
    data: {
      name: 'John Doe',
      tenant_id: 'tenant-uuid'
    }
  }
})
```

### 3. **Realtime**

#### Configuração de Canais
```typescript
// Canal para chat em tempo real
const channel = supabase
  .channel('chat_messages')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'chat_history',
      filter: `tenant_id=eq.${tenantId}`
    },
    (payload) => {
      console.log('Nova mensagem:', payload.new);
      // Atualizar UI em tempo real
    }
  )
  .subscribe()

// Canal para presence (usuários online)
const presenceChannel = supabase.channel('chat_presence', {
  config: {
    presence: {
      key: user.id,
    },
  },
});

await presenceChannel.track({
  user_id: user.id,
  user_name: user.name,
  tenant_id: tenantId,
  online_at: new Date().toISOString(),
});
```

### 4. **Storage**

#### Buckets Configurados
- **`avatars`** - Avatares de usuários (público)
- **`chat-files`** - Arquivos de chat (privado)
- **`documents`** - Documentos (privado)
- **`backups`** - Backups (apenas admin)

#### Upload de Arquivos
```typescript
// Upload de avatar
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${user.id}/avatar.jpg`, file, {
    cacheControl: '3600',
    upsert: true
  })

// Download de arquivo
const { data, error } = await supabase.storage
  .from('chat-files')
  .download('tenant-uuid/document.pdf')

// URL pública
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${user.id}/avatar.jpg`)
```

### 5. **Functions Serverless**

#### Functions Disponíveis
- **`process-chat`** - Processamento de mensagens com IA
- **`webhook-dispatcher`** - Envio de webhooks
- **`auth-webhook`** - Processamento de eventos de auth

#### Exemplo de Function
```typescript
// supabase/functions/process-chat/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const { message, agent_id, user_id, tenant_id } = await req.json()
  
  // Processar com IA
  const response = await processWithAI(message, agent_id)
  
  // Salvar no histórico
  const { data, error } = await supabase
    .from('chat_history')
    .insert({
      tenant_id,
      user_id,
      agent_id,
      message,
      response: response.text
    })
  
  return new Response(JSON.stringify({ success: true, data }))
})
```

## 📡 APIs Disponíveis

### **REST API Automática**
```bash
# Listar agentes
GET /rest/v1/agents?tenant_id=eq.tenant-uuid

# Criar agente
POST /rest/v1/agents
{
  "tenant_id": "tenant-uuid",
  "name": "Novo Agente",
  "description": "Descrição do agente"
}

# Histórico de chat
GET /rest/v1/chat_history?tenant_id=eq.tenant-uuid&order=created_at.desc
```

### **GraphQL (via pg_graphql)**
```graphql
query GetChatHistory($tenantId: UUID!) {
  chatHistoryCollection(
    filter: { tenantId: { eq: $tenantId } }
    orderBy: { createdAt: DescNullsLast }
  ) {
    edges {
      node {
        id
        message
        response
        createdAt
        user {
          name
          email
        }
        agent {
          name
        }
      }
    }
  }
}
```

## 🛡️ Segurança

### **Row Level Security (RLS)**
- ✅ **Isolamento por tenant** - Dados isolados por organização
- ✅ **Controle de acesso** - Usuários só veem dados do seu tenant
- ✅ **Políticas granulares** - Controle fino de permissões
- ✅ **Auditoria** - Logs de todas as operações

### **Autenticação**
- ✅ **JWT Tokens** - Tokens seguros e expiráveis
- ✅ **Refresh Tokens** - Renovação automática
- ✅ **Multi-factor Auth** - Suporte a MFA
- ✅ **Session Management** - Gerenciamento de sessões

### **Storage Security**
- ✅ **URLs Assinadas** - URLs temporárias para arquivos privados
- ✅ **Políticas de Bucket** - Controle de acesso por bucket
- ✅ **Validação de MIME** - Tipos de arquivo permitidos
- ✅ **Limite de Tamanho** - Controle de tamanho de arquivos

## 📊 Monitoramento e Analytics

### **Logs Estruturados**
```json
{
  "timestamp": "2024-07-22T12:00:00Z",
  "level": "INFO",
  "service": "chat",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "action": "message_sent",
  "metadata": {
    "agent_id": "uuid",
    "tokens_used": 150,
    "response_time_ms": 1200
  }
}
```

### **Métricas Disponíveis**
- 📈 **Total de mensagens** por tenant
- ⏱️ **Tempo médio de resposta**
- 💰 **Custo por token** usado
- 👥 **Usuários ativos** por período
- 🤖 **Agentes mais usados**

### **Views de Analytics**
```sql
-- Estatísticas de chat
SELECT * FROM chat_stats_view;

-- Usuários online
SELECT * FROM online_users_view;

-- Uso por tenant
SELECT * FROM tenant_usage_view;

-- Performance
SELECT * FROM performance_metrics_view;
```

## 🔄 Integração com Backend

### **Configuração do FastAPI**
```python
from supabase import create_client, Client
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

# Configuração do cliente Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# Middleware de autenticação
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        user = supabase.auth.get_user(credentials.credentials)
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

# Endpoint protegido
@app.post("/chat")
async def send_message(
    request: ChatRequest,
    current_user = Depends(get_current_user)
):
    # Lógica do chat
    pass
```

### **Sistema de Eventos**
```python
# Emitir evento
await supabase.table('events').insert({
    'event_type': 'chat_message',
    'tenant_id': tenant_id,
    'user_id': user_id,
    'data': {
        'message': message,
        'response': response,
        'agent_id': agent_id
    }
}).execute()

# Escutar eventos em tempo real
def handle_event(payload):
    print(f"Novo evento: {payload['new']}")

supabase.table('events').on('INSERT', handle_event).subscribe()
```

## 🚨 Troubleshooting

### **Problemas Comuns**

#### A. Conexão com Supabase
```bash
# Testar conexão
curl -f https://tegbkyeqfrqkuxeilgpc.supabase.co/rest/v1/

# Verificar variáveis
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY
```

#### B. RLS Bloqueando Acesso
```sql
-- Verificar políticas
SELECT * FROM pg_policies WHERE tablename = 'chat_history';

-- Testar acesso
SELECT * FROM chat_history WHERE tenant_id = 'your-tenant-id';
```

#### C. Realtime Não Funciona
```typescript
// Verificar subscription
const channel = supabase.channel('test')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'chat_history' }, 
    (payload) => console.log('Change received!', payload)
  )
  .subscribe()

// Verificar status
console.log('Channel status:', channel.subscribe())
```

### **Comandos Úteis**

```bash
# Verificar status das tabelas
psql $DATABASE_URL -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"

# Verificar políticas RLS
psql $DATABASE_URL -c "SELECT * FROM pg_policies;"

# Verificar funções
psql $DATABASE_URL -c "SELECT routine_name FROM information_schema.routines WHERE routine_schema = 'public';"

# Backup manual
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

## 📈 Performance

### **Otimizações**

#### Índices Estratégicos
```sql
-- Índices para performance
CREATE INDEX idx_chat_history_tenant_created ON chat_history(tenant_id, created_at);
CREATE INDEX idx_events_type_timestamp ON events(event_type, timestamp);
CREATE INDEX idx_users_tenant_email ON users(tenant_id, email);
```

#### Configuração de Cache
```typescript
// Cache de consultas frequentes
const { data } = await supabase
  .from('agents')
  .select('*')
  .eq('tenant_id', tenantId)
  .eq('is_active', true)
  .cache(300) // Cache por 5 minutos
```

#### Paginação Eficiente
```typescript
// Paginação com cursor
const { data } = await supabase
  .from('chat_history')
  .select('*')
  .eq('tenant_id', tenantId)
  .order('created_at', { ascending: false })
  .range(0, 49) // Primeira página
```

## 🎯 Próximos Passos

### **Melhorias Futuras**
- [ ] **Edge Functions** - Functions distribuídas geograficamente
- [ ] **Database Functions** - Lógica no banco para performance
- [ ] **Materialized Views** - Views materializadas para analytics
- [ ] **Partitioning** - Particionamento de tabelas grandes
- [ ] **Read Replicas** - Réplicas de leitura para performance

### **Integrações**
- [ ] **Stripe** - Pagamentos e assinaturas
- [ ] **SendGrid** - Emails transacionais
- [ ] **Slack** - Notificações e integrações
- [ ] **Zapier** - Automações
- [ ] **Analytics** - Google Analytics, Mixpanel

## 📚 Documentação

### **Arquivos Importantes**
- 📄 **`supabase/integration-config.md`** - Guia completo de integração
- 📄 **`supabase/advanced-schema.sql`** - Schema completo do banco
- 📄 **`supabase/realtime-config.sql`** - Configuração de realtime
- 📄 **`supabase/storage-config.sql`** - Configuração de storage
- 📄 **`scripts/migrate-supabase.sh`** - Script de migração

### **URLs de Acesso**
- 🌐 **Supabase Dashboard**: https://tegbkyeqfrqkuxeilgpc.supabase.co
- 📚 **API Docs**: https://tegbkyeqfrqkuxeilgpc.supabase.co/docs
- 🔧 **SQL Editor**: https://tegbkyeqfrqkuxeilgpc.supabase.co/sql
- 📊 **Analytics**: https://tegbkyeqfrqkuxeilgpc.supabase.co/analytics

### **Recursos Externos**
- 🔗 **Supabase Docs**: https://supabase.com/docs
- 🔗 **Supabase GitHub**: https://github.com/supabase/supabase
- 🔗 **Community**: https://supabase.com/community

---

## 🎉 **Integração Concluída!**

O n.Gabi está agora totalmente integrado com o Supabase, aproveitando:

- ✅ **PostgreSQL gerenciado** com RLS
- ✅ **Autenticação completa** com múltiplos providers
- ✅ **Realtime** para chat e eventos
- ✅ **Storage** para arquivos e avatares
- ✅ **Functions serverless** para processamento
- ✅ **Backup automático** e PITR
- ✅ **Monitoramento** e logs estruturados
- ✅ **Escalabilidade** automática

**🚀 Pronto para produção com Supabase!** 