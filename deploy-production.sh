#!/bin/bash

# Script de deploy para produção
# Configurado para usar EasyUIPanel para SSL

set -e

echo "🚀 Iniciando deploy de produção..."

# Parar containers existentes
echo "📦 Parando containers existentes..."
docker-compose -f frontend/docker-compose.production.yml down

# Pull das imagens mais recentes
echo "⬇️ Baixando imagens mais recentes..."
docker-compose -f frontend/docker-compose.production.yml pull

# Build das imagens de produção
echo "🔨 Construindo imagens de produção..."
docker-compose -f frontend/docker-compose.production.yml build --no-cache

# Iniciar serviços
echo "▶️ Iniciando serviços..."
docker-compose -f frontend/docker-compose.production.yml up -d

# Aguardar inicialização
echo "⏳ Aguardando inicialização dos serviços..."
sleep 30

# Verificar status dos containers
echo "🔍 Verificando status dos containers..."
docker-compose -f frontend/docker-compose.production.yml ps

# Health check
echo "🏥 Realizando health check..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend está respondendo"
else
    echo "❌ Frontend não está respondendo"
    exit 1
fi

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend está respondendo"
else
    echo "❌ Backend não está respondendo"
    exit 1
fi

echo "🎉 Deploy concluído com sucesso!"
echo "🌐 Aplicação disponível em: https://ngabi.ness.tec.br"
echo "📊 Status dos containers:"
docker-compose -f frontend/docker-compose.production.yml ps 