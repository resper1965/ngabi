#!/bin/bash

# 💾 Script de Backup Automático para n.Gabi
# Compatível com EasyPanel

set -e

echo "💾 Iniciando backup do n.Gabi..."

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
BACKUP_DIR="./backups"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_NAME="ngabi"

# =============================================================================
# VERIFICAÇÕES
# =============================================================================
echo "📋 Verificando configurações..."

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Verificar se PostgreSQL está rodando
if ! docker-compose ps postgres | grep -q "Up"; then
    echo "⚠️ PostgreSQL não está rodando. Backup opcional."
    exit 0
fi

# =============================================================================
# BACKUP DO BANCO DE DADOS
# =============================================================================
echo "🗄️ Criando backup do banco de dados..."

# Backup do PostgreSQL local (se existir)
if docker-compose exec -T postgres pg_isready -U ngabi_user > /dev/null 2>&1; then
    BACKUP_FILE="$BACKUP_DIR/postgres_backup_$DATE.sql"
    
    docker-compose exec -T postgres pg_dump \
        -U ngabi_user \
        -d ngabi_backup \
        --clean \
        --if-exists \
        --create \
        > "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        echo "✅ Backup PostgreSQL criado: $BACKUP_FILE"
        
        # Comprimir backup
        gzip "$BACKUP_FILE"
        echo "✅ Backup comprimido: $BACKUP_FILE.gz"
    else
        echo "❌ Erro ao criar backup PostgreSQL"
        exit 1
    fi
else
    echo "⚠️ PostgreSQL local não disponível"
fi

# =============================================================================
# BACKUP DO REDIS
# =============================================================================
echo "🔴 Criando backup do Redis..."

if docker-compose ps redis | grep -q "Up"; then
    REDIS_BACKUP_FILE="$BACKUP_DIR/redis_backup_$DATE.rdb"
    
    # Criar snapshot do Redis
    docker-compose exec -T redis redis-cli BGSAVE
    
    # Aguardar snapshot
    sleep 5
    
    # Copiar arquivo RDB
    docker cp ngabi-redis:/data/dump.rdb "$REDIS_BACKUP_FILE"
    
    if [ -f "$REDIS_BACKUP_FILE" ]; then
        echo "✅ Backup Redis criado: $REDIS_BACKUP_FILE"
        
        # Comprimir backup
        gzip "$REDIS_BACKUP_FILE"
        echo "✅ Backup Redis comprimido: $REDIS_BACKUP_FILE.gz"
    else
        echo "❌ Erro ao criar backup Redis"
    fi
else
    echo "⚠️ Redis não está rodando"
fi

# =============================================================================
# BACKUP DE CONFIGURAÇÕES
# =============================================================================
echo "⚙️ Criando backup de configurações..."

CONFIG_BACKUP_FILE="$BACKUP_DIR/config_backup_$DATE.tar.gz"

# Criar backup de configurações importantes
tar -czf "$CONFIG_BACKUP_FILE" \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='backups' \
    --exclude='*.log' \
    easypanel-config.yml \
    easypanel.env \
    docker-compose.yml \
    supabase-schema.sql \
    scripts/ \
    backend/app/core/ \
    frontend/src/config/ \
    2>/dev/null || true

if [ -f "$CONFIG_BACKUP_FILE" ]; then
    echo "✅ Backup de configurações criado: $CONFIG_BACKUP_FILE"
else
    echo "⚠️ Erro ao criar backup de configurações"
fi

# =============================================================================
# BACKUP DE LOGS
# =============================================================================
echo "📝 Criando backup de logs..."

LOGS_BACKUP_FILE="$BACKUP_DIR/logs_backup_$DATE.tar.gz"

# Coletar logs dos containers
docker-compose logs --no-color > "$BACKUP_DIR/docker_logs_$DATE.txt" 2>/dev/null || true

# Comprimir logs
tar -czf "$LOGS_BACKUP_FILE" \
    "$BACKUP_DIR/docker_logs_$DATE.txt" \
    2>/dev/null || true

if [ -f "$LOGS_BACKUP_FILE" ]; then
    echo "✅ Backup de logs criado: $LOGS_BACKUP_FILE"
    rm -f "$BACKUP_DIR/docker_logs_$DATE.txt"
else
    echo "⚠️ Erro ao criar backup de logs"
fi

# =============================================================================
# LIMPEZA DE BACKUPS ANTIGOS
# =============================================================================
echo "🧹 Limpando backups antigos..."

# Remover backups mais antigos que RETENTION_DAYS
find "$BACKUP_DIR" -name "*.gz" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "*.sql" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "*.rdb" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true

echo "✅ Limpeza concluída"

# =============================================================================
# VERIFICAÇÃO DE INTEGRIDADE
# =============================================================================
echo "🔍 Verificando integridade dos backups..."

# Verificar se os arquivos de backup existem e não estão corrompidos
BACKUP_FILES=(
    "$BACKUP_DIR/postgres_backup_$DATE.sql.gz"
    "$BACKUP_DIR/redis_backup_$DATE.rdb.gz"
    "$BACKUP_DIR/config_backup_$DATE.tar.gz"
    "$BACKUP_DIR/logs_backup_$DATE.tar.gz"
)

for file in "${BACKUP_FILES[@]}"; do
    if [ -f "$file" ]; then
        if gzip -t "$file" 2>/dev/null; then
            echo "✅ $file: OK"
        else
            echo "❌ $file: CORROMPIDO"
        fi
    else
        echo "⚠️ $file: NÃO ENCONTRADO"
    fi
done

# =============================================================================
# ESTATÍSTICAS
# =============================================================================
echo "📊 Estatísticas do backup..."

# Contar arquivos de backup
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "*.gz" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

echo "📁 Total de backups: $BACKUP_COUNT"
echo "💾 Tamanho total: $TOTAL_SIZE"

# =============================================================================
# NOTIFICAÇÃO (OPCIONAL)
# =============================================================================
if command -v curl &> /dev/null; then
    # Enviar notificação para webhook (se configurado)
    WEBHOOK_URL="${BACKUP_WEBHOOK_URL:-}"
    if [ -n "$WEBHOOK_URL" ]; then
        curl -X POST "$WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"event_type\": \"backup_completed\",
                \"timestamp\": \"$(date -Iseconds)\",
                \"backup_count\": $BACKUP_COUNT,
                \"total_size\": \"$TOTAL_SIZE\",
                \"project\": \"$PROJECT_NAME\"
            }" \
            --silent --output /dev/null || true
    fi
fi

# =============================================================================
# RELATÓRIO FINAL
# =============================================================================
echo ""
echo "🎉 BACKUP CONCLUÍDO COM SUCESSO!"
echo ""
echo "📁 Diretório: $BACKUP_DIR"
echo "📅 Data: $(date)"
echo "📊 Arquivos: $BACKUP_COUNT"
echo "💾 Tamanho: $TOTAL_SIZE"
echo ""
echo "📋 Arquivos criados:"
ls -lh "$BACKUP_DIR"/*"$DATE"* 2>/dev/null || echo "Nenhum arquivo encontrado"
echo ""
echo "🧹 Próxima limpeza: em $RETENTION_DAYS dias"
echo ""

# =============================================================================
# CRON JOB (OPCIONAL)
# =============================================================================
echo "⏰ Para configurar backup automático, adicione ao crontab:"
echo "   # Backup diário às 2h da manhã"
echo "   0 2 * * * cd $(pwd) && ./scripts/backup.sh >> logs/backup.log 2>&1"
echo "" 