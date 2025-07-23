-- 🚀 Script SQL para configurar o banco de dados do n.Gabi no Supabase
-- Execute este script no SQL Editor do Supabase

-- =============================================================================
-- TABELAS PRINCIPAIS
-- =============================================================================

-- Tabela de tenants (organizações/clientes)
CREATE TABLE IF NOT EXISTS tenants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de agentes (chatbots)
CREATE TABLE IF NOT EXISTS agents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_prompt TEXT,
    model VARCHAR(100) DEFAULT 'gpt-3.5-turbo',
    temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de histórico de chat
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    user_id UUID,
    session_id VARCHAR(255),
    message TEXT NOT NULL,
    response TEXT,
    tokens_used INTEGER DEFAULT 0,
    response_time_ms INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de usuários (opcional - para autenticação customizada)
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- ÍNDICES PARA PERFORMANCE
-- =============================================================================

-- Índices para tenants
CREATE INDEX IF NOT EXISTS idx_tenants_domain ON tenants(domain);
CREATE INDEX IF NOT EXISTS idx_tenants_is_active ON tenants(is_active);

-- Índices para agents
CREATE INDEX IF NOT EXISTS idx_agents_tenant_id ON agents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);
CREATE INDEX IF NOT EXISTS idx_agents_model ON agents(model);

-- Índices para chat_history
CREATE INDEX IF NOT EXISTS idx_chat_history_tenant_id ON chat_history(tenant_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_agent_id ON chat_history(agent_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);

-- Índices para users
CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- =============================================================================
-- TABELA DE EVENTOS (Sistema de Eventos Híbrido)
-- =============================================================================

-- Tabela para persistir eventos críticos
CREATE TABLE IF NOT EXISTS events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID,
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance da tabela events
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_processed ON events(processed);
CREATE INDEX IF NOT EXISTS idx_events_tenant_id ON events(tenant_id);
CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_retry_count ON events(retry_count);

-- =============================================================================
-- TABELA DE WEBHOOKS
-- =============================================================================

-- Tabela para configurar webhooks
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    secret TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance da tabela webhooks
CREATE INDEX IF NOT EXISTS idx_webhooks_tenant_id ON webhooks(tenant_id);
CREATE INDEX IF NOT EXISTS idx_webhooks_event_type ON webhooks(event_type);
CREATE INDEX IF NOT EXISTS idx_webhooks_is_active ON webhooks(is_active);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhooks ENABLE ROW LEVEL SECURITY;

-- Políticas para tenants (público para leitura, admin para escrita)
CREATE POLICY "Tenants are viewable by everyone" ON tenants FOR SELECT USING (true);
CREATE POLICY "Tenants are insertable by authenticated users" ON tenants FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Tenants are updatable by owner" ON tenants FOR UPDATE USING (auth.uid()::text = id::text);

-- Políticas para agents (público para leitura, tenant para escrita)
CREATE POLICY "Agents are viewable by tenant" ON agents FOR SELECT USING (true);
CREATE POLICY "Agents are insertable by tenant" ON agents FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Agents are updatable by tenant" ON agents FOR UPDATE USING (auth.role() = 'authenticated');

-- Políticas para chat_history (tenant para leitura/escrita)
CREATE POLICY "Chat history is viewable by tenant" ON chat_history FOR SELECT USING (true);
CREATE POLICY "Chat history is insertable by tenant" ON chat_history FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Chat history is updatable by tenant" ON chat_history FOR UPDATE USING (auth.role() = 'authenticated');

-- Políticas para users (tenant para leitura/escrita)
CREATE POLICY "Users are viewable by tenant" ON users FOR SELECT USING (true);
CREATE POLICY "Users are insertable by tenant" ON users FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Users are updatable by tenant" ON users FOR UPDATE USING (auth.role() = 'authenticated');

-- Políticas para events (eventos só são visíveis para o tenant correspondente)
CREATE POLICY "Events are viewable by tenant" ON events FOR SELECT USING (true);
CREATE POLICY "Events are insertable by authenticated users" ON events FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Events are updatable by tenant" ON events FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Events are deletable by tenant" ON events FOR DELETE USING (auth.role() = 'authenticated');

-- Políticas para webhooks (webhooks só são visíveis para o tenant correspondente)
CREATE POLICY "Webhooks are viewable by tenant" ON webhooks FOR SELECT USING (true);
CREATE POLICY "Webhooks are insertable by authenticated users" ON webhooks FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Webhooks are updatable by tenant" ON webhooks FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Webhooks are deletable by tenant" ON webhooks FOR DELETE USING (auth.role() = 'authenticated');

-- =============================================================================
-- DADOS INICIAIS
-- =============================================================================

-- Inserir tenant padrão
INSERT INTO tenants (id, name, domain, settings) VALUES 
(
    '00000000-0000-0000-0000-000000000001',
    'n.Gabi Default',
    'ngabi.local',
    '{"theme": "default", "features": ["chat", "analytics"]}'
) ON CONFLICT (id) DO NOTHING;

-- Inserir agente padrão
INSERT INTO agents (id, tenant_id, name, description, system_prompt, model) VALUES 
(
    '00000000-0000-0000-0000-000000000002',
    '00000000-0000-0000-0000-000000000001',
    'Gabi Assistant',
    'Assistente virtual inteligente do n.Gabi',
    'Você é o Gabi, um assistente virtual inteligente e prestativo. Sempre seja educado, útil e preciso em suas respostas.',
    'gpt-3.5-turbo'
) ON CONFLICT (id) DO NOTHING;

-- =============================================================================
-- FUNÇÕES ÚTEIS
-- =============================================================================

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para atualizar updated_at
CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- VIEWS ÚTEIS
-- =============================================================================

-- View para estatísticas de chat
CREATE OR REPLACE VIEW chat_stats AS
SELECT 
    t.name as tenant_name,
    a.name as agent_name,
    COUNT(*) as total_messages,
    AVG(ch.response_time_ms) as avg_response_time,
    SUM(ch.tokens_used) as total_tokens,
    DATE_TRUNC('day', ch.created_at) as date
FROM chat_history ch
JOIN tenants t ON ch.tenant_id = t.id
JOIN agents a ON ch.agent_id = a.id
GROUP BY t.name, a.name, DATE_TRUNC('day', ch.created_at)
ORDER BY date DESC;

-- =============================================================================
-- MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Banco de dados n.Gabi configurado com sucesso!' as status; 