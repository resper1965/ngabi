#!/bin/bash

# Script para testar versões ultra-seguras com gosu
# n.Gabi - Chat Multi-Agente (Versão Hardened + gosu)

set -e

echo "🔒 Testando versões ultra-seguras com gosu..."
echo ""

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down --remove-orphans 2>/dev/null || true

# Limpar imagens antigas
echo "🧹 Limpando imagens antigas..."
docker system prune -f

# Construir versões com gosu
echo "🔨 Construindo versões ultra-seguras com gosu..."
docker-compose -f docker-compose.gosu.yml build --no-cache

# Iniciar serviços
echo "🚀 Iniciando serviços ultra-seguros..."
docker-compose -f docker-compose.gosu.yml up -d

# Aguardar inicialização
echo "⏳ Aguardando inicialização dos serviços..."
sleep 10

# Verificar status dos containers
echo "📊 Status dos containers:"
docker-compose -f docker-compose.gosu.yml ps

# Verificar logs
echo ""
echo "📋 Logs do backend:"
docker logs ngabi-backend-gosu --tail 20

echo ""
echo "📋 Logs do frontend:"
docker logs ngabi-frontend-gosu --tail 10

# Testar health checks
echo ""
echo "🏥 Testando health checks..."

# Backend health
echo "🔍 Backend health:"
curl -f http://localhost:8000/health || echo "❌ Backend não está saudável"

# Frontend health
echo ""
echo "🔍 Frontend health:"
curl -f http://localhost:3000 || echo "❌ Frontend não está saudável"

# Verificar processos rodando como usuário não-root
echo ""
echo "👤 Verificando processos como usuário não-root:"

echo "Backend (deve ser appuser):"
docker exec ngabi-backend-gosu ps aux | head -5

echo ""
echo "Frontend (deve ser nextjs):"
docker exec ngabi-frontend-gosu ps aux | head -5

# Verificar gosu
echo ""
echo "🔒 Verificando gosu:"
docker exec ngabi-backend-gosu gosu --version
docker exec ngabi-frontend-gosu gosu --version

echo ""
echo "✅ Teste das versões ultra-seguras concluído!"
echo ""
echo "🔗 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Para parar: docker-compose -f docker-compose.gosu.yml down" 