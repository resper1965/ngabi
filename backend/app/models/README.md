# Modelos SQLAlchemy - Chat Multi-Agente

## 📊 Visão Geral dos Modelos

Este documento descreve todos os modelos SQLAlchemy do sistema, incluindo relacionamentos, índices e constraints.

## 🏢 Tenant (Organizações)

**Tabela:** `tenants`

### Campos
- `id` (UUID) - Chave primária
- `name` (TEXT) - Nome da organização
- `subdomain` (TEXT) - Subdomínio único
- `created_at` (TIMESTAMP) - Data de criação

### Relacionamentos
- `users` → Lista de usuários (1:N)
- `agents` → Lista de agentes (1:N)
- `settings` → Configurações de branding (1:1)
- `chat_history` → Histórico de chat (1:N)

### Índices
- `idx_tenants_subdomain` - Busca por subdomínio
- `idx_tenants_created_at` - Ordenação por data

### Constraints
- `subdomain` único

## 👤 User (Usuários)

**Tabela:** `users`

### Campos
- `id` (UUID) - Chave primária
- `tenant_id` (UUID) - Referência ao tenant
- `email` (TEXT) - Email do usuário
- `password_hash` (TEXT) - Hash da senha
- `role` (TEXT) - 'admin', 'user', 'developer'
- `is_active` (BOOLEAN) - Status ativo
- `created_at` (TIMESTAMP) - Data de criação

### Relacionamentos
- `tenant` → Tenant pai (N:1)
- `chat_history` → Histórico de chat (1:N)

### Índices
- `idx_users_tenant_id` - Filtro por tenant
- `idx_users_email` - Busca por email
- `idx_users_role` - Filtro por role
- `idx_users_is_active` - Filtro por status
- `idx_users_created_at` - Ordenação por data

### Constraints
- `tenant_id + email` único (email único por tenant)

## 🤖 Agent (Agentes de IA)

**Tabela:** `agents`

### Campos
- `id` (UUID) - Chave primária
- `tenant_id` (UUID) - Referência ao tenant
- `name` (TEXT) - Nome do agente
- `config` (JSONB) - Configuração do agente
- `created_at` (TIMESTAMP) - Data de criação

### Relacionamentos
- `tenant` → Tenant pai (N:1)
- `chat_history` → Histórico de chat (1:N)

### Índices
- `idx_agents_tenant_id` - Filtro por tenant
- `idx_agents_name` - Busca por nome
- `idx_agents_created_at` - Ordenação por data

### Constraints
- `tenant_id + name` único (nome único por tenant)

### Exemplo de Config JSONB
```json
{
  "prompt_template": "Você é um assistente jurídico...",
  "kb_filters": ["livros", "jurisprudencia"],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

## 🎨 TenantSettings (Configurações de Branding)

**Tabela:** `tenant_settings`

### Campos
- `tenant_id` (UUID) - Chave primária e referência
- `logo_path` (TEXT) - Caminho do logo
- `orchestrator_name` (TEXT) - Nome do orquestrador
- `theme_primary` (CHAR(7)) - Cor primária (#RRGGBB)
- `theme_secondary` (CHAR(7)) - Cor secundária (#RRGGBB)
- `contact_email` (TEXT) - Email de contato
- `contact_phone` (TEXT) - Telefone de contato
- `updated_at` (TIMESTAMP) - Data de atualização

### Relacionamentos
- `tenant` → Tenant pai (1:1)

### Índices
- `idx_tenant_settings_updated_at` - Ordenação por atualização

## 💬 ChatHistory (Histórico de Chat)

**Tabela:** `chat_history`

### Campos
- `id` (BIGSERIAL) - Chave primária
- `tenant_id` (UUID) - Referência ao tenant
- `user_id` (UUID) - Referência ao usuário
- `agent_id` (UUID) - Referência ao agente
- `message` (TEXT) - Mensagem do usuário
- `response` (TEXT) - Resposta do agente
- `chat_mode` (TEXT) - 'UsoCotidiano' ou 'EscritaLonga'
- `use_author_voice` (BOOLEAN) - Usar voz do autor
- `created_at` (TIMESTAMP) - Data de criação

### Relacionamentos
- `tenant` → Tenant pai (N:1)
- `user` → Usuário (N:1)
- `agent` → Agente (N:1)
- `messages` → Mensagens individuais (1:N)

### Índices
- `idx_chat_history_tenant_id` - Filtro por tenant
- `idx_chat_history_user_id` - Filtro por usuário
- `idx_chat_history_agent_id` - Filtro por agente
- `idx_chat_history_created_at` - Ordenação por data
- `idx_chat_history_tenant_created` - Composto (tenant + data)
- `idx_chat_history_chat_mode` - Filtro por modo

## 💭 Message (Mensagens Individuais)

**Tabela:** `messages`

### Campos
- `id` (BIGSERIAL) - Chave primária
- `chat_id` (BIGINT) - Referência ao chat
- `speaker` (TEXT) - 'user' ou 'agent'
- `content` (TEXT) - Conteúdo da mensagem
- `created_at` (TIMESTAMP) - Data de criação

### Relacionamentos
- `chat` → Chat pai (N:1)

### Índices
- `idx_messages_chat_id` - Filtro por chat
- `idx_messages_speaker` - Filtro por falante
- `idx_messages_created_at` - Ordenação por data

## 🔗 Diagrama de Relacionamentos

```
Tenant (1) ←→ (N) User
   ↓
Tenant (1) ←→ (1) TenantSettings
   ↓
Tenant (1) ←→ (N) Agent
   ↓
Tenant (1) ←→ (N) ChatHistory (N) ←→ (1) User
   ↓                                    ↓
ChatHistory (1) ←→ (N) Message    Agent (1) ←→ (N) ChatHistory
```

## 🚀 Uso dos Modelos

### Exemplo de Criação
```python
from app.models import Tenant, User, Agent
from app.database import SessionLocal

db = SessionLocal()

# Criar tenant
tenant = Tenant(name="Empresa ABC", subdomain="empresa-abc")
db.add(tenant)
db.commit()

# Criar usuário
user = User(
    tenant_id=tenant.id,
    email="admin@empresa-abc.com",
    password_hash="hash_da_senha",
    role="admin"
)
db.add(user)
db.commit()

# Criar agente
agent = Agent(
    tenant_id=tenant.id,
    name="LexAI",
    config={
        "prompt_template": "Você é um assistente jurídico...",
        "kb_filters": ["livros", "jurisprudencia"]
    }
)
db.add(agent)
db.commit()
```

### Exemplo de Consulta com Relacionamentos
```python
# Buscar tenant com todos os relacionamentos
tenant = db.query(Tenant).filter(Tenant.subdomain == "empresa-abc").first()

# Acessar relacionamentos
print(f"Tenant: {tenant.name}")
print(f"Usuários: {len(tenant.users)}")
print(f"Agentes: {len(tenant.agents)}")
print(f"Configurações: {tenant.settings.orchestrator_name if tenant.settings else 'N/A'}")

# Buscar chat history com relacionamentos
chats = db.query(ChatHistory).filter(
    ChatHistory.tenant_id == tenant.id
).options(
    joinedload(ChatHistory.user),
    joinedload(ChatHistory.agent)
).all()

for chat in chats:
    print(f"Chat {chat.id}: {chat.user.email} → {chat.agent.name}")
```

## 📝 Notas Importantes

1. **Isolamento por Tenant**: Todos os modelos (exceto Tenant) têm `tenant_id`
2. **Cascade**: Deletar tenant remove todos os dados relacionados
3. **UUIDs**: Usados para IDs de entidades principais
4. **Timestamps**: Todos os modelos têm `created_at`/`updated_at`
5. **Índices**: Otimizados para consultas por tenant e ordenação
6. **Constraints**: Garantem integridade referencial e unicidade 