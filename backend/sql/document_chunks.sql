-- =============================================================================
-- DDL para tabela document_chunks com suporte a vetores (pgvector)
-- =============================================================================

-- Habilitar extensão pgvector se não estiver habilitada
CREATE EXTENSION IF NOT EXISTS vector;

-- =============================================================================
-- TABELA: document_chunks
-- =============================================================================
CREATE TABLE document_chunks (
    -- Identificação
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    
    -- Metadados do documento
    document_id UUID NOT NULL,
    chunk_index INTEGER NOT NULL, -- índice do chunk no documento
    chunk_size INTEGER NOT NULL, -- tamanho do chunk em caracteres
    
    -- Conteúdo e processamento
    content TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL, -- hash SHA-256 do conteúdo
    embedding vector(1536), -- vetor de embedding (dimensão padrão OpenAI)
    
    -- Metadados da fonte
    source_type VARCHAR(50) NOT NULL, -- 'livro', 'processo', 'jurisprudencia', 'manual', etc.
    source_id VARCHAR(255) NOT NULL, -- ID da fonte original
    source_name VARCHAR(500) NOT NULL, -- nome/título da fonte
    source_path TEXT, -- caminho do arquivo (se aplicável)
    
    -- Metadados de processamento
    processing_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    processing_error TEXT, -- mensagem de erro se falhou
    embedding_model VARCHAR(100), -- modelo usado para embedding (ex: 'text-embedding-ada-002')
    
    -- Metadados temporais
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE, -- quando o embedding foi gerado
    
    -- Constraints
    CONSTRAINT fk_document_chunks_tenant 
        FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    
    CONSTRAINT uk_document_chunks_unique 
        UNIQUE (tenant_id, document_id, chunk_index),
    
    CONSTRAINT chk_document_chunks_chunk_size 
        CHECK (chunk_size > 0 AND chunk_size <= 10000),
    
    CONSTRAINT chk_document_chunks_source_type 
        CHECK (source_type IN ('livro', 'processo', 'jurisprudencia', 'manual', 'faq', 'legislacao', 'doutrina', 'outro')),
    
    CONSTRAINT chk_document_chunks_processing_status 
        CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed'))
);

-- =============================================================================
-- ÍNDICES PRINCIPAIS
-- =============================================================================

-- Índice composto para tenant_id + source_type (mais usado em consultas)
CREATE INDEX idx_document_chunks_tenant_source 
    ON document_chunks (tenant_id, source_type);

-- Índice para tenant_id (isolamento por tenant)
CREATE INDEX idx_document_chunks_tenant_id 
    ON document_chunks (tenant_id);

-- Índice para source_type (filtros por tipo de fonte)
CREATE INDEX idx_document_chunks_source_type 
    ON document_chunks (source_type);

-- Índice para document_id (busca por documento específico)
CREATE INDEX idx_document_chunks_document_id 
    ON document_chunks (document_id);

-- Índice para processing_status (monitoramento de processamento)
CREATE INDEX idx_document_chunks_processing_status 
    ON document_chunks (processing_status);

-- Índice para created_at (ordenação temporal)
CREATE INDEX idx_document_chunks_created_at 
    ON document_chunks (created_at);

-- Índice para content_hash (detecção de duplicatas)
CREATE INDEX idx_document_chunks_content_hash 
    ON document_chunks (content_hash);

-- =============================================================================
-- ÍNDICES DE VETOR (pgvector)
-- =============================================================================

-- Índice HNSW para busca por similaridade de embedding
-- HNSW é mais rápido para consultas, mas usa mais espaço
CREATE INDEX idx_document_chunks_embedding_hnsw 
    ON document_chunks 
    USING hnsw (embedding vector_cosine_ops)
    WHERE embedding IS NOT NULL;

-- Índice IVFFlat para busca por similaridade (alternativa)
-- IVFFlat é mais compacto, mas pode ser mais lento
-- CREATE INDEX idx_document_chunks_embedding_ivfflat 
--     ON document_chunks 
--     USING ivfflat (embedding vector_cosine_ops)
--     WITH (lists = 100)
--     WHERE embedding IS NOT NULL;

-- =============================================================================
-- ÍNDICES COMPOSTOS ESPECIALIZADOS
-- =============================================================================

-- Índice para busca por tenant + source_type + status
CREATE INDEX idx_document_chunks_tenant_source_status 
    ON document_chunks (tenant_id, source_type, processing_status);

-- Índice para busca por tenant + document_id + chunk_index
CREATE INDEX idx_document_chunks_tenant_document_chunk 
    ON document_chunks (tenant_id, document_id, chunk_index);

-- Índice para busca por tenant + source_type + created_at
CREATE INDEX idx_document_chunks_tenant_source_created 
    ON document_chunks (tenant_id, source_type, created_at);

-- =============================================================================
-- ÍNDICES PARCIAIS (para otimização)
-- =============================================================================

-- Índice apenas para chunks processados (mais usados em busca)
CREATE INDEX idx_document_chunks_processed 
    ON document_chunks (tenant_id, source_type, embedding)
    WHERE processing_status = 'completed' AND embedding IS NOT NULL;

-- Índice para chunks pendentes de processamento
CREATE INDEX idx_document_chunks_pending 
    ON document_chunks (tenant_id, processing_status, created_at)
    WHERE processing_status IN ('pending', 'processing');

-- =============================================================================
-- TRIGGERS E FUNÇÕES
-- =============================================================================

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_document_chunks_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para atualizar updated_at
CREATE TRIGGER trigger_document_chunks_updated_at
    BEFORE UPDATE ON document_chunks
    FOR EACH ROW
    EXECUTE FUNCTION update_document_chunks_updated_at();

-- Função para calcular hash do conteúdo automaticamente
CREATE OR REPLACE FUNCTION calculate_content_hash()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular hash SHA-256 do conteúdo
    NEW.content_hash = encode(sha256(NEW.content::bytea), 'hex');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular hash do conteúdo
CREATE TRIGGER trigger_document_chunks_content_hash
    BEFORE INSERT OR UPDATE OF content ON document_chunks
    FOR EACH ROW
    EXECUTE FUNCTION calculate_content_hash();

-- =============================================================================
-- FUNÇÕES DE BUSCA POR SIMILARIDADE
-- =============================================================================

-- Função para buscar chunks similares por tenant
CREATE OR REPLACE FUNCTION search_similar_chunks(
    p_tenant_id UUID,
    p_embedding vector(1536),
    p_limit INTEGER DEFAULT 10,
    p_threshold REAL DEFAULT 0.7
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    source_type VARCHAR(50),
    source_name VARCHAR(500),
    similarity REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dc.id,
        dc.content,
        dc.source_type,
        dc.source_name,
        1 - (dc.embedding <=> p_embedding) as similarity
    FROM document_chunks dc
    WHERE dc.tenant_id = p_tenant_id
        AND dc.processing_status = 'completed'
        AND dc.embedding IS NOT NULL
        AND 1 - (dc.embedding <=> p_embedding) >= p_threshold
    ORDER BY dc.embedding <=> p_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Função para buscar chunks similares por tenant e tipo de fonte
CREATE OR REPLACE FUNCTION search_similar_chunks_by_source(
    p_tenant_id UUID,
    p_embedding vector(1536),
    p_source_type VARCHAR(50),
    p_limit INTEGER DEFAULT 10,
    p_threshold REAL DEFAULT 0.7
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    source_type VARCHAR(50),
    source_name VARCHAR(500),
    similarity REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dc.id,
        dc.content,
        dc.source_type,
        dc.source_name,
        1 - (dc.embedding <=> p_embedding) as similarity
    FROM document_chunks dc
    WHERE dc.tenant_id = p_tenant_id
        AND dc.source_type = p_source_type
        AND dc.processing_status = 'completed'
        AND dc.embedding IS NOT NULL
        AND 1 - (dc.embedding <=> p_embedding) >= p_threshold
    ORDER BY dc.embedding <=> p_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- VIEWS ÚTEIS
-- =============================================================================

-- View para estatísticas de chunks por tenant
CREATE VIEW v_document_chunks_stats AS
SELECT 
    tenant_id,
    source_type,
    processing_status,
    COUNT(*) as total_chunks,
    COUNT(embedding) as processed_chunks,
    AVG(chunk_size) as avg_chunk_size,
    MIN(created_at) as first_chunk_at,
    MAX(created_at) as last_chunk_at
FROM document_chunks
GROUP BY tenant_id, source_type, processing_status;

-- View para chunks pendentes de processamento
CREATE VIEW v_pending_chunks AS
SELECT 
    id,
    tenant_id,
    document_id,
    source_type,
    source_name,
    created_at
FROM document_chunks
WHERE processing_status IN ('pending', 'processing')
ORDER BY created_at ASC;

-- =============================================================================
-- COMENTÁRIOS
-- =============================================================================

COMMENT ON TABLE document_chunks IS 'Chunks de documentos com embeddings vetoriais para busca semântica';
COMMENT ON COLUMN document_chunks.id IS 'Identificador único do chunk';
COMMENT ON COLUMN document_chunks.tenant_id IS 'ID do tenant (isolamento multi-tenant)';
COMMENT ON COLUMN document_chunks.document_id IS 'ID do documento original';
COMMENT ON COLUMN document_chunks.chunk_index IS 'Índice sequencial do chunk no documento';
COMMENT ON COLUMN document_chunks.chunk_size IS 'Tamanho do chunk em caracteres';
COMMENT ON COLUMN document_chunks.content IS 'Conteúdo textual do chunk';
COMMENT ON COLUMN document_chunks.content_hash IS 'Hash SHA-256 do conteúdo para detecção de duplicatas';
COMMENT ON COLUMN document_chunks.embedding IS 'Vetor de embedding para busca semântica (pgvector)';
COMMENT ON COLUMN document_chunks.source_type IS 'Tipo da fonte: livro, processo, jurisprudencia, etc.';
COMMENT ON COLUMN document_chunks.source_id IS 'ID da fonte original';
COMMENT ON COLUMN document_chunks.source_name IS 'Nome/título da fonte';
COMMENT ON COLUMN document_chunks.source_path IS 'Caminho do arquivo (se aplicável)';
COMMENT ON COLUMN document_chunks.processing_status IS 'Status do processamento: pending, processing, completed, failed';
COMMENT ON COLUMN document_chunks.processing_error IS 'Mensagem de erro se o processamento falhou';
COMMENT ON COLUMN document_chunks.embedding_model IS 'Modelo usado para gerar o embedding';
COMMENT ON COLUMN document_chunks.created_at IS 'Data de criação do chunk';
COMMENT ON COLUMN document_chunks.updated_at IS 'Data da última atualização';
COMMENT ON COLUMN document_chunks.processed_at IS 'Data quando o embedding foi gerado';

COMMENT ON INDEX idx_document_chunks_tenant_source IS 'Índice composto para tenant_id + source_type (consultas mais comuns)';
COMMENT ON INDEX idx_document_chunks_embedding_hnsw IS 'Índice HNSW para busca por similaridade de embedding';
COMMENT ON INDEX idx_document_chunks_processed IS 'Índice parcial para chunks processados (otimização)';

-- =============================================================================
-- EXEMPLOS DE USO
-- =============================================================================

/*
-- Exemplo 1: Inserir um chunk
INSERT INTO document_chunks (
    tenant_id,
    document_id,
    chunk_index,
    chunk_size,
    content,
    source_type,
    source_id,
    source_name
) VALUES (
    '123e4567-e89b-12d3-a456-426614174000',
    '987fcdeb-51a2-43d1-9f12-345678901234',
    1,
    1500,
    'Este é o conteúdo do primeiro chunk do documento...',
    'livro',
    'livro-001',
    'Manual de Direito Civil'
);

-- Exemplo 2: Buscar chunks similares
SELECT * FROM search_similar_chunks(
    '123e4567-e89b-12d3-a456-426614174000',
    '[0.1, 0.2, 0.3, ...]'::vector(1536),
    5,
    0.8
);

-- Exemplo 3: Buscar por tipo de fonte
SELECT * FROM search_similar_chunks_by_source(
    '123e4567-e89b-12d3-a456-426614174000',
    '[0.1, 0.2, 0.3, ...]'::vector(1536),
    'jurisprudencia',
    10,
    0.7
);

-- Exemplo 4: Estatísticas por tenant
SELECT * FROM v_document_chunks_stats 
WHERE tenant_id = '123e4567-e89b-12d3-a456-426614174000';

-- Exemplo 5: Chunks pendentes
SELECT * FROM v_pending_chunks 
WHERE tenant_id = '123e4567-e89b-12d3-a456-426614174000';
*/ 