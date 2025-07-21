#!/bin/bash

# Script para configurar ambiente Blue-Green Deployment
# Uso: ./setup-blue-green.sh [initial_version]

set -e

echo "🔄 Configurando ambiente Blue-Green Deployment..."

# Verificar argumentos
INITIAL_VERSION=${1:-"blue"}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado"
    exit 1
fi

# Criar rede Docker se não existir
echo "🌐 Criando rede Docker..."
docker network create chat_app_network 2>/dev/null || echo "Rede já existe"

# Criar diretório para configurações
mkdir -p blue-green-config

# Criar configuração inicial do Nginx
echo "⚙️  Criando configuração inicial do Nginx..."
cat > blue-green-config/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend-blue:8001 weight=1;
    }
    
    server {
        listen 80;
        
        location /health {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            access_log off;
        }
        
        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
    }
}
EOF

# Criar docker-compose inicial
echo "🐳 Criando docker-compose inicial..."
cat > blue-green-config/docker-compose.initial.yml << 'EOF'
version: '3.8'

services:
  backend-blue:
    image: ghcr.io/ngabi/backend:latest
    container_name: backend-blue
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - APP_VERSION=blue
      - APP_PORT=8001
    ports:
      - "8001:8000"
    networks:
      - chat_app_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    restart: unless-stopped
    
  proxy:
    image: nginx:alpine
    container_name: proxy-blue-green
    ports:
      - "8000:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend-blue
    networks:
      - chat_app_network
    restart: unless-stopped

networks:
  chat_app_network:
    external: true
EOF

# Criar script de monitoramento
echo "📊 Criando script de monitoramento..."
cat > blue-green-config/monitor.sh << 'EOF'
#!/bin/bash

echo "📊 Monitoramento Blue-Green Deployment"
echo "======================================"

# Verificar containers rodando
echo "🐳 Containers rodando:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(backend|proxy)"

echo ""
echo "🌐 Status do proxy:"
curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health

echo ""
echo "📈 Métricas:"
curl -s http://localhost:8000/metrics | grep -E "(http_requests_total|http_request_duration_seconds)" | head -5

echo ""
echo "🔍 Health checks:"
echo "Backend Blue: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health)"
echo "Backend Green: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8002/health 2>/dev/null || echo "N/A")"
echo "Proxy: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)"
EOF

chmod +x blue-green-config/monitor.sh

# Criar script de switch manual
echo "🔄 Criando script de switch manual..."
cat > blue-green-config/switch.sh << 'EOF'
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
EOF

# Reiniciar proxy
docker restart proxy-blue-green

# Aguardar estabilização
echo "⏳ Aguardando estabilização..."
sleep 10

# Verificar se switch foi bem-sucedido
for i in {1..5}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Switch para $NEXT_VERSION bem-sucedido!"
        break
    else
        echo "⏳ Aguardando... ($i/5)"
        sleep 2
    fi
done

echo "🎉 Switch concluído!"
EOF

chmod +x blue-green-config/switch.sh

# Criar script de rollback
echo "🔄 Criando script de rollback..."
cat > blue-green-config/rollback.sh << 'EOF'
#!/bin/bash

# Script para fazer rollback
# Uso: ./rollback.sh

set -e

echo "🔄 Iniciando rollback..."

# Determinar versão atual
if curl -s http://localhost:8000/health | grep -q "version.*blue"; then
    CURRENT_VERSION="blue"
    CURRENT_PORT="8001"
    PREVIOUS_VERSION="green"
    PREVIOUS_PORT="8002"
else
    CURRENT_VERSION="green"
    CURRENT_PORT="8002"
    PREVIOUS_VERSION="blue"
    PREVIOUS_PORT="8001"
fi

# Verificar se versão anterior está disponível
if ! docker ps -q -f name=backend-$PREVIOUS_VERSION | grep -q .; then
    echo "❌ Versão anterior $PREVIOUS_VERSION não está disponível"
    exit 1
fi

# Verificar health da versão anterior
if ! curl -f http://localhost:$PREVIOUS_PORT/health > /dev/null 2>&1; then
    echo "❌ Versão anterior $PREVIOUS_VERSION não está saudável"
    exit 1
fi

echo "🔄 Fazendo rollback para $PREVIOUS_VERSION..."

# Atualizar configuração do Nginx
cat > nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend-$CURRENT_VERSION:$CURRENT_PORT weight=0;
        server backend-$PREVIOUS_VERSION:$PREVIOUS_PORT weight=1;
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
EOF

# Reiniciar proxy
docker restart proxy-blue-green

# Aguardar estabilização
echo "⏳ Aguardando estabilização..."
sleep 10

# Verificar se rollback foi bem-sucedido
for i in {1..5}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Rollback para $PREVIOUS_VERSION bem-sucedido!"
        break
    else
        echo "⏳ Aguardando... ($i/5)"
        sleep 2
    fi
done

echo "🎉 Rollback concluído!"
EOF

chmod +x blue-green-config/rollback.sh

# Criar documentação
echo "📚 Criando documentação..."
cat > blue-green-config/README.md << 'EOF'
# Blue-Green Deployment - Chat App

## Visão Geral

Este diretório contém a configuração para deploy Blue-Green da aplicação Chat App.

## Estrutura

```
blue-green-config/
├── nginx.conf              # Configuração do proxy Nginx
├── docker-compose.initial.yml  # Docker Compose inicial
├── monitor.sh              # Script de monitoramento
├── switch.sh               # Script de switch manual
├── rollback.sh             # Script de rollback
└── README.md               # Esta documentação
```

## Configuração Inicial

### 1. Configurar variáveis de ambiente
```bash
export DATABASE_URL="postgresql://user:pass@host:port/db"
export REDIS_URL="redis://host:port"
export OPENAI_API_KEY="your_key"
export PINECONE_API_KEY="your_key"
export JWT_SECRET="your_secret"
```

### 2. Iniciar ambiente inicial
```bash
cd blue-green-config
docker-compose -f docker-compose.initial.yml up -d
```

### 3. Verificar status
```bash
./monitor.sh
```

## Operações

### Monitoramento
```bash
./monitor.sh
```

### Switch Manual
```bash
# Switch para green
./switch.sh green

# Switch para blue
./switch.sh blue
```

### Rollback
```bash
./rollback.sh
```

## Portas

- **8000**: Proxy (ponto de entrada)
- **8001**: Backend Blue
- **8002**: Backend Green

## Health Checks

- **Backend**: `http://localhost:8001/health` e `http://localhost:8002/health`
- **Proxy**: `http://localhost:8000/health`

## Troubleshooting

### Container não inicia
1. Verificar logs: `docker logs backend-blue`
2. Verificar variáveis de ambiente
3. Verificar conectividade com banco/redis

### Proxy não roteia corretamente
1. Verificar configuração do Nginx
2. Reiniciar proxy: `docker restart proxy-blue-green`
3. Verificar health dos backends

### Switch falha
1. Verificar se versão de destino está rodando
2. Verificar health da versão de destino
3. Verificar logs do proxy
EOF

echo "✅ Configuração Blue-Green concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure as variáveis de ambiente"
echo "2. Execute: cd blue-green-config && docker-compose -f docker-compose.initial.yml up -d"
echo "3. Monitore com: ./blue-green-config/monitor.sh"
echo "4. Teste switch com: ./blue-green-config/switch.sh green"
echo ""
echo "📚 Documentação: blue-green-config/README.md" 