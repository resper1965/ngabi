#!/bin/bash

# Script para build e deploy em produção
# n.Gabi - Chat Multi-Agente

echo "🚀 Iniciando build para produção..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERRO] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[AVISO] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# 1. Verificar se os arquivos necessários existem
log "Verificando arquivos necessários..."

if [ ! -f "frontend/Dockerfile.prod" ]; then
    error "frontend/Dockerfile.prod não encontrado!"
    exit 1
fi

if [ ! -f "backend/Dockerfile.prod" ]; then
    error "backend/Dockerfile.prod não encontrado!"
    exit 1
fi

if [ ! -f ".env" ]; then
    warning ".env não encontrado. Criando template..."
    cat > .env << 'EOF'
# =============================================================================
# SUPABASE (Cloud)
# =============================================================================
SUPABASE_URL=https://tegbkyeqfrqkuxeilgpc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5NzI5NzQsImV4cCI6MjA1MDU0ODk3NH0.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR0eXAiOiJKV1QifQ.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlZ2JreWVxZnJxa3V4ZWlsZ3BjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDk3Mjk3NCwiZXhwIjoyMDUwNTQ4OTc0fQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8

# =============================================================================
# JWT (OBRIGATÓRIO)
# =============================================================================
JWT_SECRET_KEY=ngabi-super-secret-jwt-key-2024-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# =============================================================================
# REDIS
# =============================================================================
REDIS_URL=redis://ngabi-redis-prod:6379
REDIS_PASSWORD=ngabi-redis-secure-password-2024

# =============================================================================
# CACHE
# =============================================================================
CACHE_ENABLED=true
CACHE_TTL=3600

# =============================================================================
# RATE LIMITING
# =============================================================================
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# =============================================================================
# CORS
# =============================================================================
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://chat.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br,http://localhost:3000,http://localhost:3001

# =============================================================================
# APP INFO
# =============================================================================
APP_NAME=n.Gabi Backend
APP_VERSION=2.0.0
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
EOF
fi

# 2. Fazer build das imagens de produção
log "Fazendo build das imagens de produção..."

# Build frontend
info "Build do frontend..."
docker build -f frontend/Dockerfile.prod -t ngabi-frontend:prod ./frontend

if [ $? -ne 0 ]; then
    error "Erro no build do frontend!"
    exit 1
fi

# Build backend
info "Build do backend..."
docker build -f backend/Dockerfile.prod -t ngabi-backend:prod ./backend

if [ $? -ne 0 ]; then
    error "Erro no build do backend!"
    exit 1
fi

# 3. Verificar imagens criadas
log "Verificando imagens criadas..."
docker images | grep ngabi

# 4. Salvar imagens para transferência
log "Salvando imagens para transferência..."
docker save ngabi-frontend:prod -o ngabi-frontend-prod.tar
docker save ngabi-backend:prod -o ngabi-backend-prod.tar

# 5. Criar arquivo de configuração para EasyPanel
log "Criando configuração para EasyPanel..."
cat > easypanel-production.yml << 'EOF'
# Configuração para EasyPanel - n.Gabi PRODUÇÃO
# Copie este conteúdo para o EasyPanel

version: '3.8'

services:
  ngabi-frontend:
    image: ngabi-frontend:prod
    container_name: ngabi-frontend-prod
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ngabi-frontend.rule=Host(`ngabi.ness.tec.br`)"
      - "traefik.http.routers.ngabi-frontend.entrypoints=websecure"
      - "traefik.http.routers.ngabi-frontend.tls.certresolver=letsencrypt"
      - "traefik.http.services.ngabi-frontend.loadbalancer.server.port=3000"
    networks:
      - traefik-public

  ngabi-backend:
    image: ngabi-backend:prod
    container_name: ngabi-backend-prod
    restart: unless-stopped
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=${JWT_ALGORITHM}
      - JWT_ACCESS_TOKEN_EXPIRE_MINUTES=${JWT_ACCESS_TOKEN_EXPIRE_MINUTES}
      - REDIS_URL=${REDIS_URL}
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - CACHE_ENABLED=${CACHE_ENABLED}
      - CACHE_TTL=${CACHE_TTL}
      - RATE_LIMIT_ENABLED=${RATE_LIMIT_ENABLED}
      - RATE_LIMIT_REQUESTS=${RATE_LIMIT_REQUESTS}
      - RATE_LIMIT_WINDOW=${RATE_LIMIT_WINDOW}
      - CORS_ORIGINS=${CORS_ORIGINS}
      - APP_NAME=${APP_NAME}
      - APP_VERSION=${APP_VERSION}
      - ENVIRONMENT=production
      - DEBUG=false
      - LOG_LEVEL=INFO
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ngabi-backend.rule=Host(`api.ngabi.ness.tec.br`)"
      - "traefik.http.routers.ngabi-backend.entrypoints=websecure"
      - "traefik.http.routers.ngabi-backend.tls.certresolver=letsencrypt"
      - "traefik.http.services.ngabi-backend.loadbalancer.server.port=8000"
    networks:
      - traefik-public

  ngabi-redis:
    image: redis:7-alpine
    container_name: ngabi-redis-prod
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - traefik-public

networks:
  traefik-public:
    external: true

volumes:
  redis_data:
EOF

# 6. Criar instruções de deploy
log "Criando instruções de deploy..."
cat > DEPLOY-INSTRUCTIONS.md << 'EOF'
# 🚀 Instruções de Deploy - n.Gabi PRODUÇÃO

## 📋 Pré-requisitos
- EasyPanel configurado com Traefik
- Rede `traefik-public` criada
- Variáveis de ambiente configuradas

## 🔧 Passos para Deploy

### 1. Transferir Imagens
```bash
# Copie os arquivos .tar para o servidor do EasyPanel
scp ngabi-frontend-prod.tar user@server:/path/to/easypanel/
scp ngabi-backend-prod.tar user@server:/path/to/easypanel/
```

### 2. Carregar Imagens no EasyPanel
```bash
# No servidor do EasyPanel
docker load -i ngabi-frontend-prod.tar
docker load -i ngabi-backend-prod.tar
```

### 3. Configurar Variáveis de Ambiente
No EasyPanel, configure as seguintes variáveis:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
- `REDIS_URL`
- `REDIS_PASSWORD`
- `CACHE_ENABLED`
- `CACHE_TTL`
- `RATE_LIMIT_ENABLED`
- `RATE_LIMIT_REQUESTS`
- `RATE_LIMIT_WINDOW`
- `CORS_ORIGINS`
- `APP_NAME`
- `APP_VERSION`

### 4. Deploy no EasyPanel
1. Copie o conteúdo de `easypanel-production.yml`
2. Cole no EasyPanel
3. Clique em "Deploy"

## 🔗 URLs Configuradas
- **Frontend**: https://ngabi.ness.tec.br
- **Backend**: https://api.ngabi.ness.tec.br

## ✅ Verificação
Após o deploy, verifique:
1. Containers rodando: `docker ps`
2. Logs: `docker logs ngabi-frontend-prod`
3. Health check: `curl https://ngabi.ness.tec.br/health`

## 🆘 Troubleshooting
- Se houver problemas, verifique os logs: `docker logs <container-name>`
- Verifique se a rede `traefik-public` existe: `docker network ls`
- Confirme se as variáveis de ambiente estão corretas
EOF

log "✅ Build para produção concluído!"
echo ""
echo "📦 Arquivos gerados:"
echo "   - ngabi-frontend-prod.tar"
echo "   - ngabi-backend-prod.tar"
echo "   - easypanel-production.yml"
echo "   - DEPLOY-INSTRUCTIONS.md"
echo ""
echo "🚀 Próximos passos:"
echo "   1. Copie os arquivos .tar para o servidor do EasyPanel"
echo "   2. Siga as instruções em DEPLOY-INSTRUCTIONS.md"
echo "   3. Deploy no EasyPanel"
echo ""
echo "🔗 URLs configuradas:"
echo "   Frontend: https://ngabi.ness.tec.br"
echo "   Backend:  https://api.ngabi.ness.tec.br" 