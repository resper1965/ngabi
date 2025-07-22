-- 📁 Configuração Storage Completa para n.Gabi
-- Buckets e políticas para armazenamento de arquivos

-- =============================================================================
-- CRIAR BUCKETS
-- =============================================================================

-- Bucket para avatares de usuários
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'avatars', 
    'avatars', 
    true, 
    5242880, -- 5MB
    ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/webp']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para arquivos de chat
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'chat-files', 
    'chat-files', 
    false, 
    10485760, -- 10MB
    ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para documentos
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'documents', 
    'documents', 
    false, 
    52428800, -- 50MB
    ARRAY['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/plain', 'text/csv']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para backups
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'backups', 
    'backups', 
    false, 
    1073741824, -- 1GB
    ARRAY['application/zip', 'application/x-tar', 'application/gzip', 'application/x-bzip2']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para logs
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'logs', 
    'logs', 
    false, 
    10485760, -- 10MB
    ARRAY['text/plain', 'application/json', 'text/csv']
) ON CONFLICT (id) DO NOTHING;

-- =============================================================================
-- POLÍTICAS RLS PARA BUCKETS
-- =============================================================================

-- Políticas para bucket avatars
CREATE POLICY "Avatars are publicly accessible" ON storage.objects
    FOR SELECT USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload their own avatar" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'avatars' 
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can update their own avatar" ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'avatars' 
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can delete their own avatar" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'avatars' 
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

-- Políticas para bucket chat-files
CREATE POLICY "Chat files are viewable by tenant" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'chat-files' 
        AND EXISTS (
            SELECT 1 FROM users u 
            WHERE u.id = auth.uid() 
            AND u.tenant_id::text = (storage.foldername(name))[1]
        )
    );

CREATE POLICY "Users can upload chat files" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'chat-files' 
        AND EXISTS (
            SELECT 1 FROM users u 
            WHERE u.id = auth.uid() 
            AND u.tenant_id::text = (storage.foldername(name))[1]
        )
    );

CREATE POLICY "Users can update their chat files" ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'chat-files' 
        AND auth.uid()::text = (storage.foldername(name))[2]
    );

CREATE POLICY "Users can delete their chat files" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'chat-files' 
        AND auth.uid()::text = (storage.foldername(name))[2]
    );

-- Políticas para bucket documents
CREATE POLICY "Documents are viewable by tenant admin" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'documents' 
        AND EXISTS (
            SELECT 1 FROM users u 
            WHERE u.id = auth.uid() 
            AND u.role = 'admin'
            AND u.tenant_id::text = (storage.foldername(name))[1]
        )
    );

CREATE POLICY "Admins can upload documents" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'documents' 
        AND EXISTS (
            SELECT 1 FROM users u 
            WHERE u.id = auth.uid() 
            AND u.role = 'admin'
            AND u.tenant_id::text = (storage.foldername(name))[1]
        )
    );

CREATE POLICY "Admins can update documents" ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'documents' 
        AND EXISTS (
            SELECT 1 FROM users u 
            WHERE u.id = auth.uid() 
            AND u.role = 'admin'
            AND u.tenant_id::text = (storage.foldername(name))[1]
        )
    );

CREATE POLICY "Admins can delete documents" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'documents' 
        AND EXISTS (
            SELECT 1 FROM users u 
            WHERE u.id = auth.uid() 
            AND u.role = 'admin'
            AND u.tenant_id::text = (storage.foldername(name))[1]
        )
    );

-- Políticas para bucket backups
CREATE POLICY "Backups are viewable by system only" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'backups' 
        AND auth.role() = 'service_role'
    );

CREATE POLICY "System can upload backups" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'backups' 
        AND auth.role() = 'service_role'
    );

CREATE POLICY "System can delete backups" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'backups' 
        AND auth.role() = 'service_role'
    );

-- Políticas para bucket logs
CREATE POLICY "Logs are viewable by system only" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'logs' 
        AND auth.role() = 'service_role'
    );

CREATE POLICY "System can upload logs" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'logs' 
        AND auth.role() = 'service_role'
    );

-- =============================================================================
-- FUNÇÕES PARA GESTÃO DE ARQUIVOS
-- =============================================================================

-- Função para obter URL assinada de arquivo
CREATE OR REPLACE FUNCTION get_signed_url(
    p_bucket_name TEXT,
    p_file_path TEXT,
    p_expires_in INTEGER DEFAULT 3600
)
RETURNS TEXT AS $$
DECLARE
    signed_url TEXT;
BEGIN
    SELECT storage.sign(
        p_file_path,
        p_bucket_name,
        p_expires_in
    ) INTO signed_url;
    
    RETURN signed_url;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para upload de avatar
CREATE OR REPLACE FUNCTION upload_avatar(
    p_file_name TEXT,
    p_file_data BYTEA,
    p_content_type TEXT
)
RETURNS TEXT AS $$
DECLARE
    file_path TEXT;
    file_id UUID;
BEGIN
    -- Gerar caminho do arquivo
    file_path := auth.uid()::text || '/' || p_file_name;
    
    -- Inserir arquivo no storage
    INSERT INTO storage.objects (bucket_id, name, owner, metadata)
    VALUES (
        'avatars',
        file_path,
        auth.uid(),
        jsonb_build_object(
            'contentType', p_content_type,
            'size', octet_length(p_file_data)
        )
    ) RETURNING id INTO file_id;
    
    -- Atualizar avatar_url do usuário
    UPDATE users 
    SET avatar_url = storage.url('avatars', file_path)
    WHERE id = auth.uid();
    
    RETURN storage.url('avatars', file_path);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para upload de arquivo de chat
CREATE OR REPLACE FUNCTION upload_chat_file(
    p_session_id UUID,
    p_file_name TEXT,
    p_file_data BYTEA,
    p_content_type TEXT
)
RETURNS TEXT AS $$
DECLARE
    file_path TEXT;
    tenant_id UUID;
    file_id UUID;
BEGIN
    -- Obter tenant_id do usuário
    SELECT u.tenant_id INTO tenant_id
    FROM users u
    WHERE u.id = auth.uid();
    
    -- Gerar caminho do arquivo
    file_path := tenant_id::text || '/' || auth.uid()::text || '/' || p_file_name;
    
    -- Inserir arquivo no storage
    INSERT INTO storage.objects (bucket_id, name, owner, metadata)
    VALUES (
        'chat-files',
        file_path,
        auth.uid(),
        jsonb_build_object(
            'contentType', p_content_type,
            'size', octet_length(p_file_data),
            'sessionId', p_session_id
        )
    ) RETURNING id INTO file_id;
    
    -- Inserir registro na tabela files
    INSERT INTO files (tenant_id, user_id, bucket_name, file_path, file_name, file_size, mime_type)
    VALUES (
        tenant_id,
        auth.uid(),
        'chat-files',
        file_path,
        p_file_name,
        octet_length(p_file_data),
        p_content_type
    );
    
    RETURN storage.url('chat-files', file_path);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para limpar arquivos antigos
CREATE OR REPLACE FUNCTION cleanup_old_files(p_days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Deletar arquivos antigos do bucket chat-files
    DELETE FROM storage.objects 
    WHERE bucket_id = 'chat-files'
    AND created_at < NOW() - INTERVAL '1 day' * p_days_to_keep;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Deletar registros correspondentes da tabela files
    DELETE FROM files 
    WHERE bucket_name = 'chat-files'
    AND created_at < NOW() - INTERVAL '1 day' * p_days_to_keep;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Função para obter estatísticas de storage
CREATE OR REPLACE FUNCTION get_storage_stats()
RETURNS TABLE (
    bucket_name TEXT,
    total_files BIGINT,
    total_size BIGINT,
    avg_file_size NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        o.bucket_id as bucket_name,
        COUNT(*) as total_files,
        SUM((o.metadata->>'size')::BIGINT) as total_size,
        AVG((o.metadata->>'size')::NUMERIC) as avg_file_size
    FROM storage.objects o
    GROUP BY o.bucket_id
    ORDER BY total_size DESC;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- TRIGGERS PARA SINCRONIZAÇÃO
-- =============================================================================

-- Trigger para sincronizar tabela files quando arquivo é deletado do storage
CREATE OR REPLACE FUNCTION sync_files_on_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Deletar registro da tabela files quando arquivo é removido do storage
    DELETE FROM files 
    WHERE bucket_name = OLD.bucket_id 
    AND file_path = OLD.name;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER storage_files_delete_trigger
    AFTER DELETE ON storage.objects
    FOR EACH ROW
    EXECUTE FUNCTION sync_files_on_delete();

-- =============================================================================
-- VIEWS PARA STORAGE
-- =============================================================================

-- View para arquivos por tenant
CREATE OR REPLACE VIEW tenant_files_view AS
SELECT 
    f.tenant_id,
    t.name as tenant_name,
    f.bucket_name,
    f.file_name,
    f.file_size,
    f.mime_type,
    f.is_public,
    f.created_at,
    storage.url(f.bucket_name, f.file_path) as file_url
FROM files f
JOIN tenants t ON f.tenant_id = t.id
ORDER BY f.created_at DESC;

-- View para estatísticas de storage por tenant
CREATE OR REPLACE VIEW tenant_storage_stats AS
SELECT 
    f.tenant_id,
    t.name as tenant_name,
    f.bucket_name,
    COUNT(*) as file_count,
    SUM(f.file_size) as total_size,
    AVG(f.file_size) as avg_file_size,
    MAX(f.created_at) as last_upload
FROM files f
JOIN tenants t ON f.tenant_id = t.id
GROUP BY f.tenant_id, t.name, f.bucket_name
ORDER BY total_size DESC;

-- =============================================================================
-- MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Storage configurado com sucesso!' as status; 