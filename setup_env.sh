#!/bin/bash

echo "🔧 CONFIGURANDO .ENV - n.Gabi"
echo "=============================="

# =============================================================================
# 1. VERIFICAR SE .ENV EXISTE
# =============================================================================
if [ -f "backend/.env" ]; then
    echo "✅ Arquivo .env já existe"
else
    echo "📝 Criando arquivo .env..."
    cp backend/env.example backend/.env
    echo "✅ Arquivo .env criado"
fi

# =============================================================================
# 2. CONFIGURAR VARIÁVEIS ESSENCIAIS
# =============================================================================
echo "🔧 Configurando variáveis essenciais..."

# Verificar se OPENAI_API_KEY está configurada
if grep -q "your-openai-api-key-here" backend/.env; then
    echo "⚠️ OPENAI_API_KEY precisa ser configurada"
    echo "📝 Edite backend/.env e configure sua OpenAI API key"
fi

# Verificar se SUPABASE_URL está configurada
if grep -q "your-supabase-url-here" backend/.env; then
    echo "⚠️ SUPABASE_URL precisa ser configurada"
    echo "📝 Edite backend/.env e configure sua Supabase URL"
fi

# Verificar se SUPABASE_ANON_KEY está configurada
if grep -q "your-supabase-anon-key-here" backend/.env; then
    echo "⚠️ SUPABASE_ANON_KEY precisa ser configurada"
    echo "📝 Edite backend/.env e configure sua Supabase Anon Key"
fi

# =============================================================================
# 3. TESTAR CONFIGURAÇÃO
# =============================================================================
echo "🧪 Testando configuração..."

# Carregar variáveis de ambiente
export $(cat backend/.env | grep -v '^#' | xargs)

# Testar se as variáveis estão carregadas
if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your-openai-api-key-here" ]; then
    echo "✅ OPENAI_API_KEY configurada"
else
    echo "❌ OPENAI_API_KEY não configurada"
fi

if [ -n "$SUPABASE_URL" ] && [ "$SUPABASE_URL" != "your-supabase-url-here" ]; then
    echo "✅ SUPABASE_URL configurada"
else
    echo "❌ SUPABASE_URL não configurada"
fi

if [ -n "$SUPABASE_ANON_KEY" ] && [ "$SUPABASE_ANON_KEY" != "your-supabase-anon-key-here" ]; then
    echo "✅ SUPABASE_ANON_KEY configurada"
else
    echo "❌ SUPABASE_ANON_KEY não configurada"
fi

# =============================================================================
# 4. TESTAR LLM SERVICE
# =============================================================================
echo "🤖 Testando LLM Service..."

python3 -c "
import os
import sys
sys.path.append('backend')

try:
    from app.core.llm_service import get_llm_service
    service = get_llm_service()
    print('✅ LLM Service OK - Usando .env diretamente')
except Exception as e:
    print(f'❌ Erro no LLM Service: {e}')
"

# =============================================================================
# 5. INSTRUÇÕES
# =============================================================================
echo ""
echo "📋 INSTRUÇÕES:"
echo "==============="
echo "1. Edite o arquivo backend/.env"
echo "2. Configure suas chaves de API:"
echo "   - OPENAI_API_KEY=sua-chave-aqui"
echo "   - SUPABASE_URL=sua-url-aqui"
echo "   - SUPABASE_ANON_KEY=sua-chave-aqui"
echo "3. Execute: python3 test_secrets.py"
echo "4. Execute: ./build_project.sh"
echo ""
echo "✅ Configuração concluída!" 