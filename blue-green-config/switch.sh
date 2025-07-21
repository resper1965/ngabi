#!/bin/bash

# Script para fazer switch manual entre blue e green
# Uso: ./switch.sh [blue|green]

set -e

TARGET_VERSION=${1:-"green"}

if [ "$TARGET_VERSION" != "blue" ] && [ "$TARGET_VERSION" != "green" ]; then
    echo "❌ Versão deve ser 'blue' ou 'green'"
    exit 1
fi

echo "🔄 Fazendo switch para versão $TARGET_VERSION..."

# Determinar versão atual
if curl -s http://localhost:8000/health | grep -q "version.*blue"; then
    CURRENT_VERSION="blue"
    CURRENT_PORT="8001"
    NEXT_VERSION="green"
    NEXT_PORT="8002"
else
    CURRENT_VERSION="green"
    CURRENT_PORT="8002"
    NEXT_VERSION="blue"
    NEXT_PORT="8001"
fi

if [ "$TARGET_VERSION" = "$CURRENT_VERSION" ]; then
    echo "ℹ️  Já está na versão $CURRENT_VERSION"
    exit 0
fi

# Verificar se versão de destino está rodando
if ! docker ps -q -f name=backend-$NEXT_VERSION | grep -q .; then
    echo "❌ Versão $NEXT_VERSION não está rodando"
    exit 1
fi

# Verificar health da versão de destino
if ! curl -f http://localhost:$NEXT_PORT/health > /dev/null 2>&1; then
    echo "❌ Versão $NEXT_VERSION não está saudável"
    exit 1
fi

# Atualizar configuração do Nginx
echo "⚙️  Atualizando proxy..."
cat > nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend-$CURRENT_VERSION:$CURRENT_PORT weight=0;
        server backend-$NEXT_VERSION:$NEXT_PORT weight=1;
    }
    
    server {
        listen 80;
        
        location /health {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            
            access_log off;
        }
        
        location / {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
    }
}
