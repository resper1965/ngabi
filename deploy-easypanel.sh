#!/bin/bash

# Script para deploy no EasyPanel
# Este script faz o build e push das imagens para facilitar o deploy

echo "🚀 Iniciando deploy para EasyPanel..."

# 1. Fazer build das imagens
echo "📦 Fazendo build das imagens..."
docker-compose build --no-cache

# 2. Verificar se as imagens foram criadas
echo "🔍 Verificando imagens..."
docker images | grep ngabi

# 3. Salvar as imagens como tar para transferência
echo "💾 Salvando imagens..."
docker save ngabi-frontend:latest -o ngabi-frontend.tar
docker save ngabi-backend:latest -o ngabi-backend.tar

# 4. Criar arquivo de configuração do EasyPanel
echo "📝 Criando configuração do EasyPanel..."
cat > easypanel-config.yml << 'EOF'
# Configuração para EasyPanel - n.Gabi
# Copie este conteúdo para o EasyPanel

version: '3.8'

services:
  ngabi-frontend:
    image: ngabi-frontend:latest
    container_name: ngabi-frontend
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
    image: ngabi-backend:latest
    container_name: ngabi-backend
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
    container_name: ngabi-redis
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

echo "✅ Deploy preparado!"
echo ""
echo "📋 Próximos passos:"
echo "1. Copie os arquivos .tar para o servidor do EasyPanel"
echo "2. No EasyPanel, carregue as imagens:"
echo "   docker load -i ngabi-frontend.tar"
echo "   docker load -i ngabi-backend.tar"
echo "3. Copie o conteúdo de easypanel-config.yml para o EasyPanel"
echo "4. Configure as variáveis de ambiente no EasyPanel"
echo "5. Deploy no EasyPanel"
echo ""
echo "🔗 URLs configuradas:"
echo "   Frontend: https://ngabi.ness.tec.br"
echo "   Backend:  https://api.ngabi.ness.tec.br" 