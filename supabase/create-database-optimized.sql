-- 🗄️ Schema SQL Otimizado para n.Gabi + Supabase
-- Remove redundâncias e foca no Supabase como infraestrutura principal
-- Execute este script no SQL Editor do Supabase Dashboard

-- =============================================================================
-- EXTENSÕES NECESSÁRIAS
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_graphql";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- =============================================================================
-- TABELAS PRINCIPAIS (Simplificadas)
-- =============================================================================

-- Tabela de agentes (Foco principal do n.Gabi)
CREATE TABLE IF NOT EXISTS agents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    model VARCHAR(100) DEFAULT 'gpt-3.5-turbo',
    temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 2048,
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Histórico de chat (Simplificado)
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    chat_mode VARCHAR(50) DEFAULT 'UsoCotidiano',
    tokens_used INTEGER DEFAULT 0,
    response_time_ms INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Eventos (Complementar)
CREATE TABLE IF NOT EXISTS events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Webhooks (Complementar)
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    secret TEXT,
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- ÍNDICES PARA PERFORMANCE
-- =============================================================================

-- Índices para chat_history
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_agent_id ON chat_history(agent_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at DESC);

-- Índices para agents
CREATE INDEX IF NOT EXISTS idx_agents_created_by ON agents(created_by);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);

-- Índices para events
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_processed ON events(processed);

-- Índices para webhooks
CREATE INDEX IF NOT EXISTS idx_webhooks_event_type ON webhooks(event_type);
CREATE INDEX IF NOT EXISTS idx_webhooks_is_active ON webhooks(is_active);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) - Multi-tenancy via JWT
-- =============================================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhooks ENABLE ROW LEVEL SECURITY;

-- Políticas para agents
CREATE POLICY "Users can view their own agents" ON agents
    FOR SELECT USING (auth.uid() = created_by);

CREATE POLICY "Users can create agents" ON agents
    FOR INSERT WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update their own agents" ON agents
    FOR UPDATE USING (auth.uid() = created_by);

CREATE POLICY "Users can delete their own agents" ON agents
    FOR DELETE USING (auth.uid() = created_by);

-- Políticas para chat_history
CREATE POLICY "Users can view their own chat history" ON chat_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own chat history" ON chat_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own chat history" ON chat_history
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own chat history" ON chat_history
    FOR DELETE USING (auth.uid() = user_id);

-- Políticas para events
CREATE POLICY "Users can view their own events" ON events
    FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can insert events" ON events
    FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can update their own events" ON events
    FOR UPDATE USING (auth.uid() = user_id);

-- Políticas para webhooks
CREATE POLICY "Users can view their own webhooks" ON webhooks
    FOR SELECT USING (auth.uid() = created_by);

CREATE POLICY "Users can create webhooks" ON webhooks
    FOR INSERT WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update their own webhooks" ON webhooks
    FOR UPDATE USING (auth.uid() = created_by);

CREATE POLICY "Users can delete their own webhooks" ON webhooks
    FOR DELETE USING (auth.uid() = created_by);

-- =============================================================================
-- FUNÇÕES ÚTEIS
-- =============================================================================

-- Função para obter estatísticas de chat
CREATE OR REPLACE FUNCTION get_chat_stats(user_uuid UUID DEFAULT NULL)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_messages', COUNT(*),
        'total_agents', (SELECT COUNT(*) FROM agents WHERE created_by = COALESCE(user_uuid, auth.uid())),
        'last_message', MAX(created_at),
        'avg_response_time', AVG(response_time_ms)
    ) INTO result
    FROM chat_history
    WHERE user_id = COALESCE(user_uuid, auth.uid());
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para limpar histórico antigo
CREATE OR REPLACE FUNCTION cleanup_old_chat_history(days_to_keep INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM chat_history 
    WHERE created_at < NOW() - INTERVAL '1 day' * days_to_keep
    AND user_id = auth.uid();
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para obter agentes ativos
CREATE OR REPLACE FUNCTION get_active_agents()
RETURNS TABLE (
    id UUID,
    name VARCHAR(255),
    description TEXT,
    model VARCHAR(100),
    temperature DECIMAL(3,2),
    max_tokens INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id,
        a.name,
        a.description,
        a.model,
        a.temperature,
        a.max_tokens
    FROM agents a
    WHERE a.is_active = true 
    AND a.created_by = auth.uid()
    ORDER BY a.created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- TRIGGERS PARA AUDITORIA
-- =============================================================================

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_webhooks_updated_at
    BEFORE UPDATE ON webhooks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- VIEWS ÚTEIS
-- =============================================================================

-- View para estatísticas de uso
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id as user_id,
    u.email,
    COUNT(DISTINCT a.id) as total_agents,
    COUNT(ch.id) as total_messages,
    MAX(ch.created_at) as last_activity,
    AVG(ch.response_time_ms) as avg_response_time
FROM auth.users u
LEFT JOIN agents a ON u.id = a.created_by
LEFT JOIN chat_history ch ON u.id = ch.user_id
GROUP BY u.id, u.email;

-- View para agentes com estatísticas
CREATE OR REPLACE VIEW agent_stats AS
SELECT 
    a.id,
    a.name,
    a.model,
    a.is_active,
    COUNT(ch.id) as total_messages,
    AVG(ch.response_time_ms) as avg_response_time,
    MAX(ch.created_at) as last_used
FROM agents a
LEFT JOIN chat_history ch ON a.id = ch.agent_id
WHERE a.created_by = auth.uid()
GROUP BY a.id, a.name, a.model, a.is_active;

-- =============================================================================
-- DADOS INICIAIS (OPCIONAL)
-- =============================================================================

-- Inserir agente padrão se não existir
INSERT INTO agents (name, description, system_prompt, model, temperature, max_tokens)
VALUES (
    'n.Gabi Assistant',
    'Assistente padrão do n.Gabi',
    'Você é o n.Gabi, um assistente inteligente e útil. Responda de forma clara e concisa.',
    'gpt-3.5-turbo',
    0.7,
    2048
) ON CONFLICT DO NOTHING;

-- =============================================================================
-- COMENTÁRIOS FINAIS
-- =============================================================================

COMMENT ON TABLE agents IS 'Agentes de IA - Foco principal do n.Gabi';
COMMENT ON TABLE chat_history IS 'Histórico de conversas - Armazenamento via Supabase';
COMMENT ON TABLE events IS 'Sistema de eventos - Complementar';
COMMENT ON TABLE webhooks IS 'Webhooks - Complementar';

COMMENT ON FUNCTION get_chat_stats IS 'Obter estatísticas de chat do usuário';
COMMENT ON FUNCTION cleanup_old_chat_history IS 'Limpar histórico antigo';
COMMENT ON FUNCTION get_active_agents IS 'Obter agentes ativos do usuário';

-- =============================================================================
-- VERIFICAÇÃO FINAL
-- =============================================================================

-- Verificar se as tabelas foram criadas
SELECT 
    table_name,
    '✅ Criada' as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('agents', 'chat_history', 'events', 'webhooks');

-- Verificar se RLS está habilitado
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('agents', 'chat_history', 'events', 'webhooks'); 