-- 🔄 Configuração Realtime para n.Gabi
-- Habilitar realtime para todas as tabelas relevantes

-- =============================================================================
-- HABILITAR REALTIME
-- =============================================================================

-- Habilitar realtime para chat_history
ALTER PUBLICATION supabase_realtime ADD TABLE chat_history;

-- Habilitar realtime para events
ALTER PUBLICATION supabase_realtime ADD TABLE events;

-- Habilitar realtime para users
ALTER PUBLICATION supabase_realtime ADD TABLE users;

-- Habilitar realtime para agents
ALTER PUBLICATION supabase_realtime ADD TABLE agents;

-- Habilitar realtime para chat_sessions
ALTER PUBLICATION supabase_realtime ADD TABLE chat_sessions;

-- Habilitar realtime para webhooks
ALTER PUBLICATION supabase_realtime ADD TABLE webhooks;

-- =============================================================================
-- CONFIGURAÇÃO DE PRESENCE
-- =============================================================================

-- Criar tabela de presence para chat
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

-- Índices para presence
CREATE INDEX IF NOT EXISTS idx_presence_tenant_id ON presence(tenant_id);
CREATE INDEX IF NOT EXISTS idx_presence_user_id ON presence(user_id);
CREATE INDEX IF NOT EXISTS idx_presence_session_id ON presence(session_id);
CREATE INDEX IF NOT EXISTS idx_presence_status ON presence(status);
CREATE INDEX IF NOT EXISTS idx_presence_last_seen ON presence(last_seen);

-- RLS para presence
ALTER TABLE presence ENABLE ROW LEVEL SECURITY;

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
-- FUNÇÕES PARA PRESENCE
-- =============================================================================

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

-- Função para limpar presence antiga
CREATE OR REPLACE FUNCTION cleanup_old_presence()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM presence 
    WHERE last_seen < NOW() - INTERVAL '5 minutes';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- TRIGGERS PARA REALTIME
-- =============================================================================

-- Trigger para atualizar last_login quando usuário faz login
CREATE OR REPLACE FUNCTION update_last_login()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users 
    SET last_login = NOW() 
    WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_last_login
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION update_last_login();

-- Trigger para emitir evento quando chat_history é inserido
CREATE OR REPLACE FUNCTION emit_chat_event()
RETURNS TRIGGER AS $$
BEGIN
    -- Inserir evento de chat
    INSERT INTO events (event_type, tenant_id, user_id, data)
    VALUES (
        'chat_message',
        NEW.tenant_id,
        NEW.user_id,
        jsonb_build_object(
            'message_id', NEW.id,
            'agent_id', NEW.agent_id,
            'session_id', NEW.session_id,
            'chat_mode', NEW.chat_mode,
            'response_time_ms', NEW.response_time_ms,
            'tokens_used', NEW.tokens_used
        )
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_emit_chat_event
    AFTER INSERT ON chat_history
    FOR EACH ROW
    EXECUTE FUNCTION emit_chat_event();

-- =============================================================================
-- VIEWS PARA REALTIME
-- =============================================================================

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

-- View para estatísticas de presence
CREATE OR REPLACE VIEW presence_stats_view AS
SELECT 
    t.name as tenant_name,
    COUNT(CASE WHEN p.status = 'online' THEN 1 END) as online_users,
    COUNT(CASE WHEN p.status = 'away' THEN 1 END) as away_users,
    COUNT(*) as total_active_users,
    MAX(p.last_seen) as last_activity
FROM presence p
JOIN tenants t ON p.tenant_id = t.id
WHERE p.last_seen > NOW() - INTERVAL '1 hour'
GROUP BY t.id, t.name
ORDER BY online_users DESC;

-- =============================================================================
-- CONFIGURAÇÃO DE CANAIS
-- =============================================================================

-- Função para obter canais de realtime por tenant
CREATE OR REPLACE FUNCTION get_realtime_channels(p_tenant_id UUID)
RETURNS TABLE (
    channel_name TEXT,
    table_name TEXT,
    event_types TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'chat_' || p_tenant_id::text as channel_name,
        'chat_history' as table_name,
        ARRAY['INSERT', 'UPDATE'] as event_types
    UNION ALL
    SELECT 
        'events_' || p_tenant_id::text as channel_name,
        'events' as table_name,
        ARRAY['INSERT', 'UPDATE'] as event_types
    UNION ALL
    SELECT 
        'presence_' || p_tenant_id::text as channel_name,
        'presence' as table_name,
        ARRAY['INSERT', 'UPDATE', 'DELETE'] as event_types;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Realtime configurado com sucesso!' as status; 