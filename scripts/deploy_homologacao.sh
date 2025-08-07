#!/bin/bash

# 🚀 Script de Deploy para Homologação - n.Gabi
# Este script automatiza o processo de deploy em homologação

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy em homologação..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "BMAD.md" ]; then
    error "Execute este script na raiz do projeto n.Gabi"
    exit 1
fi

# Verificar dependências
check_dependencies() {
    log "Verificando dependências..."
    
    # Verificar se git está instalado
    if ! command -v git &> /dev/null; then
        error "Git não está instalado"
        exit 1
    fi
    
    # Verificar se estamos em um repositório git
    if [ ! -d ".git" ]; then
        error "Não estamos em um repositório git"
        exit 1
    fi
    
    log "✅ Dependências verificadas"
}

# Verificar status do git
check_git_status() {
    log "Verificando status do git..."
    
    # Verificar se há mudanças não commitadas
    if [ -n "$(git status --porcelain)" ]; then
        warn "Há mudanças não commitadas:"
        git status --short
        read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Deploy cancelado"
            exit 1
        fi
    fi
    
    # Verificar se estamos na branch main
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        warn "Você está na branch '$current_branch', não na 'main'"
        read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Deploy cancelado"
            exit 1
        fi
    fi
    
    log "✅ Status do git verificado"
}

# Verificar arquivos de configuração
check_config_files() {
    log "Verificando arquivos de configuração..."
    
    # Verificar se os arquivos principais existem
    required_files=(
        "backend/app/main.py"
        "backend/requirements.txt"
        "frontend/package.json"
        "BMAD.md"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            error "Arquivo obrigatório não encontrado: $file"
            exit 1
        fi
    done
    
    log "✅ Arquivos de configuração verificados"
}

# Verificar variáveis de ambiente
check_env_vars() {
    log "Verificando variáveis de ambiente..."
    
    # Lista de variáveis obrigatórias para homologação
    required_vars=(
        "SUPABASE_URL"
        "SUPABASE_ANON_KEY"
        "SUPABASE_SERVICE_ROLE_KEY"
        "OPENAI_API_KEY"
        "REDIS_URL"
    )
    
    missing_vars=()
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        error "Variáveis de ambiente obrigatórias não definidas:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        exit 1
    fi
    
    log "✅ Variáveis de ambiente verificadas"
}

# Backup antes do deploy
create_backup() {
    log "Criando backup..."
    
    backup_dir="backups/$(date +'%Y%m%d_%H%M%S')"
    mkdir -p "$backup_dir"
    
    # Backup dos arquivos de configuração
    cp -r backend/app/core/config*.py "$backup_dir/" 2>/dev/null || true
    cp -r frontend/src/config*.ts "$backup_dir/" 2>/dev/null || true
    
    # Backup do BMAD
    cp BMAD.md "$backup_dir/"
    
    log "✅ Backup criado em $backup_dir"
}

# Testes pré-deploy
run_pre_deploy_tests() {
    log "Executando testes pré-deploy..."
    
    # Testar se o backend pode ser importado
    cd backend
    python -c "import app.main; print('✅ Backend importado com sucesso')" || {
        error "Erro ao importar backend"
        exit 1
    }
    cd ..
    
    # Testar se o frontend pode ser buildado
    cd frontend
    npm run build --silent || {
        error "Erro ao fazer build do frontend"
        exit 1
    }
    cd ..
    
    log "✅ Testes pré-deploy passaram"
}

# Deploy no EasyUIPanel (simulado)
deploy_to_easyui() {
    log "Iniciando deploy no EasyUIPanel..."
    
    # Aqui você conectaria com a API do EasyUIPanel
    # Por enquanto, vamos simular o processo
    
    info "📋 Passos para deploy manual no EasyUIPanel:"
    echo
    echo "1. Acesse o EasyUIPanel"
    echo "2. Crie um novo projeto: 'ngabi-homologacao'"
    echo "3. Configure o domínio: ngabi.ness.tec.br"
    echo "4. Configure as aplicações:"
    echo "   - Backend (Python, porta 8000, path: /backend)"
    echo "   - Frontend (Node.js, porta 3000, path: /)"
    echo "   - Redis (porta 6379)"
    echo "5. Configure as variáveis de ambiente"
    echo "6. Conecte o repositório GitHub"
    echo "7. Habilite auto-deploy"
    echo
    echo "📝 URLs de homologação:"
    echo "   - Frontend: https://ngabi.ness.tec.br"
    echo "   - Backend: https://ngabi.ness.tec.br/backend"
    echo "   - Docs: https://ngabi.ness.tec.br/backend/docs"
    echo "   - Health: https://ngabi.ness.tec.br/backend/health"
    echo
    
    read -p "Pressione Enter quando o deploy estiver configurado..."
}

# Testes pós-deploy
run_post_deploy_tests() {
    log "Executando testes pós-deploy..."
    
    # URLs de teste
    api_url="https://ngabi.ness.tec.br/backend"
    frontend_url="https://ngabi.ness.tec.br"
    
    info "Testando health check..."
    if curl -f -s "$api_url/health" > /dev/null; then
        log "✅ Health check passou"
    else
        error "❌ Health check falhou"
        return 1
    fi
    
    info "Testando documentação da API..."
    if curl -f -s "$api_url/docs" > /dev/null; then
        log "✅ Documentação da API acessível"
    else
        warn "⚠️ Documentação da API não acessível"
    fi
    
    info "Testando frontend..."
    if curl -f -s "$frontend_url" > /dev/null; then
        log "✅ Frontend acessível"
    else
        error "❌ Frontend não acessível"
        return 1
    fi
    
    log "✅ Testes pós-deploy passaram"
}

# Função principal
main() {
    log "🚀 Iniciando processo de deploy em homologação..."
    
    # Verificações
    check_dependencies
    check_git_status
    check_config_files
    check_env_vars
    
    # Backup
    create_backup
    
    # Testes pré-deploy
    run_pre_deploy_tests
    
    # Deploy
    deploy_to_easyui
    
    # Testes pós-deploy
    run_post_deploy_tests
    
    log "🎉 Deploy em homologação concluído com sucesso!"
    echo
    echo "📋 Próximos passos:"
    echo "1. Testar todas as funcionalidades"
    echo "2. Verificar logs no EasyUIPanel"
    echo "3. Configurar monitoramento"
    echo "4. Documentar problemas encontrados"
    echo
    echo "🔗 URLs de acesso:"
    echo "   - Frontend: https://ngabi.ness.tec.br"
    echo "   - Backend: https://ngabi.ness.tec.br/backend"
    echo "   - Docs: https://ngabi.ness.tec.br/backend/docs"
    echo "   - Health: https://ngabi.ness.tec.br/backend/health"
}

# Executar função principal
main "$@" 