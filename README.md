# n.Gabi - Chat Multi-Agente

Plataforma de chat inteligente com múltiplos agentes, construída com React, FastAPI e Supabase.

## 🚀 Tecnologias

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python 3.13
- **Database**: Supabase (PostgreSQL)
- **Cache**: Redis
- **Deploy**: EasyPanel + Traefik

## 📁 Estrutura do Projeto

```
ngabi/
├── frontend/          # Aplicação React
├── backend/           # API FastAPI
├── docs/             # Documentação
├── scripts/          # Scripts utilitários
└── docker-compose.yml
```

## 🛠️ Desenvolvimento

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+
- Python 3.13+

### Executar Localmente
```bash
# Clone o repositório
git clone https://github.com/resper1965/ngabi.git
cd ngabi

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute com Docker Compose
docker-compose up -d
```

### URLs Locais
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Redis**: localhost:6379

## 🚀 Produção

### Deploy no EasyPanel
```bash
# Build para produção
./build-production.sh

# Siga as instruções geradas para deploy no EasyPanel
```

### URLs de Produção
- **Frontend**: https://ngabi.ness.tec.br
- **Backend**: https://api.ngabi.ness.tec.br

## 📚 Documentação

- [PRD (Product Requirements Document)](docs/nGabiPRD.md)
- [Schema do Banco de Dados](docs/supabase-schema.sql)

## 🔧 Scripts Úteis

- `./build-production.sh` - Build para produção
- `docker-compose up -d` - Executar localmente
- `docker-compose down` - Parar serviços

## 📄 Licença

Este projeto é privado e proprietário.
