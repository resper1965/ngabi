#!/bin/bash

# Script para configurar Supabase via CLI
# n.Gabi - Python 3.13 Migration

set -e

echo "🗄️ Configurando Supabase via CLI..."

# Verificar se Supabase CLI está instalado
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI não encontrado"
    echo "📦 Instale com: npm install -g supabase"
    echo "🔗 Ou acesse: https://supabase.com/docs/guides/cli"
    exit 1
fi

# Carregar variáveis de ambiente
source .env

# Verificar se as variáveis estão definidas
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Erro: SUPABASE_URL e SUPABASE_ANON_KEY devem estar definidos no .env"
    exit 1
fi

echo "🔗 Conectando ao projeto Supabase..."

# Tentar executar o SQL via CLI
supabase db push --db-url "$SUPABASE_URL" || {
    echo "⚠️ CLI não conseguiu conectar, execute manualmente:"
    echo ""
    echo "🔗 Acesse: https://supabase.com/dashboard/project/$(echo $SUPABASE_URL | cut -d'/' -f4)"
    echo "📋 Use o SQL em: supabase/setup-tables-manual.md"
}

echo "✅ Script concluído!" 