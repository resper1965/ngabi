# chat-multi-agents

**Visão Geral**  
Plataforma de chat multi-agentes (React, FastAPI, n8n, Pinecone, Elasticsearch).

## Tecnologias  
- Frontend: React + TypeScript + Tailwind + shadcn/ui  
- Backend: FastAPI + Uvicorn + Pydantic  
- Orquestração: n8n  
- Vetorização: Pinecone  
- Document Store: Elasticsearch on-premises  

## Setup Rápido  
1. Clone o repositório  
2. Copie `.env.example` para `.env` e preencha as chaves (incluindo `WEBHOOK_URL`)  
3. `docker-compose up --build`  
4. Frontend: http://localhost:3000 | API: http://localhost:8000 | n8n: ${WEBHOOK_URL}  

## Roadmap  
- v0.1.0: Esqueleto backend, frontend, n8n  
- v0.2.0: Módulos de tenancy, usuários e branding  
- v0.3.0: Geração de conteúdo longo e CI/CD 