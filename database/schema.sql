-- 1. Tabela de Organizações (Tenants)
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  subdomain TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 2. Tabela de Usuários
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL,           -- ex.: 'admin', 'user'
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_tenant ON users(tenant_id);

-- 3. Tabela de Agentes
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name TEXT NOT NULL,           -- ex.: 'LexAI', 'FinBot'
  config JSONB NOT NULL,        -- prompt templates, flows, KB filters
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (tenant_id, name)
);

CREATE INDEX idx_agents_tenant ON agents(tenant_id);

-- 4. Tabela de Configurações de Branding (Settings)
CREATE TABLE tenant_settings (
  tenant_id UUID PRIMARY KEY REFERENCES tenants(id) ON DELETE CASCADE,
  logo_path TEXT,               -- caminho no filesystem/NAS
  orchestrator_name TEXT,       -- nome customizado do agente orquestrador
  theme_primary CHAR(7),        -- ex.: '#1a73e8'
  theme_secondary CHAR(7),
  contact_email TEXT,
  contact_phone TEXT,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 5. Histórico de Chat
CREATE TABLE chat_history (
  id BIGSERIAL PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE SET NULL,
  message TEXT NOT NULL,
  response TEXT NOT NULL,
  chat_mode TEXT NOT NULL,      -- 'UsoCotidiano' ou 'EscritaLonga'
  use_author_voice BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_chat_tenant_created ON chat_history(tenant_id, created_at DESC);

-- 6. (Opcional) Tabela de Mensagens Unitárias
-- se você quiser granularizar a conversa turn-by-turn
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  chat_id BIGINT NOT NULL REFERENCES chat_history(id) ON DELETE CASCADE,
  speaker TEXT NOT NULL,        -- 'user' ou 'agent'
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_messages_chat ON messages(chat_id); 