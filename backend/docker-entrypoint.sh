#!/bin/bash

set -e

echo "🚀 Iniciando n.Gabi Backend com bancos integrados..."

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

# Iniciar PostgreSQL
echo "🐘 Iniciando PostgreSQL..."
pg_ctl -D /var/lib/postgresql/data -l /var/log/postgresql/postgresql.log start

# Aguardar PostgreSQL
wait_for_service "PostgreSQL" "http://localhost:5432" || {
    echo "❌ PostgreSQL não conseguiu iniciar"
    exit 1
}

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

# Executar migrações do banco
echo "🗄️ Executando migrações do banco..."
python -m alembic upgrade head

# Iniciar aplicação FastAPI
echo "🚀 Iniciando aplicação FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 