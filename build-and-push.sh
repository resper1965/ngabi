#!/bin/bash

# Script para build e push das imagens n.Gabi para produção
# Usado para deploy no EasyPanel

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[AVISO] $1${NC}"
}

error() {
    echo -e "${RED}[ERRO] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Configurações
DOCKER_USERNAME="resper1965"
FRONTEND_IMAGE="ngabi-frontend"
BACKEND_IMAGE="ngabi-backend"
VERSION="latest"

log "🚀 Iniciando build e push das imagens n.Gabi para produção..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    error "Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi

# Verificar se está logado no Docker Hub
if ! docker info | grep -q "Username"; then
    warning "Você não está logado no Docker Hub. Execute: docker login"
    read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build da imagem do Frontend
log "📦 Build da imagem do Frontend..."
cd frontend
docker build -f Dockerfile.prod -t ${DOCKER_USERNAME}/${FRONTEND_IMAGE}:${VERSION} .
docker tag ${DOCKER_USERNAME}/${FRONTEND_IMAGE}:${VERSION} ${DOCKER_USERNAME}/${FRONTEND_IMAGE}:latest
cd ..

# Build da imagem do Backend
log "📦 Build da imagem do Backend..."
cd backend
docker build -f Dockerfile.prod -t ${DOCKER_USERNAME}/${BACKEND_IMAGE}:${VERSION} .
docker tag ${DOCKER_USERNAME}/${BACKEND_IMAGE}:${VERSION} ${DOCKER_USERNAME}/${BACKEND_IMAGE}:latest
cd ..

# Push das imagens para Docker Hub
log "📤 Push das imagens para Docker Hub..."

log "Push Frontend..."
docker push ${DOCKER_USERNAME}/${FRONTEND_IMAGE}:${VERSION}
docker push ${DOCKER_USERNAME}/${FRONTEND_IMAGE}:latest

log "Push Backend..."
docker push ${DOCKER_USERNAME}/${BACKEND_IMAGE}:${VERSION}
docker push ${DOCKER_USERNAME}/${BACKEND_IMAGE}:latest

# Criar arquivo de instruções para EasyPanel
log "📝 Criando instruções para EasyPanel..."

cat > DEPLOY-EASYPANEL.md << 'EOF'
# 🚀 Deploy n.Gabi no EasyPanel

## 📋 Pré-requisitos

1. EasyPanel configurado com Traefik
2. Rede `traefik-public` criada
3. Variáveis de ambiente configuradas

## 🔧 Configuração no EasyPanel

### 1. Criar Projeto
- Nome: `ngabi`
- Descrição: `Chat Multi-Agente n.Gabi`

### 2. Configurar Variáveis de Ambiente
```bash
SUPABASE_URL=sua_url_do_supabase
SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
```

### 3. Deploy dos Serviços

#### Frontend
- **Imagem**: `resper1965/ngabi-frontend:latest`
- **Porta**: `3000`
- **Domínio**: `ngabi.ness.tec.br`
- **SSL**: Automático (Let's Encrypt)

#### Backend
- **Imagem**: `resper1965/ngabi-backend:latest`
- **Porta**: `8000`
- **Domínio**: `api.ngabi.ness.tec.br`
- **SSL**: Automático (Let's Encrypt)

#### Redis
- **Imagem**: `redis:7-alpine`
- **Porta**: `6379`

### 4. Configurar Traefik Labels

#### Frontend Labels:
```yaml
- "traefik.enable=true"
- "traefik.http.routers.ngabi-frontend.rule=Host(`ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-frontend.entrypoints=websecure"
- "traefik.http.routers.ngabi-frontend.tls.certresolver=letsencrypt"
- "traefik.http.services.ngabi-frontend.loadbalancer.server.port=3000"
- "traefik.docker.network=traefik-public"
```

#### Backend Labels:
```yaml
- "traefik.enable=true"
- "traefik.http.routers.ngabi-backend.rule=Host(`api.ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-backend.entrypoints=websecure"
- "traefik.http.routers.ngabi-backend.tls.certresolver=letsencrypt"
- "traefik.http.services.ngabi-backend.loadbalancer.server.port=8000"
- "traefik.docker.network=traefik-public"
```

## 🌐 URLs de Produção

- **Frontend**: https://ngabi.ness.tec.br
- **Backend API**: https://api.ngabi.ness.tec.br
- **Health Check**: https://api.ngabi.ness.tec.br/health

## 🔍 Verificação

1. Acesse https://ngabi.ness.tec.br
2. Verifique se a página carrega corretamente
3. Teste a API em https://api.ngabi.ness.tec.br/health
4. Verifique os logs no EasyPanel

## 🛠️ Troubleshooting

### Se a página não carregar:
1. Verifique se as imagens foram baixadas corretamente
2. Confirme se as variáveis de ambiente estão configuradas
3. Verifique os logs dos containers
4. Confirme se o Traefik está roteando corretamente

### Se a API não responder:
1. Verifique se o Redis está rodando
2. Confirme as credenciais do Supabase
3. Verifique os logs do backend

## 📞 Suporte

Para problemas técnicos, verifique:
- Logs dos containers no EasyPanel
- Status dos serviços
- Configuração do Traefik
- Variáveis de ambiente
EOF

log "✅ Build e push concluídos com sucesso!"
echo ""
echo "📋 Resumo:"
echo "   ✅ Frontend: ${DOCKER_USERNAME}/${FRONTEND_IMAGE}:${VERSION}"
echo "   ✅ Backend: ${DOCKER_USERNAME}/${BACKEND_IMAGE}:${VERSION}"
echo "   ✅ Instruções: DEPLOY-EASYPANEL.md"
echo ""
echo "🚀 Próximos passos:"
echo "   1. Acesse o EasyPanel"
echo "   2. Siga as instruções em DEPLOY-EASYPANEL.md"
echo "   3. Configure as variáveis de ambiente"
echo "   4. Deploy dos serviços"
echo ""
echo "🌐 URLs finais:"
echo "   - Frontend: https://ngabi.ness.tec.br"
echo "   - Backend: https://api.ngabi.ness.tec.br" 