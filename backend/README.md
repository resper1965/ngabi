# n.Gabi Backend

Backend da aplicação n.Gabi com Supabase externo.

## 🏗️ Arquitetura

Este backend inclui a aplicação FastAPI principal:

- **FastAPI** - API principal do n.Gabi
- **Supabase** - Banco de dados PostgreSQL + Auth + Real-time (externo)
- **Redis** - Cache e sessões (opcional)

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
# Supabase Configuration (externo)
SUPABASE_URL=https://sup.ngabi.ness.tec.br
SUPABASE_ANON_KEY=your-anon-key

# Redis Configuration (opcional)
REDIS_URL=redis://ngabi-redis:6379

# CORS Configuration
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://chat.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br,https://sup.ngabi.ness.tec.br

# Application Configuration
APP_NAME=n.Gabi Backend
APP_VERSION=2.0.0
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

1. **Supabase não conecta**
   - Verificar se `SUPABASE_URL` e `SUPABASE_ANON_KEY` estão corretos
   - Verificar se o Supabase está rodando

2. **Redis não conecta**
   - Verificar se a porta 6379 está livre
   - Verificar configuração do Redis

### Comandos Úteis

```bash
# Verificar status dos serviços
docker exec <container_id> ps aux

# Conectar ao Redis
docker exec -it <container_id> redis-cli

# Verificar Supabase
curl https://sup.ngabi.ness.tec.br/rest/v1/
```

## 📝 Notas

- O backend usa Supabase externo (sem PostgreSQL interno)
- Redis é opcional para cache
- Todos os dados são gerenciados pelo Supabase
- O container pode demorar alguns minutos para inicializar completamente

## 🎯 Dependências

- **Supabase**: Banco de dados, autenticação e real-time
- **Redis**: Cache (opcional)
- **FastAPI**: API framework
- **Uvicorn**: ASGI server 