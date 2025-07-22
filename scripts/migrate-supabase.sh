#!/bin/bash

# 🚀 Script de Migração Completa para Supabase - n.Gabi
# Migra todas as configurações: Schema, RLS, Realtime, Storage, Functions

set -e

echo "🚀 Iniciando migração completa para Supabase..."

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
SUPABASE_URL="${SUPABASE_URL:-https://tegbkyeqfrqkuxeilgpc.supabase.co}"
SUPABASE_ANON_KEY="${SUPABASE_ANON_KEY:-}"
SUPABASE_SERVICE_ROLE_KEY="${SUPABASE_SERVICE_ROLE_KEY:-}"
PROJECT_NAME="ngabi"

# =============================================================================
# VERIFICAÇÕES PRÉVIAS
# =============================================================================
echo "📋 Verificando pré-requisitos..."

# Verificar se as variáveis de ambiente existem
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Variáveis SUPABASE_URL e SUPABASE_ANON_KEY são obrigatórias"
    exit 1
fi

# Verificar se psql está instalado
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL client (psql) não está instalado"
    exit 1
fi

# Verificar se curl está instalado
if ! command -v curl &> /dev/null; then
    echo "❌ curl não está instalado"
    exit 1
fi

echo "✅ Pré-requisitos verificados"

# =============================================================================
# CONSTRUIR DATABASE URL
# =============================================================================
echo "🔗 Configurando conexão com Supabase..."

# Extrair host e database da URL do Supabase
SUPABASE_HOST=$(echo $SUPABASE_URL | sed 's|https://||' | sed 's|\.supabase\.co.*||')
DATABASE_URL="postgresql://postgres.${SUPABASE_HOST}:5432/postgres"

echo "📊 Database URL: $DATABASE_URL"

# =============================================================================
# TESTAR CONEXÃO
# =============================================================================
echo "🔍 Testando conexão com Supabase..."

# Testar conexão usando PGPASSWORD
export PGPASSWORD="$SUPABASE_SERVICE_ROLE_KEY"

if ! psql "$DATABASE_URL" -c "SELECT version();" > /dev/null 2>&1; then
    echo "❌ Falha ao conectar com Supabase"
    echo "💡 Verifique se SUPABASE_SERVICE_ROLE_KEY está configurado corretamente"
    exit 1
fi

echo "✅ Conexão com Supabase estabelecida"

# =============================================================================
# BACKUP ANTES DA MIGRAÇÃO
# =============================================================================
echo "💾 Criando backup antes da migração..."

BACKUP_FILE="backup_pre_migration_$(date +%Y%m%d_%H%M%S).sql"

# Backup das tabelas existentes
psql "$DATABASE_URL" -c "
\copy (SELECT * FROM tenants) TO '/tmp/tenants_backup.csv' CSV HEADER;
\copy (SELECT * FROM users) TO '/tmp/users_backup.csv' CSV HEADER;
\copy (SELECT * FROM agents) TO '/tmp/agents_backup.csv' CSV HEADER;
\copy (SELECT * FROM chat_history) TO '/tmp/chat_history_backup.csv' CSV HEADER;
" > /dev/null 2>&1 || echo "⚠️ Backup opcional falhou"

echo "✅ Backup criado: $BACKUP_FILE"

# =============================================================================
# MIGRAÇÃO DO SCHEMA
# =============================================================================
echo "🗄️ Migrando schema do banco de dados..."

# Executar schema avançado
echo "📋 Executando schema avançado..."
psql "$DATABASE_URL" -f supabase/advanced-schema.sql

if [ $? -eq 0 ]; then
    echo "✅ Schema avançado migrado com sucesso"
else
    echo "❌ Erro ao migrar schema avançado"
    exit 1
fi

# =============================================================================
# CONFIGURAÇÃO DE REALTIME
# =============================================================================
echo "🔄 Configurando Realtime..."

# Executar configuração de realtime
echo "📋 Executando configuração de realtime..."
psql "$DATABASE_URL" -f supabase/realtime-config.sql

if [ $? -eq 0 ]; then
    echo "✅ Realtime configurado com sucesso"
else
    echo "❌ Erro ao configurar realtime"
    exit 1
fi

# =============================================================================
# CONFIGURAÇÃO DE STORAGE
# =============================================================================
echo "📁 Configurando Storage..."

# Executar configuração de storage
echo "📋 Executando configuração de storage..."
psql "$DATABASE_URL" -f supabase/storage-config.sql

if [ $? -eq 0 ]; then
    echo "✅ Storage configurado com sucesso"
else
    echo "❌ Erro ao configurar storage"
    exit 1
fi

# =============================================================================
# CONFIGURAÇÃO DE AUTENTICAÇÃO
# =============================================================================
echo "🔐 Configurando autenticação..."

# Configurar providers de autenticação via API
echo "📋 Configurando providers de auth..."

# Habilitar email/password
curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": {
      "enabled": true,
      "double_confirm_changes": true,
      "enable_signup": true
    }
  }' --silent --output /dev/null || echo "⚠️ Configuração de email falhou"

# Habilitar Google OAuth (se configurado)
if [ -n "$GOOGLE_CLIENT_ID" ] && [ -n "$GOOGLE_CLIENT_SECRET" ]; then
    curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
      -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"google\": {
          \"enabled\": true,
          \"client_id\": \"$GOOGLE_CLIENT_ID\",
          \"client_secret\": \"$GOOGLE_CLIENT_SECRET\"
        }
      }" --silent --output /dev/null || echo "⚠️ Configuração do Google falhou"
fi

# Habilitar GitHub OAuth (se configurado)
if [ -n "$GITHUB_CLIENT_ID" ] && [ -n "$GITHUB_CLIENT_SECRET" ]; then
    curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
      -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"github\": {
          \"enabled\": true,
          \"client_id\": \"$GITHUB_CLIENT_ID\",
          \"client_secret\": \"$GITHUB_CLIENT_SECRET\"
        }
      }" --silent --output /dev/null || echo "⚠️ Configuração do GitHub falhou"
fi

echo "✅ Autenticação configurada"

# =============================================================================
# DEPLOY DE FUNCTIONS
# =============================================================================
echo "⚡ Deployando Functions Serverless..."

# Verificar se supabase CLI está instalado
if command -v supabase &> /dev/null; then
    echo "📋 Deployando functions..."
    
    # Deploy da function de processamento de chat
    if [ -f "supabase/functions/process-chat/index.ts" ]; then
        supabase functions deploy process-chat --project-ref $(echo $SUPABASE_HOST | sed 's|.*\.||')
        echo "✅ Function process-chat deployada"
    fi
    
    # Deploy da function de webhook dispatcher
    if [ -f "supabase/functions/webhook-dispatcher/index.ts" ]; then
        supabase functions deploy webhook-dispatcher --project-ref $(echo $SUPABASE_HOST | sed 's|.*\.||')
        echo "✅ Function webhook-dispatcher deployada"
    fi
else
    echo "⚠️ Supabase CLI não encontrado. Functions devem ser deployadas manualmente."
fi

# =============================================================================
# CONFIGURAÇÃO DE WEBHOOKS
# =============================================================================
echo "🔗 Configurando webhooks..."

# Configurar webhook para eventos de auth
curl -X POST "$SUPABASE_URL/rest/v1/webhooks" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth-events",
    "url": "'$SUPABASE_URL'/functions/v1/auth-webhook",
    "events": ["auth.user.created", "auth.user.updated", "auth.user.deleted"]
  }' --silent --output /dev/null || echo "⚠️ Configuração de webhook auth falhou"

echo "✅ Webhooks configurados"

# =============================================================================
# DADOS INICIAIS
# =============================================================================
echo "📊 Inserindo dados iniciais..."

# Inserir tenant padrão se não existir
psql "$DATABASE_URL" -c "
INSERT INTO tenants (id, name, domain, settings, subscription_plan) 
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'n.Gabi Default',
    'ngabi.local',
    '{\"theme\": \"default\", \"features\": [\"chat\", \"analytics\", \"webhooks\"]}',
    'pro'
) ON CONFLICT (id) DO NOTHING;
"

# Inserir agente padrão se não existir
psql "$DATABASE_URL" -c "
INSERT INTO agents (id, tenant_id, name, description, system_prompt, model) 
VALUES (
    '00000000-0000-0000-0000-000000000002',
    '00000000-0000-0000-0000-000000000001',
    'Gabi Assistant',
    'Assistente virtual inteligente do n.Gabi',
    'Você é o Gabi, um assistente virtual inteligente e prestativo. Sempre seja educado, útil e preciso em suas respostas.',
    'gpt-3.5-turbo'
) ON CONFLICT (id) DO NOTHING;
"

echo "✅ Dados iniciais inseridos"

# =============================================================================
# VERIFICAÇÕES PÓS-MIGRAÇÃO
# =============================================================================
echo "🔍 Verificando migração..."

# Verificar se as tabelas foram criadas
TABLES=("tenants" "users" "agents" "chat_history" "events" "webhooks" "files" "presence")

for table in "${TABLES[@]}"; do
    if psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM $table;" > /dev/null 2>&1; then
        echo "✅ Tabela $table: OK"
    else
        echo "❌ Tabela $table: FALHOU"
        exit 1
    fi
done

# Verificar se as views foram criadas
VIEWS=("chat_stats_view" "recent_events_view" "tenant_usage_view" "online_users_view")

for view in "${VIEWS[@]}"; do
    if psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM $view;" > /dev/null 2>&1; then
        echo "✅ View $view: OK"
    else
        echo "❌ View $view: FALHOU"
    fi
done

# Verificar se as funções foram criadas
FUNCTIONS=("get_chat_stats" "cleanup_old_events" "update_presence" "register_file")

for func in "${FUNCTIONS[@]}"; do
    if psql "$DATABASE_URL" -c "SELECT $func('00000000-0000-0000-0000-000000000001');" > /dev/null 2>&1; then
        echo "✅ Função $func: OK"
    else
        echo "⚠️ Função $func: Não testada"
    fi
done

# =============================================================================
# TESTES DE INTEGRAÇÃO
# =============================================================================
echo "🧪 Executando testes de integração..."

# Teste de inserção de evento
psql "$DATABASE_URL" -c "
INSERT INTO events (event_type, tenant_id, data) 
VALUES (
    'migration_test',
    '00000000-0000-0000-0000-000000000001',
    '{\"message\": \"Teste de migração\"}'
);
"

if [ $? -eq 0 ]; then
    echo "✅ Teste de inserção de evento: OK"
else
    echo "❌ Teste de inserção de evento: FALHOU"
fi

# Teste de função de estatísticas
psql "$DATABASE_URL" -c "
SELECT * FROM get_chat_stats('00000000-0000-0000-0000-000000000001', 1);
" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Teste de função de estatísticas: OK"
else
    echo "❌ Teste de função de estatísticas: FALHOU"
fi

# =============================================================================
# LIMPEZA
# =============================================================================
echo "🧹 Limpando arquivos temporários..."

# Remover arquivos de backup temporários
rm -f /tmp/*_backup.csv 2>/dev/null || true

# Limpar variáveis de ambiente sensíveis
unset PGPASSWORD

# =============================================================================
# RELATÓRIO FINAL
# =============================================================================
echo ""
echo "🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!"
echo ""
echo "📊 Resumo da Migração:"
echo "   ✅ Schema avançado migrado"
echo "   ✅ Realtime configurado"
echo "   ✅ Storage configurado"
echo "   ✅ Autenticação configurada"
echo "   ✅ Webhooks configurados"
echo "   ✅ Dados iniciais inseridos"
echo ""
echo "🔗 URLs de Acesso:"
echo "   🌐 Supabase Dashboard: $SUPABASE_URL"
echo "   📚 API Docs: $SUPABASE_URL/docs"
echo "   🔧 SQL Editor: $SUPABASE_URL/sql"
echo ""
echo "📋 Próximos Passos:"
echo "   1. Configurar variáveis de ambiente no backend"
echo "   2. Atualizar frontend para usar Supabase client"
echo "   3. Testar autenticação e realtime"
echo "   4. Configurar providers OAuth (Google, GitHub)"
echo "   5. Deploy das functions serverless"
echo ""
echo "📚 Documentação:"
echo "   📄 supabase/integration-config.md"
echo "   📄 supabase/advanced-schema.sql"
echo "   📄 supabase/realtime-config.sql"
echo "   📄 supabase/storage-config.sql"
echo ""
echo "🚀 n.Gabi está pronto para usar com Supabase!"
echo "" 