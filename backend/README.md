# n.Gabi Backend

Backend da aplicação n.Gabi com bancos integrados (PostgreSQL, Redis, Elasticsearch).

## 🏗️ Arquitetura

Este backend inclui a aplicação FastAPI principal:

- **FastAPI** - API principal do n.Gabi
- **Redis** - Cache e sessões (opcional)
- **Bancos externos** - PostgreSQL e Elasticsearch como serviços separados

## 🚀 Deploy no Easypanel

### Configuração do Serviço

1. **Tipo de Fonte**: GitHub
2. **Proprietário**: `resper1965`
3. **Repositório**: `ngabi`
4. **Branch**: `main`
5. **Caminho**: `/backend`

### Configuração de Build

1. **Tipo de Construção**: Dockerfile
2. **Arquivo**: `Dockerfile`
3. **Caminho de Build**: `/backend`

### Variáveis de Ambiente

```env
REDIS_URL=redis://redis:6379
JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKey123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br
```

### Configuração de Domínio

- **Host**: `api.ngabi.ness.tec.br`
- **Porta**: `8000`
- **Protocolo**: `HTTP`
- **HTTPS**: Habilitado

## 🔧 Desenvolvimento Local

### Pré-requisitos

- Docker
- Docker Compose

### Executar Localmente

```bash
# Na pasta backend
docker-compose up --build
```

### Acessar Serviços

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📊 Health Checks

- **API**: `GET /health`
- **Cache**: `GET /cache/health`
- **Métricas**: `GET /metrics`

## 🔍 Logs

Os logs de todos os serviços são exibidos no console do container:

```bash
# Ver logs do container
docker logs <container_id>
```

## 🛠️ Troubleshooting

### Problemas Comuns

1. **PostgreSQL não inicia**
   - Verificar permissões do diretório `/var/lib/postgresql/data`
   - Verificar se a porta 5432 está livre

2. **Redis não inicia**
   - Verificar se a porta 6379 está livre
   - Verificar configuração do Redis

3. **Elasticsearch não inicia**
   - Verificar se há memória suficiente (mínimo 512MB)
   - Verificar se a porta 9200 está livre

### Comandos Úteis

```bash
# Verificar status dos serviços
docker exec <container_id> ps aux

# Conectar ao PostgreSQL
docker exec -it <container_id> su - postgres -c "psql -d chat_agents"

# Conectar ao Redis
docker exec -it <container_id> redis-cli

# Verificar Elasticsearch
docker exec <container_id> curl http://localhost:9200/_cluster/health
```

## 📝 Notas

- Todos os dados são persistidos em volumes Docker
- O container pode demorar alguns minutos para inicializar completamente
- Os serviços são iniciados em sequência: PostgreSQL → Redis → Elasticsearch → FastAPI 