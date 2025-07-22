-- 📁 Configuração Storage para n.Gabi
-- Buckets e políticas para armazenamento de arquivos

-- =============================================================================
-- CRIAR BUCKETS
-- =============================================================================

-- Bucket para avatares de usuários (público)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types) 
VALUES (
    'avatars', 
    'avatars', 
    true, 
    5242880, -- 5MB
    ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/webp']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para arquivos de chat (privado)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types) 
VALUES (
    'chat-files', 
    'chat-files', 
    false, 
    10485760, -- 10MB
    ARRAY['image/*', 'application/pdf', 'text/plain', 'application/json']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para documentos (privado)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types) 
VALUES (
    'documents', 
    'documents', 
    false, 
    52428800, -- 50MB
    ARRAY['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
) ON CONFLICT (id) DO NOTHING;

-- Bucket para backups (privado)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types) 
VALUES (
    'backups', 
    'backups', 
    false, 
    1073741824, -- 1GB
    ARRAY['application/sql', 'application/zip', 'application/gzip']
) ON CONFLICT (id) DO NOTHING;

-- =============================================================================
-- POLÍTICAS DE STORAGE
-- =============================================================================

-- Políticas para avatars (público para leitura, usuário para escrita)
CREATE POLICY "Avatars are publicly accessible" ON storage.objects
FOR SELECT USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload avatars" ON storage.objects
FOR INSERT WITH CHECK (
    bucket_id = 'avatars' 
    AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update own avatars" ON storage.objects
FOR UPDATE USING (
    bucket_id = 'avatars' 
    AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own avatars" ON storage.objects
FOR DELETE USING (
    bucket_id = 'avatars' 
    AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Políticas para chat-files (privado por tenant)
CREATE POLICY "Chat files are viewable by tenant" ON storage.objects
FOR SELECT USING (
    bucket_id = 'chat-files'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

CREATE POLICY "Users can upload chat files" ON storage.objects
FOR INSERT WITH CHECK (
    bucket_id = 'chat-files'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

CREATE POLICY "Users can update chat files" ON storage.objects
FOR UPDATE USING (
    bucket_id = 'chat-files'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

CREATE POLICY "Users can delete chat files" ON storage.objects
FOR DELETE USING (
    bucket_id = 'chat-files'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

-- Políticas para documents (privado por tenant)
CREATE POLICY "Documents are viewable by tenant" ON storage.objects
FOR SELECT USING (
    bucket_id = 'documents'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

CREATE POLICY "Users can upload documents" ON storage.objects
FOR INSERT WITH CHECK (
    bucket_id = 'documents'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

CREATE POLICY "Users can update documents" ON storage.objects
FOR UPDATE USING (
    bucket_id = 'documents'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

CREATE POLICY "Users can delete documents" ON storage.objects
FOR DELETE USING (
    bucket_id = 'documents'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND tenant_id::text = (storage.foldername(name))[1]
    )
);

-- Políticas para backups (apenas admin)
CREATE POLICY "Backups are viewable by admin" ON storage.objects
FOR SELECT USING (
    bucket_id = 'backups'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND role = 'admin'
    )
);

CREATE POLICY "Admins can upload backups" ON storage.objects
FOR INSERT WITH CHECK (
    bucket_id = 'backups'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND role = 'admin'
    )
);

CREATE POLICY "Admins can delete backups" ON storage.objects
FOR DELETE USING (
    bucket_id = 'backups'
    AND EXISTS (
        SELECT 1 FROM users 
        WHERE id = auth.uid() 
        AND role = 'admin'
    )
);

-- =============================================================================
-- FUNÇÕES PARA STORAGE
-- =============================================================================

-- Função para obter URL pública de arquivo
CREATE OR REPLACE FUNCTION get_file_url(
    p_bucket_name TEXT,
    p_file_path TEXT
)
RETURNS TEXT AS $$
BEGIN
    RETURN 'https://' || current_setting('app.settings.supabase_url') || '/storage/v1/object/public/' || p_bucket_name || '/' || p_file_path;
END;
$$ LANGUAGE plpgsql;

-- Função para obter URL assinada de arquivo
CREATE OR REPLACE FUNCTION get_signed_url(
    p_bucket_name TEXT,
    p_file_path TEXT,
    p_expires_in INTEGER DEFAULT 3600
)
RETURNS TEXT AS $$
BEGIN
    -- Esta função seria implementada via Edge Function
    -- Por enquanto retorna URL pública
    RETURN get_file_url(p_bucket_name, p_file_path);
END;
$$ LANGUAGE plpgsql;

-- Função para registrar arquivo na tabela files
CREATE OR REPLACE FUNCTION register_file(
    p_bucket_name TEXT,
    p_file_path TEXT,
    p_file_name TEXT,
    p_file_size BIGINT,
    p_mime_type TEXT,
    p_is_public BOOLEAN DEFAULT false
)
RETURNS UUID AS $$
DECLARE
    file_id UUID;
BEGIN
    INSERT INTO files (
        tenant_id,
        user_id,
        bucket_name,
        file_path,
        file_name,
        file_size,
        mime_type,
        is_public
    ) VALUES (
        (SELECT tenant_id FROM users WHERE id = auth.uid()),
        auth.uid(),
        p_bucket_name,
        p_file_path,
        p_file_name,
        p_file_size,
        p_mime_type,
        p_is_public
    ) RETURNING id INTO file_id;
    
    RETURN file_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para limpar arquivos órfãos
CREATE OR REPLACE FUNCTION cleanup_orphaned_files()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Remover registros de arquivos que não existem mais no storage
    DELETE FROM files 
    WHERE id IN (
        SELECT f.id 
        FROM files f
        LEFT JOIN storage.objects o ON f.bucket_name = o.bucket_id AND f.file_path = o.name
        WHERE o.id IS NULL
    );
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- VIEWS PARA STORAGE
-- =============================================================================

-- View para arquivos por tenant
CREATE OR REPLACE VIEW tenant_files_view AS
SELECT 
    f.id,
    f.tenant_id,
    t.name as tenant_name,
    f.user_id,
    u.name as user_name,
    f.bucket_name,
    f.file_path,
    f.file_name,
    f.file_size,
    f.mime_type,
    f.is_public,
    f.created_at,
    get_file_url(f.bucket_name, f.file_path) as public_url
FROM files f
JOIN tenants t ON f.tenant_id = t.id
JOIN users u ON f.user_id = u.id
ORDER BY f.created_at DESC;

-- View para estatísticas de storage
CREATE OR REPLACE VIEW storage_stats_view AS
SELECT 
    t.name as tenant_name,
    f.bucket_name,
    COUNT(*) as total_files,
    SUM(f.file_size) as total_size_bytes,
    ROUND(SUM(f.file_size) / 1024.0 / 1024.0, 2) as total_size_mb,
    COUNT(CASE WHEN f.is_public = true THEN 1 END) as public_files,
    COUNT(CASE WHEN f.is_public = false THEN 1 END) as private_files,
    MAX(f.created_at) as last_upload
FROM files f
JOIN tenants t ON f.tenant_id = t.id
GROUP BY t.name, f.bucket_name
ORDER BY total_size_bytes DESC;

-- View para arquivos recentes
CREATE OR REPLACE VIEW recent_files_view AS
SELECT 
    f.file_name,
    f.mime_type,
    f.file_size,
    f.is_public,
    f.created_at,
    t.name as tenant_name,
    u.name as uploaded_by
FROM files f
JOIN tenants t ON f.tenant_id = t.id
JOIN users u ON f.user_id = u.id
WHERE f.created_at >= NOW() - INTERVAL '7 days'
ORDER BY f.created_at DESC;

-- =============================================================================
-- TRIGGERS PARA STORAGE
-- =============================================================================

-- Trigger para registrar arquivo automaticamente
CREATE OR REPLACE FUNCTION auto_register_file()
RETURNS TRIGGER AS $$
BEGIN
    -- Registrar arquivo na tabela files
    INSERT INTO files (
        tenant_id,
        user_id,
        bucket_name,
        file_path,
        file_name,
        file_size,
        mime_type,
        is_public
    ) VALUES (
        (SELECT tenant_id FROM users WHERE id = auth.uid()),
        auth.uid(),
        NEW.bucket_id,
        NEW.name,
        split_part(NEW.name, '/', -1),
        NEW.metadata->>'size',
        NEW.metadata->>'mimetype',
        CASE WHEN NEW.bucket_id = 'avatars' THEN true ELSE false END
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para remover registro quando arquivo é deletado
CREATE OR REPLACE FUNCTION auto_remove_file_record()
RETURNS TRIGGER AS $$
BEGIN
    -- Remover registro da tabela files
    DELETE FROM files 
    WHERE bucket_name = OLD.bucket_id 
    AND file_path = OLD.name;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- MENSAGEM DE SUCESSO
-- =============================================================================

SELECT '✅ Storage configurado com sucesso!' as status; 