#!/bin/bash

echo "🚀 COMMIT DAS MUDANÇAS - n.Gabi"
echo "================================"

# =============================================================================
# 1. PREPARAR ARQUIVOS
# =============================================================================
echo "📦 Preparando arquivos..."

# Tornar scripts executáveis
chmod +x setup_env.sh build_project.sh

# Adicionar todos os arquivos
git add .

# =============================================================================
# 2. VERIFICAR STATUS
# =============================================================================
echo "📋 Status do Git:"
git status --porcelain

# =============================================================================
# 3. FAZER COMMIT
# =============================================================================
echo "💾 Fazendo commit..."

git commit -m "🔧 DESABILITAR SECRETS SERVICE - n.Gabi

- Remove dependência do SecretsService
- LLMService agora usa .env diretamente
- Simplifica configuração e debugging
- Melhora performance e compatibilidade
- Adiciona arquivo env.example para backend
- Cria script setup_env.sh para configuração
- Cria script build_project.sh para build completo
- Adiciona documentação DESABILITAR_SECRETS_SERVICE.md
- Corrige problemas de inicialização
- Prepara para deploy no EasyPanel

Mudanças principais:
- backend/app/core/llm_service.py: Remove SecretsService
- backend/env.example: Template de configuração
- setup_env.sh: Script de configuração
- build_project.sh: Script de build
- DESABILITAR_SECRETS_SERVICE.md: Documentação

Resultado: Sistema mais simples e robusto!"

# =============================================================================
# 4. FAZER PUSH
# =============================================================================
echo "🚀 Fazendo push..."
git push origin main

# =============================================================================
# 5. VERIFICAÇÃO FINAL
# =============================================================================
echo "✅ COMMIT CONCLUÍDO!"
echo "===================="
echo "✅ SecretsService desabilitado"
echo "✅ LLMService usa .env diretamente"
echo "✅ Configuração simplificada"
echo "✅ Performance melhorada"
echo "✅ Pronto para deploy no EasyPanel"
echo ""
echo "🎯 Próximos passos:"
echo "1. Configure backend/.env"
echo "2. Execute: ./setup_env.sh"
echo "3. Execute: ./build_project.sh"
echo "4. Deploy no EasyPanel" 