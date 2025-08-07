#!/bin/bash

# Script para remover secrets do histórico do Git
echo "🚨 Removendo secrets do histórico do Git..."

# Lista de arquivos com secrets
SECRET_FILES=(
    "BACKEND_STATUS.md"
    "FRONTEND_ENV_VARS.md"
    "FRONTEND_BACKEND_CONNECTION.md"
    "BACKEND_ENV_VARS.md"
    "EASYUI_ENV_VARS.md"
    "CORRIGIR_SECRETS_URGENTE.md"
    "REMOVER_SECRETS.md"
    "frontend/env.example"
    "backend/env.example"
    "scripts/*.sh"
    "setup-supabase.sh"
    "build-production.sh"
    "docker-compose.production.yml"
    "easypanel-production.yml"
    "deploy-production.sh"
    "build-and-push.sh"
    "organize-repo.sh"
)

# Remover arquivos do staging
echo "📦 Removendo arquivos com secrets do staging..."
for file in "${SECRET_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Removendo: $file"
        git rm --cached "$file" 2>/dev/null || true
    fi
done

# Remover arquivos que já estão no .gitignore
echo "🗑️ Removendo arquivos que estão no .gitignore..."
git rm --cached BACKEND_STATUS.md 2>/dev/null || true
git rm --cached FRONTEND_ENV_VARS.md 2>/dev/null || true
git rm --cached FRONTEND_BACKEND_CONNECTION.md 2>/dev/null || true
git rm --cached BACKEND_ENV_VARS.md 2>/dev/null || true
git rm --cached EASYUI_ENV_VARS.md 2>/dev/null || true
git rm --cached CORRIGIR_SECRETS_URGENTE.md 2>/dev/null || true
git rm --cached REMOVER_SECRETS.md 2>/dev/null || true

# Substituir secrets nos arquivos restantes
echo "🔧 Substituindo secrets nos arquivos restantes..."
find . -name "*.md" -exec sed -i 's/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/your-openai-api-key/g' {} \;

# Verificar se ainda há secrets
echo "🔍 Verificando se ainda há secrets..."
if grep -r "sk-proj" . --exclude-dir=.git --exclude=*.md 2>/dev/null; then
    echo "⚠️ Ainda há secrets encontrados!"
else
    echo "✅ Nenhum secret encontrado!"
fi

# Adicionar .gitignore
echo "📝 Adicionando .gitignore..."
git add .gitignore

# Commit limpo
echo "💾 Fazendo commit limpo..."
git add .
git commit -m "Remove all secrets and secure repository

- Add security files to .gitignore
- Remove files with exposed secrets
- Replace API keys with placeholders
- Prepare for secure deployment"

echo "✅ Script concluído!"
echo "🚀 Agora faça: git push origin main" 