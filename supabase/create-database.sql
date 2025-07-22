-- 🗄️ Script SQL para Criar Banco de Dados n.Gabi no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard

-- =============================================================================
-- EXTENSÕES NECESSÁRIAS
-- =============================================================================

-- Habilitar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_graphql";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- =============================================================================
-- TABELAS PRINCIPAIS
-- =============================================================================

-- Tabela de tenants (organizações/clientes)
CREATE TABLE IF NOT EXISTS tenants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    settings JSONB DEFAULT '{}',
    subscription_plan VARCHAR(50) DEFAULT 'free',
    max_users INTEGER DEFAULT 10,
    max_agents INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de usuários (integração com auth.users)
CREATE TABLE IF NOT EXISTS users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'moderator')),
    permissions JSONB DEFAULT '{}',
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de agentes
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
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    session_id UUID DEFAULT gen_random_uuid(),
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    chat_mode VARCHAR(100) DEFAULT 'UsoCotidiano',
    use_author_voice BOOLEAN DEFAULT false,
    response_time_ms INTEGER,
    tokens_used INTEGER,
    cost_usd DECIMAL(10,6) DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de eventos (sistema híbrido)
CREATE TABLE IF NOT EXISTS events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de webhooks
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    secret TEXT,
    headers JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    retry_count INTEGER DEFAULT 0,
    last_triggered TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de arquivos (integração com storage)
CREATE TABLE IF NOT EXISTS files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    bucket_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    metadata JSONB DEFAULT '{}',
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de sessões de chat
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    title VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de logs de auditoria
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de presence (usuários online)
CREATE TABLE IF NOT EXISTS presence (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID NOT NULL,
    status VARCHAR(50) DEFAULT 'online' CHECK (status IN ('online', 'away', 'offline')),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
# ÍNDICES PARA PERFORMANCE
-- =============================================================================

-- Índices para tenants
CREATE INDEX IF NOT EXISTS idx_tenants_domain ON tenants(domain);
CREATE INDEX IF NOT EXISTS idx_tenants_is_active ON tenants(is_active);
CREATE INDEX IF NOT EXISTS idx_tenants_subscription_plan ON tenants(subscription_plan);

-- Índices para users
CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login);

-- Índices para agents
CREATE INDEX IF NOT EXISTS idx_agents_tenant_id ON agents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);
CREATE INDEX IF NOT EXISTS idx_agents_model ON agents(model);

-- Índices para chat_history
CREATE INDEX IF NOT EXISTS idx_chat_history_tenant_id ON chat_history(tenant_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_agent_id ON chat_history(agent_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_history_chat_mode ON chat_history(chat_mode);

-- Índices para events
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_processed ON events(processed);
CREATE INDEX IF NOT EXISTS idx_events_tenant_id ON events(tenant_id);
CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_retry_count ON events(retry_count);
CREATE INDEX IF NOT EXISTS idx_events_priority ON events(priority);

-- Índices para webhooks
CREATE INDEX IF NOT EXISTS idx_webhooks_tenant_id ON webhooks(tenant_id);
CREATE INDEX IF NOT EXISTS idx_webhooks_event_type ON webhooks(event_type);
CREATE INDEX IF NOT EXISTS idx_webhooks_is_active ON webhooks(is_active);

-- Índices para files
CREATE INDEX IF NOT EXISTS idx_files_tenant_id ON files(tenant_id);
CREATE INDEX IF NOT EXISTS idx_files_user_id ON files(user_id);
CREATE INDEX IF NOT EXISTS idx_files_bucket_name ON files(bucket_name);
CREATE INDEX IF NOT EXISTS idx_files_is_public ON files(is_public);

-- Índices para chat_sessions
CREATE INDEX IF NOT EXISTS idx_chat_sessions_tenant_id ON chat_sessions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_agent_id ON chat_sessions(agent_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_status ON chat_sessions(status);

-- Índices para audit_logs
CREATE INDEX IF NOT EXISTS idx_audit_logs_tenant_id ON audit_logs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Índices para presence
CREATE INDEX IF NOT EXISTS idx_presence_tenant_id ON presence(tenant_id);
CREATE INDEX IF NOT EXISTS idx_presence_user_id ON presence(user_id);
CREATE INDEX IF NOT EXISTS idx_presence_session_id ON presence(session_id);
CREATE INDEX IF NOT EXISTS idx_presence_status ON presence(status);
CREATE INDEX IF NOT EXISTS idx_presence_last_seen ON presence(last_seen);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE files ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE presence ENABLE ROW LEVEL SECURITY;

-- Políticas para tenants
CREATE POLICY "Tenants are viewable by authenticated users" ON tenants
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Tenants are insertable by authenticated users" ON tenants
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Tenants are updatable by owner" ON tenants
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Políticas para users
CREATE POLICY "Users can view own tenant data" ON users
    FOR SELECT USING (
        tenant_id IN (
            SELECT id FROM tenants WHERE id = tenant_id
        )
    );

CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Admins can manage tenant users" ON users
    FOR ALL USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Políticas para agents
CREATE POLICY "Agents are viewable by tenant" ON agents
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Agents are manageable by tenant admin" ON agents
    FOR ALL USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Políticas para chat_history
CREATE POLICY "Chat history is viewable by tenant" ON chat_history
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Chat history is insertable by tenant users" ON chat_history
    FOR INSERT WITH CHECK (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

-- Políticas para events
CREATE POLICY "Events are viewable by tenant" ON events
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Events are insertable by authenticated users" ON events
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Events are updatable by tenant admin" ON events
    FOR UPDATE USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Políticas para webhooks
CREATE POLICY "Webhooks are viewable by tenant" ON webhooks
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Webhooks are manageable by tenant admin" ON webhooks
    FOR ALL USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Políticas para files
CREATE POLICY "Files are viewable by tenant" ON files
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Files are insertable by tenant users" ON files
    FOR INSERT WITH CHECK (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Public files are viewable by everyone" ON files
    FOR SELECT USING (is_public = true);

-- Políticas para chat_sessions
CREATE POLICY "Chat sessions are viewable by tenant" ON chat_sessions
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Chat sessions are manageable by tenant users" ON chat_sessions
    FOR ALL USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

-- Políticas para audit_logs
CREATE POLICY "Audit logs are viewable by tenant admin" ON audit_logs
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Audit logs are insertable by system" ON audit_logs
    FOR INSERT WITH CHECK (true);

-- Políticas para presence
CREATE POLICY "Presence is viewable by tenant" ON presence
    FOR SELECT USING (
        tenant_id IN (
            SELECT tenant_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Users can update own presence" ON presence
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can insert own presence" ON presence
    FOR INSERT WITH CHECK (user_id = auth.uid());

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

-- Triggers para updated_at
CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_webhooks_updated_at BEFORE UPDATE ON webhooks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Função para registrar logs de auditoria
CREATE OR REPLACE FUNCTION log_audit_event(
    p_action VARCHAR,
    p_resource_type VARCHAR DEFAULT NULL,
    p_resource_id UUID DEFAULT NULL,
    p_details JSONB DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO audit_logs (
        tenant_id,
        user_id,
        action,
        resource_type,
        resource_id,
        details,
        ip_address
    ) VALUES (
        (SELECT tenant_id FROM users WHERE id = auth.uid()),
        auth.uid(),
        p_action,
        p_resource_type,
        p_resource_id,
        p_details,
        inet_client_addr()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para obter estatísticas de chat
CREATE OR REPLACE FUNCTION get_chat_stats(
    p_tenant_id UUID,
    p_days_back INTEGER DEFAULT 30
)
RETURNS TABLE (
    total_messages BIGINT,
    avg_response_time NUMERIC,
    total_tokens BIGINT,
    active_users BIGINT,
    popular_agents JSONB,
    total_cost_usd NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as total_messages,
        AVG(response_time_ms) as avg_response_time,
        SUM(tokens_used) as total_tokens,
        COUNT(DISTINCT user_id) as active_users,
        jsonb_agg(
            jsonb_build_object(
                'agent_name', a.name,
                'message_count', COUNT(*)
            )
        ) as popular_agents,
        SUM(cost_usd) as total_cost_usd
    FROM chat_history ch
    JOIN agents a ON ch.agent_id = a.id
    WHERE ch.tenant_id = p_tenant_id
    AND ch.created_at >= NOW() - INTERVAL '1 day' * p_days_back
    GROUP BY ch.tenant_id;
END;
$$ LANGUAGE plpgsql;

-- Função para limpar eventos antigos
CREATE OR REPLACE FUNCTION cleanup_old_events(p_days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM events 
    WHERE created_at < NOW() - INTERVAL '1 day' * p_days_to_keep
    AND processed = true;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar presence
CREATE OR REPLACE FUNCTION update_presence(
    p_session_id UUID,
    p_status VARCHAR DEFAULT 'online'
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO presence (tenant_id, user_id, session_id, status)
    VALUES (
        (SELECT tenant_id FROM users WHERE id = auth.uid()),
        auth.uid(),
        p_session_id,
        p_status
    )
    ON CONFLICT (user_id, session_id) 
    DO UPDATE SET 
        status = EXCLUDED.status,
        last_seen = NOW(),
        metadata = EXCLUDED.metadata;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- VIEWS ÚTEIS
-- =============================================================================

-- View para estatísticas de chat
CREATE OR REPLACE VIEW chat_stats_view AS
SELECT 
    t.name as tenant_name,
    a.name as agent_name,
    COUNT(*) as total_messages,
    AVG(ch.response_time_ms) as avg_response_time,
    SUM(ch.tokens_used) as total_tokens,
    SUM(ch.cost_usd) as total_cost_usd,
    DATE_TRUNC('day', ch.created_at) as date
FROM chat_history ch
JOIN tenants t ON ch.tenant_id = t.id
JOIN agents a ON ch.agent_id = a.id
GROUP BY t.name, a.name, DATE_TRUNC('day', ch.created_at)
ORDER BY date DESC;

-- View para eventos recentes
CREATE OR REPLACE VIEW recent_events_view AS
SELECT 
    e.event_type,
    e.timestamp,
    e.tenant_id,
    t.name as tenant_name,
    e.user_id,
    u.name as user_name,
    e.data,
    e.processed
FROM events e
JOIN tenants t ON e.tenant_id = t.id
LEFT JOIN users u ON e.user_id = u.id
WHERE e.created_at >= NOW() - INTERVAL '7 days'
ORDER BY e.timestamp DESC;

-- View para uso por tenant
CREATE OR REPLACE VIEW tenant_usage_view AS
SELECT 
    t.name as tenant_name,
    t.subscription_plan,
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT a.id) as total_agents,
    COUNT(ch.id) as total_messages,
    SUM(ch.tokens_used) as total_tokens,
    SUM(ch.cost_usd) as total_cost_usd,
    t.created_at as tenant_created_at
FROM tenants t
LEFT JOIN users u ON t.id = u.tenant_id
LEFT JOIN agents a ON t.id = a.tenant_id
LEFT JOIN chat_history ch ON t.id = ch.tenant_id
GROUP BY t.id, t.name, t.subscription_plan, t.created_at
ORDER BY total_messages DESC;

-- View para usuários online
CREATE OR REPLACE VIEW online_users_view AS
SELECT 
    p.tenant_id,
    t.name as tenant_name,
    p.user_id,
    u.name as user_name,
    u.email,
    p.status,
    p.last_seen,
    p.session_id
FROM presence p
JOIN tenants t ON p.tenant_id = t.id
JOIN users u ON p.user_id = u.id
WHERE p.last_seen > NOW() - INTERVAL '5 minutes'
ORDER BY p.last_seen DESC;

-- =============================================================================
-- DADOS INICIAIS
-- =============================================================================

-- Inserir tenant padrão
INSERT INTO tenants (id, name, domain, settings, subscription_plan) VALUES 
(
    '00000000-0000-0000-0000-000000000001',
    'n.Gabi Default',
    'ngabi.local',
    '{"theme": "default", "features": ["chat", "analytics", "webhooks"]}',
    'pro'
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
-- MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Banco de dados n.Gabi criado com sucesso!' as status; 