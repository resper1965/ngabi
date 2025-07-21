#!/bin/bash

# 🚀 Script de Configuração do Supabase da Nuvem
# n.Gabi - Setup Supabase

set -e

echo "🚀 Configurando Supabase da Nuvem para n.Gabi..."
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    print_status "Criando arquivo .env..."
    cat > .env << 'EOF'
# SUPABASE CONFIGURATION (CLOUD)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# REDIS CONFIGURATION
REDIS_URL=redis://localhost:6379

# CORS CONFIGURATION
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# FRONTEND CONFIGURATION
VITE_API_BASE_URL=http://localhost:8000

# APPLICATION CONFIGURATION
APP_NAME=n.Gabi
APP_VERSION=2.0.0
EOF
    print_success "Arquivo .env criado!"
else
    print_warning "Arquivo .env já existe. Verifique se as configurações estão corretas."
fi

echo ""
print_status "📋 Próximos passos para configurar o Supabase:"
echo ""
echo "1. 🌐 Acesse: https://supabase.com/dashboard"
echo "2. 📁 Crie um novo projeto ou selecione um existente"
echo "3. ⚙️  Vá em Settings → API"
echo "4. 📋 Copie:"
echo "   - Project URL"
echo "   - anon public key"
echo "5. ✏️  Edite o arquivo .env com suas credenciais"
echo "6. 🗄️  Execute o SQL do arquivo SUPABASE-SETUP.md no SQL Editor"
echo "7. 🚀 Execute: docker-compose up -d"
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    print_error "Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

print_success "Docker está rodando!"

# Verificar se as credenciais estão configuradas
if grep -q "your-project.supabase.co" .env; then
    print_warning "⚠️  Configure suas credenciais do Supabase no arquivo .env"
    echo "   - SUPABASE_URL=https://seu-projeto.supabase.co"
    echo "   - SUPABASE_ANON_KEY=sua_chave_anonima_aqui"
else
    print_success "✅ Credenciais do Supabase configuradas!"
fi

echo ""
print_status "🔧 Para testar a configuração:"
echo "   docker-compose up -d"
echo "   docker-compose logs backend"
echo "   curl http://localhost:8000/health"
echo ""

print_success "🎉 Setup do Supabase concluído!"
print_status "📚 Consulte SUPABASE-SETUP.md para mais detalhes" 