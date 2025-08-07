#!/bin/bash

# Script para build e commit - n.Gabi
echo "🚀 Iniciando build e commit..."

# Verificar status do git
echo "📋 Verificando status do git..."
git status

# Adicionar todas as mudanças
echo "📦 Adicionando mudanças..."
git add .

# Fazer commit
echo "💾 Fazendo commit..."
git commit -m "🔧 Corrigir sistema de secrets e cache para EasyPanel

- Reorganizar ordem das classes EnvSecretsManager
- Adicionar tratamento de exceções no secrets manager
- Corrigir configuração do Redis com fallback
- Melhorar tolerância a falhas
- Suportar múltiplos nomes de secrets
- Atualizar documentação para EasyPanel
- Preparar para deploy em homologação"

# Fazer push
echo "🚀 Fazendo push..."
git push origin main

echo "✅ Build e commit concluído!"
echo "🎯 Pronto para deploy no EasyPanel!" 