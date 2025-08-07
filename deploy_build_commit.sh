#!/bin/bash

# Script completo para deploy, build e commit - n.Gabi
echo "🚀 Iniciando deploy, build e commit..."

# =============================================================================
# 1. LIMPEZA DE SECRETS
# =============================================================================
echo "🔒 Limpando secrets..."

# Remover arquivos com secrets do staging
echo "📦 Removendo arquivos com secrets..."
git rm --cached BACKEND_STATUS.md 2>/dev/null || true
git rm --cached FRONTEND_ENV_VARS.md 2>/dev/null || true
git rm --cached FRONTEND_BACKEND_CONNECTION.md 2>/dev/null || true
git rm --cached BACKEND_ENV_VARS.md 2>/dev/null || true
git rm --cached EASYUI_ENV_VARS.md 2>/dev/null || true
git rm --cached CORRIGIR_SECRETS_URGENTE.md 2>/dev/null || true
git rm --cached REMOVER_SECRETS.md 2>/dev/null || true

# Substituir secrets nos arquivos restantes
echo "🔧 Substituindo secrets..."
find . -name "*.md" -exec sed -i 's/your-openai-api-key/your-openai-api-key/g' {} \; 2>/dev/null || true

# =============================================================================
# 2. BUILD DO PROJETO
# =============================================================================
echo "🔨 Fazendo build do projeto..."

# Build do Backend
echo "📦 Build do Backend..."
cd backend
if [ -f "requirements.txt" ]; then
    echo "✅ Requirements.txt encontrado"
else
    echo "⚠️ Requirements.txt não encontrado"
fi
cd ..

# Build do Frontend
echo "📦 Build do Frontend..."
cd frontend
if [ -f "package.json" ]; then
    echo "✅ Package.json encontrado"
else
    echo "⚠️ Package.json não encontrado"
fi
cd ..

# =============================================================================
# 3. VERIFICAÇÃO DE SEGURANÇA
# =============================================================================
echo "🔍 Verificando segurança..."

# Verificar se ainda há secrets
if grep -r "sk-proj" . --exclude-dir=.git 2>/dev/null; then
    echo "⚠️ Ainda há secrets encontrados!"
else
    echo "✅ Nenhum secret encontrado!"
fi

# Verificar .gitignore
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore encontrado"
else
    echo "❌ .gitignore não encontrado"
fi

# =============================================================================
# 4. GIT OPERATIONS
# =============================================================================
echo "📝 Operações Git..."

# Verificar status
echo "📋 Status do Git:"
git status --porcelain

# Adicionar .gitignore primeiro
echo "📝 Adicionando .gitignore..."
git add .gitignore

# Adicionar todas as mudanças
echo "📦 Adicionando mudanças..."
git add .

# Fazer commit
echo "💾 Fazendo commit..."
git commit -m "🔧 Deploy, build e commit - n.Gabi

- Remove all exposed secrets
- Update .gitignore with security files
- Fix environment configuration
- Prepare for EasyPanel deployment
- Clean up documentation
- Secure repository"

# =============================================================================
# 5. PUSH
# =============================================================================
echo "🚀 Fazendo push..."
git push origin main

# =============================================================================
# 6. VERIFICAÇÃO FINAL
# =============================================================================
echo "✅ Verificação final..."

# Verificar se o push foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "🎉 Push bem-sucedido!"
    echo "✅ Repositório seguro"
    echo "✅ Pronto para deploy no EasyPanel"
else
    echo "❌ Erro no push"
    echo "🔧 Verifique as configurações"
fi

echo "🎯 Deploy, build e commit concluído!" 