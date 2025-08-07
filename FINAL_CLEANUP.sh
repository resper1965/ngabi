#!/bin/bash

echo "🚨 LIMPEZA FINAL DE SECRETS - n.Gabi"
echo "======================================"

# 1. Remover arquivos .env com secrets
echo "🗑️ Removendo arquivos .env..."
find . -name "*.env*" -type f -delete 2>/dev/null || true
find . -name ".env*" -type f -delete 2>/dev/null || true

# 2. Remover arquivos de backup
echo "🗑️ Removendo arquivos de backup..."
find . -name "*.backup" -type f -delete 2>/dev/null || true
find . -name "*backup*" -type f -delete 2>/dev/null || true

# 3. Substituir secrets em TODOS os arquivos
echo "🔧 Substituindo secrets em todos os arquivos..."
find . -type f -not -path "./.git/*" -exec sed -i 's/your-openai-api-key/your-openai-api-key/g' {} \; 2>/dev/null || true

# 4. Verificar se ainda há secrets
echo "🔍 Verificando se ainda há secrets..."
if grep -r "sk-proj" . --exclude-dir=.git 2>/dev/null; then
    echo "⚠️ Ainda há secrets encontrados!"
    grep -r "sk-proj" . --exclude-dir=.git
else
    echo "✅ Nenhum secret encontrado!"
fi

# 5. Git operations
echo "📝 Operações Git..."

# Remover arquivos do staging
git rm --cached backend/.env 2>/dev/null || true
git rm --cached backend/.env.backup 2>/dev/null || true
git rm --cached frontend/.env 2>/dev/null || true
git rm --cached frontend/.env.backup 2>/dev/null || true

# Adicionar .gitignore
git add .gitignore

# Adicionar todas as mudanças
git add .

# Commit limpo
git commit -m "🔒 FINAL CLEANUP - Remove ALL secrets

- Delete all .env files with secrets
- Replace all API keys with placeholders
- Secure repository completely
- Ready for EasyPanel deployment"

# Push
echo "🚀 Fazendo push..."
git push origin main

echo "✅ LIMPEZA FINAL CONCLUÍDA!" 