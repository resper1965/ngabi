#!/bin/bash

# Script para configurar alertas do Chat App
# Uso: ./setup-alerts.sh [slack_webhook_url] [slack_channel]

set -e

echo "🚀 Configurando alertas do Chat App..."

# Verificar argumentos
SLACK_WEBHOOK_URL=${1:-"YOUR_SLACK_WEBHOOK_URL"}
SLACK_CHANNEL=${2:-"#alerts"}

if [ "$SLACK_WEBHOOK_URL" = "YOUR_SLACK_WEBHOOK_URL" ]; then
    echo "⚠️  Aviso: Usando URL de webhook padrão. Configure a URL real do Slack."
fi

# Função para substituir placeholders
replace_placeholder() {
    local file=$1
    local placeholder=$2
    local value=$3
    
    if [ "$value" != "YOUR_SLACK_WEBHOOK_URL" ]; then
        sed -i "s|$placeholder|$value|g" "$file"
        echo "✅ Configurado $placeholder em $file"
    else
        echo "⚠️  Mantendo placeholder $placeholder em $file"
    fi
}

# Configurar Grafana alerts
echo "📊 Configurando alertas do Grafana..."
replace_placeholder "grafana-alerts.yml" "YOUR_SLACK_WEBHOOK_URL" "$SLACK_WEBHOOK_URL"
replace_placeholder "grafana-alerts.yml" "#alerts" "$SLACK_CHANNEL"

# Configurar Alertmanager
echo "🔔 Configurando Alertmanager..."
replace_placeholder "alertmanager.yml" "YOUR_SLACK_WEBHOOK_URL" "$SLACK_WEBHOOK_URL"
replace_placeholder "alertmanager.yml" "#alerts" "$SLACK_CHANNEL"

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p /etc/grafana/provisioning/alerting
mkdir -p /etc/alertmanager/templates

# Copiar arquivos de configuração
echo "📋 Copiando arquivos de configuração..."
cp grafana-alerts.yml /etc/grafana/provisioning/alerting/
cp alertmanager.yml /etc/alertmanager/

# Verificar se Prometheus está configurado
if [ -f "prometheus.yml" ]; then
    echo "✅ Arquivo prometheus.yml encontrado"
else
    echo "❌ Arquivo prometheus.yml não encontrado. Execute primeiro o setup do Prometheus."
    exit 1
fi

# Verificar se as métricas estão sendo coletadas
echo "🔍 Verificando métricas..."
if command -v curl >/dev/null 2>&1; then
    echo "Testando endpoint de métricas..."
    if curl -s http://localhost:8000/metrics | grep -q "http_requests_total"; then
        echo "✅ Métricas estão sendo coletadas"
    else
        echo "⚠️  Métricas não encontradas. Verifique se o app está rodando."
    fi
else
    echo "⚠️  curl não encontrado. Não foi possível verificar métricas."
fi

# Criar arquivo de configuração do Docker Compose
echo "🐳 Criando docker-compose.alerts.yml..."
cat > docker-compose.alerts.yml << EOF
version: '3.8'

services:
  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
      - '--web.listen-address=:9093'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana-alerts.yml:/etc/grafana/provisioning/alerting/grafana-alerts.yml
      - ./grafana-dashboard.json:/etc/grafana/provisioning/dashboards/dashboard.json
    restart: unless-stopped

volumes:
  alertmanager_data:
  grafana_data:
EOF

# Criar script de teste
echo "🧪 Criando script de teste..."
cat > test-alerts.sh << 'EOF'
#!/bin/bash

echo "🧪 Testando alertas..."

# Simular alta latência
echo "Simulando alta latência..."
for i in {1..10}; do
    curl -X POST http://localhost:8000/api/v1/chat/ \
        -H "Content-Type: application/json" \
        -H "X-Tenant-ID: test-tenant" \
        -d '{"message": "test", "agent_id": "test-agent"}' &
done

# Simular erros
echo "Simulando erros..."
for i in {1..5}; do
    curl -X POST http://localhost:8000/api/v1/chat/ \
        -H "Content-Type: application/json" \
        -H "X-Tenant-ID: test-tenant" \
        -d '{"invalid": "data"}' &
done

wait
echo "✅ Teste concluído. Verifique os alertas no Slack e Grafana."
EOF

chmod +x test-alerts.sh

# Criar arquivo de documentação
echo "📚 Criando documentação..."
cat > ALERTS_README.md << 'EOF'
# Configuração de Alertas - Chat App

## Visão Geral

Este sistema de alertas monitora a aplicação Chat App e envia notificações para o Slack quando detecta problemas de performance ou disponibilidade.

## Alertas Configurados

### Alertas Críticos
1. **Chat Request Latency High** (> 2s)
   - Dispara quando a latência p95 excede 2 segundos
   - Duração: 2 minutos
   - Canal: #critical-alerts

2. **Chat Error Rate High** (> 5%)
   - Dispara quando a taxa de erro excede 5%
   - Duração: 1 minuto
   - Canal: #critical-alerts

### Alertas de Aviso
1. **Chat Request Latency Warning** (> 1.5s)
2. **Chat Error Rate Warning** (> 3%)
3. **Chat QPS High** (> 100 req/s)
4. **Cache Hit Rate Low** (< 80%)
5. **Rate Limit Violations High** (> 10/s)
6. **Memory Usage High** (> 2GB)
7. **Active Connections High** (> 1000)

## Configuração

### 1. Slack
- Configure o webhook URL no arquivo `grafana-alerts.yml`
- Configure o canal no arquivo `alertmanager.yml`

### 2. Grafana
- Acesse: http://localhost:3000
- Login: admin / admin123
- Importe o dashboard: `grafana-dashboard.json`

### 3. Alertmanager
- Acesse: http://localhost:9093
- Configure silenciamentos e agrupamentos

## Teste

Execute o script de teste:
```bash
./test-alerts.sh
```

## Manutenção

### Silenciar Alertas
```bash
# Via Alertmanager UI
curl -X POST http://localhost:9093/api/v1/silences \
  -H "Content-Type: application/json" \
  -d '{
    "matchers": [{"name": "alertname", "value": "Chat Request Latency Warning"}],
    "startsAt": "2024-01-01T00:00:00Z",
    "endsAt": "2024-01-01T23:59:59Z",
    "createdBy": "admin",
    "comment": "Maintenance window"
  }'
```

### Verificar Status
```bash
# Grafana
curl http://localhost:3000/api/health

# Alertmanager
curl http://localhost:9093/api/v1/status

# Prometheus
curl http://localhost:9090/api/v1/status/config
```

## Troubleshooting

### Alertas não disparam
1. Verifique se as métricas estão sendo coletadas
2. Verifique a configuração do webhook do Slack
3. Verifique os logs do Grafana e Alertmanager

### Muitos alertas
1. Ajuste os thresholds nos arquivos de configuração
2. Configure agrupamento mais agressivo
3. Configure silenciamentos para horários de manutenção
EOF

echo "✅ Configuração de alertas concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure a URL do webhook do Slack nos arquivos"
echo "2. Execute: docker-compose -f docker-compose.alerts.yml up -d"
echo "3. Acesse Grafana: http://localhost:3000 (admin/admin123)"
echo "4. Acesse Alertmanager: http://localhost:9093"
echo "5. Teste com: ./test-alerts.sh"
echo ""
echo "📚 Documentação: ALERTS_README.md" 