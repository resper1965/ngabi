# 🚀 Chat Agents Platform

Plataforma de chat multi-agente com React frontend, FastAPI backend, n8n orchestration, Pinecone vectorization e Elasticsearch document store.

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Tailwind CSS + Vite
- **Backend**: FastAPI + Python 3.11 + Pydantic
- **Orchestration**: n8n
- **Vector Store**: Pinecone
- **Document Store**: Elasticsearch 7.17
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Containerization**: Docker + Docker Compose

## 📋 Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

## 🚀 Setup Rápido

### 1. Clone o repositório
```bash
git clone <repository-url>
cd ngabi
```

### 2. Configure as variáveis de ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### 3. Inicie os serviços
```bash
make up
# ou
docker-compose up -d
```

### 4. Acesse as aplicações
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **n8n**: http://localhost:5678
- **Elasticsearch**: http://localhost:9200

## 🛠️ Comandos Úteis

### Usando Makefile (Recomendado)
```bash
make help          # Mostra todos os comandos disponíveis
make build         # Constrói todas as imagens
make up            # Inicia todos os serviços
make down          # Para todos os serviços
make logs          # Mostra logs de todos os serviços
make health        # Verifica saúde dos serviços
make status        # Mostra status dos serviços
```

### Desenvolvimento
```bash
make dev-frontend  # Inicia frontend em modo desenvolvimento
make dev-backend   # Inicia backend em modo desenvolvimento
make install-frontend  # Instala dependências do frontend
make install-backend   # Instala dependências do backend
```

### Logs específicos
```bash
make logs-frontend     # Logs do frontend
make logs-backend      # Logs do backend
make logs-n8n          # Logs do n8n
make logs-db           # Logs do PostgreSQL
make logs-redis        # Logs do Redis
make logs-elasticsearch # Logs do Elasticsearch
```

### Limpeza e Manutenção
```bash
make clean             # Remove containers e volumes não utilizados
make clean-frontend    # Limpa cache do frontend
make clean-backend     # Limpa cache do backend
make backup-n8n        # Faz backup dos workflows do n8n
```

## 📁 Estrutura do Projeto

```
ngabi/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── App.tsx          # Componente principal
│   │   └── index.css        # Estilos globais
│   ├── package.json         # Dependências Node.js
│   └── Dockerfile           # Container do frontend
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── models/          # Modelos Pydantic
│   │   ├── routers/         # Rotas da API
│   │   └── main.py          # Aplicação principal
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile           # Container do backend
├── n8n/                     # Workflows e configurações n8n
├── docker-compose.yml       # Orquestração dos serviços
├── Makefile                 # Automação de comandos
├── env.example              # Exemplo de variáveis de ambiente
└── README.md               # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `env.example`:

```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:your_secure_password@postgres:5432/chat_agents
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=chat_agents

# Redis Configuration
REDIS_URL=redis://redis:6379

# Elasticsearch Configuration
ELASTICSEARCH_URL=http://elasticsearch:9200

# n8n Configuration
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_secure_n8n_password
WEBHOOK_URL=http://localhost:5678

# JWT Configuration
JWT_SECRET_KEY=your_super_secret_jwt_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_N8N_URL=http://localhost:5678

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🔒 Segurança

- ✅ CORS configurado
- ✅ Health checks implementados
- ✅ Usuário não-root nos containers
- ✅ Variáveis de ambiente para credenciais
- ⚠️ Elasticsearch security desabilitado (configurar para produção)

## 📊 Monitoramento

### Health Checks
Todos os serviços possuem health checks configurados:
- Frontend: Verifica se a aplicação está respondendo
- Backend: Endpoint `/health`
- n8n: Verifica se a interface está acessível
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`
- Elasticsearch: Cluster health check

### Logs
```bash
make logs          # Logs de todos os serviços
make monitor       # Monitoramento de recursos
```

## 🧪 Testes

```bash
make test          # Executa todos os testes
make lint          # Executa linters
make format        # Formata código
```

## 🚀 Deploy

### Desenvolvimento
```bash
make up
```

### Produção
```bash
make prod-build
make prod-up
```

## 📈 Roadmap

### ✅ Concluído
- [x] Estrutura básica do projeto
- [x] Docker Compose com todos os serviços
- [x] Frontend React com TypeScript
- [x] Backend FastAPI com Pydantic
- [x] Health checks implementados
- [x] CORS configurado
- [x] Makefile para automação
- [x] Componentes básicos do frontend

### 🚧 Em Desenvolvimento
- [ ] Autenticação JWT completa
- [ ] Integração com Pinecone
- [ ] Workflows n8n avançados
- [ ] Testes automatizados
- [ ] CI/CD pipeline

### 📋 Próximos Passos
- [ ] Implementar autenticação JWT
- [ ] Adicionar testes automatizados
- [ ] Configurar CI/CD
- [ ] Implementar monitoramento
- [ ] Documentação da API
- [ ] Dashboard de administração

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato com a equipe de desenvolvimento. 