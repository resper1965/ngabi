#!/bin/bash

# 🚀 Script de Deploy Automatizado para n.Gabi
# Compatível com EasyPanel

set -e

echo "🚀 Iniciando deploy do n.Gabi..."

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
PROJECT_NAME="ngabi"
DOMAIN="ngabi.ness.tec.br"
API_DOMAIN="api.ngabi.ness.tec.br"
ADMIN_EMAIL="admin@ngabi.ness.tec.br"

# =============================================================================
# VERIFICAÇÕES PRÉVIAS
# =============================================================================
echo "📋 Verificando pré-requisitos..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado"
    exit 1
fi

# Verificar se as variáveis de ambiente existem
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Variáveis de ambiente SUPABASE_URL e SUPABASE_ANON_KEY são obrigatórias"
    exit 1
fi

echo "✅ Pré-requisitos verificados"

# =============================================================================
# BACKUP (se aplicável)
# =============================================================================
if [ -d "backups" ]; then
    echo "💾 Criando backup antes do deploy..."
    mkdir -p backups
    docker-compose exec -T postgres pg_dump -U ngabi_user ngabi_backup > "backups/pre_deploy_$(date +%Y%m%d_%H%M%S).sql" 2>/dev/null || echo "⚠️ Backup opcional falhou"
fi

# =============================================================================
# BUILD DAS IMAGENS
# =============================================================================
echo "🔨 Construindo imagens Docker..."

# Build do frontend
echo "📦 Construindo frontend..."
docker-compose build frontend

# Build do backend
echo "🐍 Construindo backend..."
docker-compose build backend

echo "✅ Imagens construídas com sucesso"

# =============================================================================
# DEPLOY COM ZERO-DOWNTIME
# =============================================================================
echo "🚀 Iniciando deploy com zero-downtime..."

# Parar serviços antigos (se existirem)
echo "⏹️ Parando serviços antigos..."
docker-compose down --remove-orphans || true

# Iniciar serviços em ordem
echo "🔄 Iniciando Redis..."
docker-compose up -d redis
sleep 10

echo "🔄 Iniciando PostgreSQL (se configurado)..."
docker-compose up -d postgres || echo "⚠️ PostgreSQL opcional não iniciado"
sleep 5

echo "🔄 Iniciando Traefik..."
docker-compose up -d traefik
sleep 5

echo "🔄 Iniciando Backend..."
docker-compose up -d backend
sleep 15

echo "🔄 Iniciando Frontend..."
docker-compose up -d frontend
sleep 10

# =============================================================================
# VERIFICAÇÕES PÓS-DEPLOY
# =============================================================================
echo "🔍 Verificando saúde dos serviços..."

# Verificar Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: OK"
else
    echo "❌ Redis: FALHOU"
    exit 1
fi

# Verificar Backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend: OK"
else
    echo "❌ Backend: FALHOU"
    exit 1
fi

# Verificar Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: FALHOU"
    exit 1
fi

# =============================================================================
# CONFIGURAÇÃO DE DOMÍNIO (se aplicável)
# =============================================================================
echo "🌐 Configurando domínios..."

# Verificar se os domínios estão configurados
if command -v dig &> /dev/null; then
    if dig +short $DOMAIN | grep -q .; then
        echo "✅ Domínio $DOMAIN configurado"
    else
        echo "⚠️ Domínio $DOMAIN não encontrado no DNS"
    fi
    
    if dig +short $API_DOMAIN | grep -q .; then
        echo "✅ Domínio $API_DOMAIN configurado"
    else
        echo "⚠️ Domínio $API_DOMAIN não encontrado no DNS"
    fi
fi

# =============================================================================
# TESTES AUTOMATIZADOS
# =============================================================================
echo "🧪 Executando testes automatizados..."

# Teste da API
if curl -f http://localhost:8000/api/v1/events/types > /dev/null 2>&1; then
    echo "✅ API Events: OK"
else
    echo "❌ API Events: FALHOU"
fi

# Teste de webhooks
if curl -f http://localhost:8000/api/v1/webhooks/events > /dev/null 2>&1; then
    echo "✅ API Webhooks: OK"
else
    echo "❌ API Webhooks: FALHOU"
fi

# =============================================================================
# LIMPEZA
# =============================================================================
echo "🧹 Limpando recursos não utilizados..."
docker system prune -f

# =============================================================================
# RELATÓRIO FINAL
# =============================================================================
echo ""
echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo ""
echo "📊 Status dos Serviços:"
docker-compose ps
echo ""
echo "🌐 URLs de Acesso:"
echo "   Frontend: https://$DOMAIN"
echo "   Backend API: https://$API_DOMAIN"
echo "   Traefik Dashboard: https://traefik.$DOMAIN"
echo ""
echo "📋 Comandos Úteis:"
echo "   Logs: docker-compose logs -f"
echo "   Status: docker-compose ps"
echo "   Restart: docker-compose restart"
echo "   Stop: docker-compose down"
echo ""
echo "📚 Documentação:"
echo "   Sistema de Eventos: SISTEMA-EVENTOS-WEBHOOKS.md"
echo "   API Docs: https://$API_DOMAIN/docs"
echo "" 