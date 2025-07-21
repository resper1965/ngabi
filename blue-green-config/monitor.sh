#!/bin/bash

echo "📊 Monitoramento Blue-Green Deployment"
echo "======================================"

# Verificar containers rodando
echo "🐳 Containers rodando:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(backend|proxy)"

echo ""
echo "🌐 Status do proxy:"
curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health

echo ""
echo "📈 Métricas:"
curl -s http://localhost:8000/metrics | grep -E "(http_requests_total|http_request_duration_seconds)" | head -5

echo ""
echo "🔍 Health checks:"
echo "Backend Blue: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health)"
echo "Backend Green: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8002/health 2>/dev/null || echo "N/A")"
echo "Proxy: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)"
