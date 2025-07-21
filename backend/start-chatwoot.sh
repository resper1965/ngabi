#!/bin/bash

echo "💬 Iniciando Chatwoot..."

# Configurar variáveis de ambiente do Chatwoot
export RAILS_ENV=production
export DATABASE_URL=postgresql://postgres:NgabiDB2024!Secure@localhost:5432/chatwoot_production
export REDIS_URL=redis://localhost:6379
export SECRET_KEY_BASE=NgabiChatwootSecretKey2024!SuperSecureKeyForProductionEnvironment
export FRONTEND_URL=https://chatwoot.ngabi.ness.tec.br
export INSTALLATION_NAME="n.Gabi Chatwoot"

# Aguardar um pouco para garantir que os bancos estão prontos
sleep 10

# Ir para o diretório do Chatwoot
cd /app/chatwoot

# Executar migrações se necessário
echo "🗄️ Verificando migrações do Chatwoot..."
bundle exec rails db:migrate

# Executar seeds se necessário
echo "🌱 Verificando seeds do Chatwoot..."
bundle exec rails db:seed

# Compilar assets se necessário
echo "📦 Verificando assets do Chatwoot..."
bundle exec rails assets:precompile

# Iniciar Sidekiq em background
echo "🔄 Iniciando Sidekiq..."
bundle exec sidekiq -d

# Iniciar Chatwoot
echo "🚀 Iniciando servidor Chatwoot..."
exec bundle exec rails server -b 0.0.0.0 -p 3000 