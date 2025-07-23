#!/bin/bash

# Script para organizar o repositório n.Gabi
# Remove arquivos desnecessários e antigos

echo "🧹 Iniciando organização do repositório..."

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

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# 1. Remover Dockerfiles antigos e duplicados
log "Removendo Dockerfiles antigos..."

# Backend - manter apenas os principais
rm -f backend/Dockerfile.alpine
rm -f backend/Dockerfile.alpine-secure
rm -f backend/Dockerfile.alpine-optimized
rm -f backend/Dockerfile.alpine-gosu
rm -f backend/Dockerfile.python313
rm -f backend/requirements-compatibility-test.txt

# Frontend - manter apenas os principais
rm -f frontend/Dockerfile.alpine
rm -f frontend/Dockerfile.alpine-gosu
rm -f frontend/nginx.conf

# 2. Remover docker-compose duplicados
log "Removendo docker-compose duplicados..."
rm -f docker-compose.prod.yml
rm -f docker-compose.secure.yml
rm -f docker-compose.gosu.yml
rm -f docker-compose.ports.yml
rm -f docker-compose.port-forwarding.yml
rm -f docker-compose.duplo.yml
rm -f docker-compose.traefik.yml
rm -f docker-compose.easypanel.yml

# 3. Remover arquivos de configuração antigos
log "Removendo arquivos de configuração antigos..."
rm -f easypanel-config.yml
rm -f easypanel-deploy.yml
rm -f easypanel-ngabi.yml
rm -f deploy-easypanel.sh

# 4. Remover documentação antiga
log "Removendo documentação antiga..."
rm -f VARIAVEIS-AMBIENTE.md
rm -f GOSU-SEGURANCA.md
rm -f ANALISE-NODEJS-VULNERABILIDADES.md
rm -f RESUMO-MIGRACAO-ALPINE.md
rm -f ANALISE-VULNERABILIDADES-ALPINE.md
rm -f ANALISE-ALPINE-vs-SLIM.md
rm -f MIGRACAO-PYTHON313.md
rm -f ARQUITETURA-OTIMIZADA.md
rm -f supabase-config.md
rm -f README-SUPABASE.md
rm -f README-EASYPANEL.md
rm -f EASYPANEL-DEPLOY.md
rm -f SISTEMA-EVENTOS-WEBHOOKS.md
rm -f SUPABASE-SETUP.md
rm -f SUPABASE-SIMPLE-CONFIG.md

# 5. Remover arquivos de exemplo antigos
log "Removendo arquivos de exemplo antigos..."
rm -f env.example
rm -f easypanel.env

# 6. Remover diretórios desnecessários
log "Removendo diretórios desnecessários..."
rm -rf blue-green-config/
rm -rf supabase/

# 7. Organizar documentação
log "Organizando documentação..."
mkdir -p docs

# Mover documentação importante para docs/
if [ -f "nGabiPRD.md" ]; then
    mv nGabiPRD.md docs/
fi

if [ -f "supabase-schema.sql" ]; then
    mv supabase-schema.sql docs/
fi

# 8. Criar README principal atualizado
log "Criando README principal..."
cat > README.md << 'EOF'
# n.Gabi - Chat Multi-Agente

Plataforma de chat inteligente com múltiplos agentes, construída com React, FastAPI e Supabase.

## 🚀 Tecnologias

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python 3.13
- **Database**: Supabase (PostgreSQL)
- **Cache**: Redis
- **Deploy**: EasyPanel + Traefik

## 📁 Estrutura do Projeto

```
ngabi/
├── frontend/          # Aplicação React
├── backend/           # API FastAPI
├── docs/             # Documentação
├── scripts/          # Scripts utilitários
└── docker-compose.yml
```

## 🛠️ Desenvolvimento

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+
- Python 3.13+

### Executar Localmente
```bash
# Clone o repositório
git clone https://github.com/resper1965/ngabi.git
cd ngabi

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute com Docker Compose
docker-compose up -d
```

### URLs Locais
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Redis**: localhost:6379

## 🚀 Produção

### Deploy no EasyPanel
```bash
# Build para produção
./build-production.sh

# Siga as instruções geradas para deploy no EasyPanel
```

### URLs de Produção
- **Frontend**: https://ngabi.ness.tec.br
- **Backend**: https://api.ngabi.ness.tec.br

## 📚 Documentação

- [PRD (Product Requirements Document)](docs/nGabiPRD.md)
- [Schema do Banco de Dados](docs/supabase-schema.sql)

## 🔧 Scripts Úteis

- `./build-production.sh` - Build para produção
- `docker-compose up -d` - Executar localmente
- `docker-compose down` - Parar serviços

## 📄 Licença

Este projeto é privado e proprietário.
EOF

# 9. Limpar node_modules se existir
if [ -d "frontend/node_modules" ]; then
    log "Removendo node_modules..."
    rm -rf frontend/node_modules
fi

# 10. Criar .dockerignore global
log "Criando .dockerignore global..."
cat > .dockerignore << 'EOF'
# Git
.git
.gitignore

# Documentation
docs/
*.md
!README.md

# Scripts
scripts/
*.sh

# Docker
docker-compose*.yml
Dockerfile*

# Environment
.env
.env.*

# Logs
*.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
EOF

# 11. Atualizar .gitignore
log "Atualizando .gitignore..."
cat > .gitignore << 'EOF'
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Dependencies
node_modules/
__pycache__/
*.py[cod]
*$py.class

# Build outputs
dist/
dist-ssr/
build/
*.egg-info/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Docker
*.tar
*.tar.gz
*.tar.bz2

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp

# Python
venv/
env/
ENV/
env.bak/
venv.bak/

# Coverage
.coverage
htmlcov/
.pytest_cache/
EOF

log "✅ Organização concluída!"
echo ""
echo "📋 Resumo das mudanças:"
echo "   ✅ Dockerfiles antigos removidos"
echo "   ✅ docker-compose duplicados removidos"
echo "   ✅ Documentação antiga removida"
echo "   ✅ Diretórios desnecessários removidos"
echo "   ✅ README principal atualizado"
echo "   ✅ .gitignore atualizado"
echo "   ✅ .dockerignore criado"
echo ""
echo "📁 Estrutura final:"
echo "   - frontend/ (React + TypeScript)"
echo "   - backend/ (FastAPI + Python)"
echo "   - docs/ (Documentação)"
echo "   - scripts/ (Scripts utilitários)"
echo "   - docker-compose.yml (Desenvolvimento)"
echo "   - docker-compose.production.yml (Produção)"
echo "   - build-production.sh (Build automatizado)" 