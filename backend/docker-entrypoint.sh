#!/bin/bash

set -e

echo "🚀 Iniciando n.Gabi Backend com Chatwoot e bancos integrados..."

# Função para aguardar serviço ficar pronto
wait_for_service() {
    local service=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Aguardando $service ficar pronto..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "$url" > /dev/null 2>&1; then
            echo "✅ $service está pronto!"
            return 0
        fi
        
        echo "🔄 Tentativa $attempt/$max_attempts - $service ainda não está pronto..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service não ficou pronto em $max_attempts tentativas"
    return 1
}

# Configurar variáveis de ambiente do Chatwoot
export RAILS_ENV=production
export CHATWOOT_DATABASE_URL=postgresql://postgres:NgabiDB2024!Secure@localhost:5432/chatwoot_production
export CHATWOOT_REDIS_URL=redis://localhost:6379
export SECRET_KEY_BASE=NgabiChatwootSecretKey2024!SuperSecureKeyForProductionEnvironment
export FRONTEND_URL=https://chatwoot.ngabi.ness.tec.br
export INSTALLATION_NAME="n.Gabi Chatwoot"

# Iniciar PostgreSQL
echo "🐘 Iniciando PostgreSQL..."
pg_ctl -D /var/lib/postgresql/data -l /var/log/postgresql/postgresql.log start

# Aguardar PostgreSQL
wait_for_service "PostgreSQL" "http://localhost:5432" || {
    echo "❌ PostgreSQL não conseguiu iniciar"
    exit 1
}

# Criar banco de dados do Chatwoot
echo "🗄️ Criando banco de dados do Chatwoot..."
su - postgres -c "createdb chatwoot_production" || echo "Banco já existe"

# Iniciar Redis
echo "🔴 Iniciando Redis..."
redis-server --daemonize yes

# Aguardar Redis
wait_for_service "Redis" "http://localhost:6379" || {
    echo "❌ Redis não conseguiu iniciar"
    exit 1
}

# Iniciar Elasticsearch
echo "🔍 Iniciando Elasticsearch..."
elasticsearch -d

# Aguardar Elasticsearch
wait_for_service "Elasticsearch" "http://localhost:9200" || {
    echo "❌ Elasticsearch não conseguiu iniciar"
    exit 1
}

# Executar migrações do banco principal
echo "🗄️ Executando migrações do banco principal..."
python -m alembic upgrade head

# Configurar e inicializar Chatwoot
echo "💬 Configurando Chatwoot..."
cd /app/chatwoot

# Executar migrações do Chatwoot
echo "🗄️ Executando migrações do Chatwoot..."
bundle exec rails db:migrate

# Executar seeds do Chatwoot se necessário
echo "🌱 Executando seeds do Chatwoot..."
bundle exec rails db:seed

# Compilar assets do Chatwoot
echo "📦 Compilando assets do Chatwoot..."
bundle exec rails assets:precompile

# Voltar para o diretório principal
cd /app

# Tornar o script do Chatwoot executável
chmod +x start-chatwoot.sh

# Iniciar Chatwoot em background
echo "💬 Iniciando Chatwoot em background..."
./start-chatwoot.sh &

# Aguardar um pouco para o Chatwoot inicializar
sleep 15

# Iniciar aplicação FastAPI
echo "🚀 Iniciando aplicação FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 