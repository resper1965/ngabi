#!/bin/bash

set -e

echo "🚀 Iniciando n.Gabi Backend com Evolution API e bancos integrados..."

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

# Configurar variáveis de ambiente da Evolution API
export EVOLUTION_API_URL=http://localhost:8080
export EVOLUTION_API_KEY=NgabiEvolution2024!SecureKey
export EVOLUTION_WEBHOOK_URL=https://api.ngabi.ness.tec.br/webhook/evolution

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

# Configurar e inicializar Evolution API
echo "📱 Configurando Evolution API..."
cd /app/evolution-api

# Criar arquivo de configuração da Evolution API
cat > .env << EOF
# Evolution API Configuration
NODE_ENV=production
PORT=8080
HOST=0.0.0.0
CORS_ORIGIN=https://ngabi.ness.tec.br
WEBHOOK_BY_EVENTS=true
WEBHOOK_GLOBAL=https://api.ngabi.ness.tec.br/webhook/evolution
WEBHOOK_EVENTS_CONNECTION=true
WEBHOOK_EVENTS_MESSAGES=true
WEBHOOK_EVENTS_MESSAGES_UPSERT=true
WEBHOOK_EVENTS_MESSAGES_UPDATE=true
WEBHOOK_EVENTS_MESSAGES_DELETE=true
WEBHOOK_EVENTS_SEND_MESSAGE=true
WEBHOOK_EVENTS_CONTACTS_UPDATE=true
WEBHOOK_EVENTS_CONTACTS_UPSERT=true
WEBHOOK_EVENTS_PRESENCE_UPDATE=true
WEBHOOK_EVENTS_CHATS_UPSERT=true
WEBHOOK_EVENTS_CHATS_UPDATE=true
WEBHOOK_EVENTS_CHATS_DELETE=true
WEBHOOK_EVENTS_GROUPS_UPSERT=true
WEBHOOK_EVENTS_GROUPS_UPDATE=true
WEBHOOK_EVENTS_GROUP_PARTICIPANTS_UPDATE=true
WEBHOOK_EVENTS_INSTANCE=true
WEBHOOK_EVENTS_APPLICATION_STARTUP=true
WEBHOOK_EVENTS_QRCODE_UPDATED=true
WEBHOOK_EVENTS_CONNECTION_UPDATE=true
WEBHOOK_EVENTS_CALL=true
WEBHOOK_EVENTS_NEW_JWT_TOKEN=true
WEBHOOK_EVENTS_REQUEST=true
WEBHOOK_EVENTS_SESSION_DATA=true
WEBHOOK_EVENTS_LOGOUT=true
WEBHOOK_EVENTS_DELETE_INSTANCE=true
WEBHOOK_EVENTS_RECEIVE_TEMPLATE=true
WEBHOOK_EVENTS_SEND_TEMPLATE=true
WEBHOOK_EVENTS_SEND_POLL=true
WEBHOOK_EVENTS_SEND_BUTTONS=true
WEBHOOK_EVENTS_SEND_LIST=true
WEBHOOK_EVENTS_SEND_LOCATION=true
WEBHOOK_EVENTS_SEND_CONTACT=true
WEBHOOK_EVENTS_SEND_REACTION=true
WEBHOOK_EVENTS_SEND_VIDEO=true
WEBHOOK_EVENTS_SEND_AUDIO=true
WEBHOOK_EVENTS_SEND_DOCUMENT=true
WEBHOOK_EVENTS_SEND_STICKER=true
WEBHOOK_EVENTS_SEND_IMAGE=true
WEBHOOK_EVENTS_SEND_TEXT=true
WEBHOOK_EVENTS_SEND_MEDIA=true
WEBHOOK_EVENTS_SEND_TEMPLATE_BUTTONS=true
WEBHOOK_EVENTS_SEND_TEMPLATE_LIST=true
WEBHOOK_EVENTS_SEND_TEMPLATE_LOCATION=true
WEBHOOK_EVENTS_SEND_TEMPLATE_CONTACT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_REACTION=true
WEBHOOK_EVENTS_SEND_TEMPLATE_VIDEO=true
WEBHOOK_EVENTS_SEND_TEMPLATE_AUDIO=true
WEBHOOK_EVENTS_SEND_TEMPLATE_DOCUMENT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_STICKER=true
WEBHOOK_EVENTS_SEND_TEMPLATE_IMAGE=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEXT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_MEDIA=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_BUTTONS=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_LIST=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_LOCATION=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_CONTACT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_REACTION=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_VIDEO=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_AUDIO=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_DOCUMENT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_STICKER=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_IMAGE=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEXT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_MEDIA=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_BUTTONS=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_LIST=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_LOCATION=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_CONTACT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_REACTION=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_VIDEO=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_AUDIO=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_DOCUMENT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_STICKER=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_IMAGE=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_TEXT=true
WEBHOOK_EVENTS_SEND_TEMPLATE_TEMPLATE_TEMPLATE_MEDIA=true
EOF

# Iniciar Evolution API em background
echo "📱 Iniciando Evolution API..."
npm start &

# Aguardar Evolution API
wait_for_service "Evolution API" "http://localhost:8080" || {
    echo "❌ Evolution API não conseguiu iniciar"
    exit 1
}

# Voltar para o diretório principal
cd /app

# Iniciar aplicação FastAPI
echo "🚀 Iniciando aplicação FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 