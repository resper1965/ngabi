# 🚀 n.Gabi - Chat Agents Platform

Plataforma de chat multi-agente com React frontend e FastAPI backend integrado ao Supabase.

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Tailwind CSS + Vite
- **Backend**: FastAPI + Python 3.11 + Pydantic
- **Database**: Supabase (PostgreSQL + Auth + Realtime)
- **Cache**: Redis (opcional)
- **Containerization**: Docker + Docker Compose

## 📋 Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)
- Conta no Supabase

## 🚀 Setup Rápido

### 1. Clone o repositório
```bash
git clone <repository-url>
cd ngabi
```

### 2. Configure as variáveis de ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações do Supabase
```

### 3. Configure o Supabase
- Crie um projeto no Supabase
- Configure as tabelas usando o arquivo `backend/SUPABASE-SETUP.md`
- Copie as credenciais para o arquivo `.env`

### 4. Inicie os serviços
```bash
docker-compose up -d
```

### 5. Acesse as aplicações
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 🛠️ Comandos Úteis

### Docker Compose
```bash
docker-compose up -d          # Inicia todos os serviços
docker-compose down           # Para todos os serviços
docker-compose logs           # Mostra logs de todos os serviços
docker-compose ps             # Mostra status dos serviços
```

### Desenvolvimento
```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
```

### Health Checks
```bash
curl http://localhost:8000/health    # Backend health
curl http://localhost:3000           # Frontend health
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
│   │   ├── routers/         # Endpoints da API
│   │   ├── schemas/         # Modelos Pydantic
│   │   ├── core/            # Configurações e utilitários
│   │   └── main.py          # Aplicação principal
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile           # Container do backend
├── docker-compose.yml       # Orquestração dos serviços
└── env.example              # Exemplo de variáveis de ambiente
```

## 🔧 Configuração do Supabase

### 1. Criar Projeto
- Acesse [supabase.com](https://supabase.com)
- Crie um novo projeto
- Anote a URL e chave anônima

### 2. Configurar Tabelas
Execute os comandos SQL do arquivo `backend/SUPABASE-SETUP.md` no SQL Editor do Supabase.

### 3. Configurar Variáveis
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

## 🚀 Deploy

### Easypanel
1. Configure os serviços no Easypanel
2. Use as variáveis do arquivo `backend/SUPABASE-SIMPLE-CONFIG.md`
3. Deploy dos containers

### Variáveis de Ambiente
```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## 📚 Documentação

- [Supabase Setup](backend/SUPABASE-SETUP.md)
- [Environment Variables](backend/SUPABASE-SIMPLE-CONFIG.md)
- [API Documentation](http://localhost:8000/docs)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request 
