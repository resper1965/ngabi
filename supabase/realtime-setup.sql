-- 🔄 Configuração Realtime Completa para n.Gabi
-- Habilitar realtime para todas as tabelas relevantes

-- =============================================================================
-- HABILITAR REALTIME PARA TABELAS
-- =============================================================================

-- Habilitar realtime para chat_history (mensagens em tempo real)
ALTER PUBLICATION supabase_realtime ADD TABLE chat_history;

-- Habilitar realtime para events (sistema de eventos)
ALTER PUBLICATION supabase_realtime ADD TABLE events;

-- Habilitar realtime para presence (usuários online)
ALTER PUBLICATION supabase_realtime ADD TABLE presence;

-- Habilitar realtime para chat_sessions (sessões ativas)
ALTER PUBLICATION supabase_realtime ADD TABLE chat_sessions;

-- Habilitar realtime para agents (configurações de agentes)
ALTER PUBLICATION supabase_realtime ADD TABLE agents;

-- Habilitar realtime para users (status de usuários)
ALTER PUBLICATION supabase_realtime ADD TABLE users;

-- =============================================================================
# FUNÇÕES PARA PRESENCE
-- =============================================================================

-- Função para inserir/atualizar presence
CREATE OR REPLACE FUNCTION handle_presence()
RETURNS TRIGGER AS $$
BEGIN
    -- Se o usuário já existe na tabela presence, atualizar
    IF EXISTS (SELECT 1 FROM presence WHERE user_id = NEW.user_id AND session_id = NEW.session_id) THEN
        UPDATE presence 
        SET 
            status = NEW.status,
            last_seen = NOW(),
            metadata = NEW.metadata
        WHERE user_id = NEW.user_id AND session_id = NEW.session_id;
        RETURN NULL;
    ELSE
        -- Se não existe, inserir novo registro
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Trigger para presence
CREATE TRIGGER presence_trigger
    BEFORE INSERT ON presence
    FOR EACH ROW
    EXECUTE FUNCTION handle_presence();

-- Função para limpar presence antiga
CREATE OR REPLACE FUNCTION cleanup_old_presence()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM presence 
    WHERE last_seen < NOW() - INTERVAL '30 minutes';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
# FUNÇÕES PARA EVENTOS EM TEMPO REAL
-- =============================================================================

-- Função para emitir eventos de chat
CREATE OR REPLACE FUNCTION emit_chat_event()
RETURNS TRIGGER AS $$
BEGIN
    -- Emitir evento quando nova mensagem é inserida
    IF TG_OP = 'INSERT' THEN
        PERFORM pg_notify(
            'chat_message',
            json_build_object(
                'tenant_id', NEW.tenant_id,
                'user_id', NEW.user_id,
                'agent_id', NEW.agent_id,
                'session_id', NEW.session_id,
                'message', NEW.message,
                'response', NEW.response,
                'timestamp', NEW.created_at
            )::text
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para eventos de chat
CREATE TRIGGER chat_event_trigger
    AFTER INSERT ON chat_history
    FOR EACH ROW
    EXECUTE FUNCTION emit_chat_event();

-- Função para emitir eventos de presence
CREATE OR REPLACE FUNCTION emit_presence_event()
RETURNS TRIGGER AS $$
BEGIN
    -- Emitir evento quando presence é atualizada
    PERFORM pg_notify(
        'user_presence',
        json_build_object(
            'tenant_id', NEW.tenant_id,
            'user_id', NEW.user_id,
            'status', NEW.status,
            'last_seen', NEW.last_seen
        )::text
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para eventos de presence
CREATE TRIGGER presence_event_trigger
    AFTER INSERT OR UPDATE ON presence
    FOR EACH ROW
    EXECUTE FUNCTION emit_presence_event();

-- =============================================================================
# VIEWS PARA REALTIME
-- =============================================================================

-- View para usuários online por tenant
CREATE OR REPLACE VIEW online_users_realtime AS
SELECT 
    p.tenant_id,
    t.name as tenant_name,
    p.user_id,
    u.name as user_name,
    u.email,
    u.avatar_url,
    p.status,
    p.last_seen,
    p.session_id,
    EXTRACT(EPOCH FROM (NOW() - p.last_seen)) as seconds_ago
FROM presence p
JOIN tenants t ON p.tenant_id = t.id
JOIN users u ON p.user_id = u.id
WHERE p.last_seen > NOW() - INTERVAL '5 minutes'
ORDER BY p.last_seen DESC;

-- View para estatísticas em tempo real
CREATE OR REPLACE VIEW realtime_stats AS
SELECT 
    t.id as tenant_id,
    t.name as tenant_name,
    COUNT(DISTINCT p.user_id) as online_users,
    COUNT(ch.id) as messages_today,
    AVG(ch.response_time_ms) as avg_response_time,
    SUM(ch.tokens_used) as total_tokens_today
FROM tenants t
LEFT JOIN presence p ON t.id = p.tenant_id AND p.last_seen > NOW() - INTERVAL '5 minutes'
LEFT JOIN chat_history ch ON t.id = ch.tenant_id AND ch.created_at >= DATE_TRUNC('day', NOW())
GROUP BY t.id, t.name;

-- =============================================================================
# FUNÇÕES PARA BROADCAST
-- =============================================================================

-- Função para broadcast de mensagem para tenant
CREATE OR REPLACE FUNCTION broadcast_to_tenant(
    p_tenant_id UUID,
    p_event_type VARCHAR,
    p_data JSONB
)
RETURNS VOID AS $$
BEGIN
    PERFORM pg_notify(
        'tenant_broadcast',
        json_build_object(
            'tenant_id', p_tenant_id,
            'event_type', p_event_type,
            'data', p_data,
            'timestamp', NOW()
        )::text
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para broadcast global
CREATE OR REPLACE FUNCTION broadcast_global(
    p_event_type VARCHAR,
    p_data JSONB
)
RETURNS VOID AS $$
BEGIN
    PERFORM pg_notify(
        'global_broadcast',
        json_build_object(
            'event_type', p_event_type,
            'data', p_data,
            'timestamp', NOW()
        )::text
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
-- =============================================================================

-- Configurar WAL para realtime
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;

-- Configurar para melhor performance de realtime
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements,pg_graphql';

-- =============================================================================
# FUNÇÕES DE UTILIDADE
-- =============================================================================

-- Função para obter canais de realtime ativos
CREATE OR REPLACE FUNCTION get_active_channels()
RETURNS TABLE (
    channel_name VARCHAR,
    listener_count INTEGER,
    last_activity TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'chat_message' as channel_name,
        COUNT(*) as listener_count,
        MAX(p.last_seen) as last_activity
    FROM presence p
    WHERE p.last_seen > NOW() - INTERVAL '5 minutes'
    UNION ALL
    SELECT 
        'user_presence' as channel_name,
        COUNT(*) as listener_count,
        MAX(p.last_seen) as last_activity
    FROM presence p
    WHERE p.last_seen > NOW() - INTERVAL '5 minutes';
END;
$$ LANGUAGE plpgsql;

-- Função para monitorar performance do realtime
CREATE OR REPLACE FUNCTION monitor_realtime_performance()
RETURNS TABLE (
    metric_name VARCHAR,
    metric_value NUMERIC,
    description TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'active_connections' as metric_name,
        COUNT(*)::NUMERIC as metric_value,
        'Conexões ativas de realtime' as description
    FROM presence p
    WHERE p.last_seen > NOW() - INTERVAL '5 minutes'
    UNION ALL
    SELECT 
        'messages_per_minute' as metric_name,
        COUNT(*)::NUMERIC as metric_value,
        'Mensagens por minuto' as description
    FROM chat_history ch
    WHERE ch.created_at > NOW() - INTERVAL '1 minute'
    UNION ALL
    SELECT 
        'avg_response_time' as metric_name,
        AVG(ch.response_time_ms) as metric_value,
        'Tempo médio de resposta (ms)' as description
    FROM chat_history ch
    WHERE ch.created_at > NOW() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
# MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Realtime configurado com sucesso!' as status; 