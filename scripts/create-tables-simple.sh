#!/bin/bash

# Script simples para criar tabelas básicas no Supabase
# n.Gabi - Python 3.13 Migration

set -e

echo "🗄️ Criando tabelas básicas no Supabase..."

# Carregar variáveis de ambiente
source .env

# Verificar se as variáveis estão definidas
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Erro: SUPABASE_URL e SUPABASE_ANON_KEY devem estar definidos no .env"
    exit 1
fi

# SQL básico para criar tabelas essenciais
SQL_BASIC="
-- Extensões básicas
CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";

-- Tabela de agentes (essencial)
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

-- Histórico de chat (essencial)
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

-- Habilitar RLS
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Políticas básicas para agents
CREATE POLICY \"Users can view their own agents\" ON agents
    FOR SELECT USING (auth.uid() = created_by);

CREATE POLICY \"Users can create agents\" ON agents
    FOR INSERT WITH CHECK (auth.uid() = created_by);

-- Políticas básicas para chat_history
CREATE POLICY \"Users can view their own chat history\" ON chat_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY \"Users can insert their own chat history\" ON chat_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);
"

echo "📝 Executando SQL básico..."

# Tentar executar via API (pode não funcionar, mas vale tentar)
echo "$SQL_BASIC" | curl -X POST \
    -H "apikey: $SUPABASE_ANON_KEY" \
    -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
    -H "Content-Type: application/json" \
    -H "Prefer: return=minimal" \
    -d "{\"query\": \"$SQL_BASIC\"}" \
    "$SUPABASE_URL/rest/v1/rpc/exec_sql" || {
    echo "⚠️ API não suportada, execute manualmente no SQL Editor:"
    echo ""
    echo "🔗 Acesse: https://supabase.com/dashboard/project/$(echo $SUPABASE_URL | cut -d'/' -f4)"
    echo "📋 Copie e cole o SQL abaixo no SQL Editor:"
    echo ""
    echo "$SQL_BASIC"
}

echo "✅ Script concluído!"
echo "📋 Se as tabelas não foram criadas, execute o SQL manualmente no Supabase Dashboard" 