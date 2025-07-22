-- 🔐 Configuração Auth Completa para n.Gabi
-- Configurar providers de autenticação e políticas

-- =============================================================================
-- CONFIGURAÇÕES DE AUTH
-- =============================================================================

-- Habilitar extensões necessárias para auth
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- FUNÇÕES PARA GESTÃO DE USUÁRIOS
-- =============================================================================

-- Função para criar usuário automaticamente após signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Inserir na tabela users quando novo usuário se registra
    INSERT INTO public.users (id, email, name, tenant_id)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'name', NEW.email),
        '00000000-0000-0000-0000-000000000001' -- Tenant padrão
    );
    
    -- Registrar evento de auditoria
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, resource_id, details)
    VALUES (
        '00000000-0000-0000-0000-000000000001',
        NEW.id,
        'user_created',
        'user',
        NEW.id,
        jsonb_build_object(
            'email', NEW.email,
            'provider', NEW.raw_user_meta_data->>'provider',
            'created_at', NEW.created_at
        )
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para criar usuário automaticamente
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Função para atualizar last_login
CREATE OR REPLACE FUNCTION public.handle_user_login()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualizar last_login do usuário
    UPDATE public.users 
    SET last_login = NOW()
    WHERE id = NEW.id;
    
    -- Registrar evento de auditoria
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, resource_id, details)
    VALUES (
        (SELECT tenant_id FROM public.users WHERE id = NEW.id),
        NEW.id,
        'user_login',
        'user',
        NEW.id,
        jsonb_build_object(
            'login_time', NOW(),
            'ip_address', inet_client_addr()
        )
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para atualizar last_login
CREATE TRIGGER on_auth_user_login
    AFTER UPDATE ON auth.users
    FOR EACH ROW 
    WHEN (OLD.last_sign_in_at IS DISTINCT FROM NEW.last_sign_in_at)
    EXECUTE FUNCTION public.handle_user_login();

-- Função para deletar usuário e dados relacionados
CREATE OR REPLACE FUNCTION public.handle_user_deletion()
RETURNS TRIGGER AS $$
BEGIN
    -- Registrar evento de auditoria antes de deletar
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, resource_id, details)
    VALUES (
        (SELECT tenant_id FROM public.users WHERE id = OLD.id),
        OLD.id,
        'user_deleted',
        'user',
        OLD.id,
        jsonb_build_object(
            'deletion_time', NOW(),
            'email', OLD.email
        )
    );
    
    -- Deletar dados relacionados (cascade já faz isso automaticamente)
    -- Mas podemos adicionar lógica customizada aqui se necessário
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para deletar usuário
CREATE TRIGGER on_auth_user_deleted
    BEFORE DELETE ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_user_deletion();

-- =============================================================================
-- FUNÇÕES PARA GESTÃO DE TENANTS
-- =============================================================================

-- Função para criar tenant para novo usuário
CREATE OR REPLACE FUNCTION public.create_tenant_for_user(
    p_tenant_name TEXT,
    p_domain TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    new_tenant_id UUID;
    user_tenant_id UUID;
BEGIN
    -- Obter tenant_id do usuário atual
    SELECT tenant_id INTO user_tenant_id
    FROM public.users
    WHERE id = auth.uid();
    
    -- Se usuário já tem tenant, retornar erro
    IF user_tenant_id IS NOT NULL THEN
        RAISE EXCEPTION 'Usuário já possui um tenant';
    END IF;
    
    -- Criar novo tenant
    INSERT INTO public.tenants (name, domain, subscription_plan)
    VALUES (p_tenant_name, p_domain, 'free')
    RETURNING id INTO new_tenant_id;
    
    -- Atualizar usuário para o novo tenant
    UPDATE public.users
    SET tenant_id = new_tenant_id, role = 'admin'
    WHERE id = auth.uid();
    
    -- Registrar evento de auditoria
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, resource_id, details)
    VALUES (
        new_tenant_id,
        auth.uid(),
        'tenant_created',
        'tenant',
        new_tenant_id,
        jsonb_build_object(
            'tenant_name', p_tenant_name,
            'domain', p_domain
        )
    );
    
    RETURN new_tenant_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para convidar usuário para tenant
CREATE OR REPLACE FUNCTION public.invite_user_to_tenant(
    p_email TEXT,
    p_role TEXT DEFAULT 'user'
)
RETURNS TEXT AS $$
DECLARE
    tenant_id UUID;
    invite_token TEXT;
BEGIN
    -- Verificar se usuário atual é admin
    IF NOT EXISTS (
        SELECT 1 FROM public.users 
        WHERE id = auth.uid() AND role = 'admin'
    ) THEN
        RAISE EXCEPTION 'Apenas admins podem convidar usuários';
    END IF;
    
    -- Obter tenant_id do usuário atual
    SELECT u.tenant_id INTO tenant_id
    FROM public.users u
    WHERE u.id = auth.uid();
    
    -- Gerar token de convite
    invite_token := encode(gen_random_bytes(32), 'hex');
    
    -- Aqui você pode implementar o envio de email
    -- Por enquanto, apenas retornamos o token
    
    -- Registrar evento de auditoria
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, details)
    VALUES (
        tenant_id,
        auth.uid(),
        'user_invited',
        'user',
        jsonb_build_object(
            'invited_email', p_email,
            'role', p_role,
            'invite_token', invite_token
        )
    );
    
    RETURN invite_token;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- FUNÇÕES PARA GESTÃO DE PERMISSÕES
-- =============================================================================

-- Função para verificar permissões do usuário
CREATE OR REPLACE FUNCTION public.check_user_permission(
    p_permission TEXT,
    p_resource_type TEXT DEFAULT NULL,
    p_resource_id UUID DEFAULT NULL
)
RETURNS BOOLEAN AS $$
DECLARE
    user_role TEXT;
    user_permissions JSONB;
    tenant_id UUID;
BEGIN
    -- Obter informações do usuário
    SELECT u.role, u.permissions, u.tenant_id
    INTO user_role, user_permissions, tenant_id
    FROM public.users u
    WHERE u.id = auth.uid();
    
    -- Se usuário não existe, retornar false
    IF user_role IS NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Admins têm todas as permissões
    IF user_role = 'admin' THEN
        RETURN TRUE;
    END IF;
    
    -- Verificar permissões específicas
    IF user_permissions ? p_permission THEN
        RETURN (user_permissions->>p_permission)::BOOLEAN;
    END IF;
    
    -- Verificar permissões baseadas em role
    CASE user_role
        WHEN 'moderator' THEN
            RETURN p_permission IN ('read', 'write', 'moderate');
        WHEN 'user' THEN
            RETURN p_permission IN ('read', 'write');
        ELSE
            RETURN FALSE;
    END CASE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para atualizar permissões do usuário
CREATE OR REPLACE FUNCTION public.update_user_permissions(
    p_user_id UUID,
    p_permissions JSONB
)
RETURNS BOOLEAN AS $$
DECLARE
    current_user_role TEXT;
    target_user_tenant_id UUID;
    current_user_tenant_id UUID;
BEGIN
    -- Verificar se usuário atual é admin
    SELECT u.role, u.tenant_id
    INTO current_user_role, current_user_tenant_id
    FROM public.users u
    WHERE u.id = auth.uid();
    
    IF current_user_role != 'admin' THEN
        RAISE EXCEPTION 'Apenas admins podem atualizar permissões';
    END IF;
    
    -- Obter tenant_id do usuário alvo
    SELECT u.tenant_id
    INTO target_user_tenant_id
    FROM public.users u
    WHERE u.id = p_user_id;
    
    -- Verificar se usuários são do mesmo tenant
    IF current_user_tenant_id != target_user_tenant_id THEN
        RAISE EXCEPTION 'Usuários devem ser do mesmo tenant';
    END IF;
    
    -- Atualizar permissões
    UPDATE public.users
    SET permissions = p_permissions
    WHERE id = p_user_id;
    
    -- Registrar evento de auditoria
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, resource_id, details)
    VALUES (
        current_user_tenant_id,
        auth.uid(),
        'permissions_updated',
        'user',
        p_user_id,
        jsonb_build_object(
            'new_permissions', p_permissions
        )
    );
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- FUNÇÕES PARA SESSÕES
-- =============================================================================

-- Função para criar sessão de chat
CREATE OR REPLACE FUNCTION public.create_chat_session(
    p_agent_id UUID,
    p_title TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    session_id UUID;
    tenant_id UUID;
BEGIN
    -- Obter tenant_id do usuário
    SELECT u.tenant_id INTO tenant_id
    FROM public.users u
    WHERE u.id = auth.uid();
    
    -- Verificar se agente pertence ao tenant
    IF NOT EXISTS (
        SELECT 1 FROM public.agents a
        WHERE a.id = p_agent_id AND a.tenant_id = tenant_id
    ) THEN
        RAISE EXCEPTION 'Agente não encontrado ou não pertence ao tenant';
    END IF;
    
    -- Criar sessão
    INSERT INTO public.chat_sessions (tenant_id, user_id, agent_id, title)
    VALUES (tenant_id, auth.uid(), p_agent_id, p_title)
    RETURNING id INTO session_id;
    
    -- Registrar evento de auditoria
    INSERT INTO public.audit_logs (tenant_id, user_id, action, resource_type, resource_id, details)
    VALUES (
        tenant_id,
        auth.uid(),
        'session_created',
        'chat_session',
        session_id,
        jsonb_build_object(
            'agent_id', p_agent_id,
            'title', p_title
        )
    );
    
    RETURN session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- VIEWS PARA AUTH
-- =============================================================================

-- View para informações do usuário atual
CREATE OR REPLACE VIEW current_user_info AS
SELECT 
    u.id,
    u.email,
    u.name,
    u.avatar_url,
    u.role,
    u.permissions,
    u.tenant_id,
    t.name as tenant_name,
    t.subscription_plan,
    u.last_login,
    u.created_at
FROM public.users u
JOIN public.tenants t ON u.tenant_id = t.id
WHERE u.id = auth.uid();

-- View para usuários do tenant
CREATE OR REPLACE VIEW tenant_users AS
SELECT 
    u.id,
    u.email,
    u.name,
    u.avatar_url,
    u.role,
    u.permissions,
    u.last_login,
    u.created_at,
    u.is_active
FROM public.users u
WHERE u.tenant_id = (
    SELECT tenant_id FROM public.users WHERE id = auth.uid()
)
ORDER BY u.created_at DESC;

-- View para estatísticas de auth
CREATE OR REPLACE VIEW auth_stats AS
SELECT 
    t.name as tenant_name,
    COUNT(u.id) as total_users,
    COUNT(CASE WHEN u.last_login > NOW() - INTERVAL '7 days' THEN 1 END) as active_users_7d,
    COUNT(CASE WHEN u.last_login > NOW() - INTERVAL '30 days' THEN 1 END) as active_users_30d,
    COUNT(CASE WHEN u.role = 'admin' THEN 1 END) as admin_count,
    COUNT(CASE WHEN u.role = 'moderator' THEN 1 END) as moderator_count,
    COUNT(CASE WHEN u.role = 'user' THEN 1 END) as user_count,
    AVG(EXTRACT(EPOCH FROM (NOW() - u.last_login))/3600) as avg_hours_since_login
FROM public.tenants t
LEFT JOIN public.users u ON t.id = u.tenant_id
GROUP BY t.id, t.name
ORDER BY total_users DESC;

-- =============================================================================
-- FUNÇÕES DE UTILIDADE
-- =============================================================================

-- Função para obter estatísticas de login
CREATE OR REPLACE FUNCTION public.get_login_stats(p_days INTEGER DEFAULT 30)
RETURNS TABLE (
    date DATE,
    login_count BIGINT,
    unique_users BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE(al.created_at) as date,
        COUNT(*) as login_count,
        COUNT(DISTINCT al.user_id) as unique_users
    FROM public.audit_logs al
    WHERE al.action = 'user_login'
    AND al.created_at >= NOW() - INTERVAL '1 day' * p_days
    GROUP BY DATE(al.created_at)
    ORDER BY date DESC;
END;
$$ LANGUAGE plpgsql;

-- Função para limpar logs antigos
CREATE OR REPLACE FUNCTION public.cleanup_old_logs(p_days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM public.audit_logs 
    WHERE created_at < NOW() - INTERVAL '1 day' * p_days_to_keep;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Auth configurado com sucesso!' as status; 