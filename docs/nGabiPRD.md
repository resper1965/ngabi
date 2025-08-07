# 📋 PRD (Product Requirements Document) - n.Gabi Chat Agents Platform

## 1. **Resumo Executivo**

### Visão Geral do Produto
O **n.Gabi** é uma plataforma SaaS de chat multi-agente que permite organizações criarem e gerenciarem chatbots inteligentes com suporte a múltiplos tenants, autenticação integrada e sistema de cache distribuído.

### Problemas Resolvidos
- **Complexidade de Implementação**: Simplifica a criação de chatbots empresariais
- **Multi-tenancy**: Permite que múltiplas organizações usem a mesma plataforma
- **Escalabilidade**: Arquitetura containerizada com cache Redis
- **Integração**: Conecta-se facilmente com LLMs e APIs externas

### Para Quem é Este Sistema?
- **Empresas SaaS** que precisam de chatbots para atendimento ao cliente
- **Desenvolvedores** que querem uma solução pronta para chat AI
- **Organizações** que precisam de múltiplos agentes para diferentes propósitos

### Objetivos Principais
1. Fornecer uma plataforma completa de chat AI multi-tenant
2. Simplificar a criação e gerenciamento de agentes conversacionais
3. Oferecer escalabilidade e performance através de cache e rate limiting
4. Prover uma interface moderna e responsiva

---

## 2. **Arquitetura Técnica**

### Linguagens e Frameworks
- **Frontend**: React 18 + TypeScript + Tailwind CSS + Vite
- **Backend**: FastAPI + Python 3.11 + Pydantic
- **Database**: Supabase (PostgreSQL + Auth + Realtime)
- **Cache**: Redis 7
- **Containerização**: Docker + Docker Compose

### Estrutura do Projeto
```
ngabi/
├── frontend/                 # React SPA
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── services/       # Serviços de API
│   │   └── lib/            # Utilitários
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── routers/        # Endpoints da API
│   │   ├── schemas/        # Modelos Pydantic
│   │   ├── core/           # Configurações e cache
│   │   ├── middleware/     # Middlewares customizados
│   │   └── repositories/   # Camada de acesso a dados
└── docker-compose.yml      # Orquestração
```

### Bancos de Dados e Ferramentas
- **Supabase**: PostgreSQL cloud com autenticação e RLS
- **Redis**: Cache distribuído e rate limiting
- **Prometheus**: Métricas e observabilidade

### Serviços e Microsserviços
- **Frontend Service**: React SPA (porta 3000)
- **Backend Service**: FastAPI API (porta 8000)
- **Redis Service**: Cache e sessões (porta 6379)

### Padrões Implementados
- **Autenticação**: Supabase Auth com JWT
- **Cache**: Redis com TTL configurável
- **Rate Limiting**: Por tenant e usuário
- **CI/CD**: GitHub Actions com testes automatizados
- **Health Checks**: Endpoints de monitoramento

---

## 3. **Funcionalidades Identificadas**

### Módulos Principais

#### **Chat Module** (`/api/v1/chat`)
- `POST /` - Envio de mensagens
- `POST /stream` - Chat em streaming
- `POST /batch` - Processamento em lote
- `POST /user-chat` - Chat baseado em usuário
- `POST /role-based-chat` - Chat baseado em papel
- `GET /history` - Histórico de conversas
- `GET /cache/stats` - Estatísticas de cache
- `DELETE /cache/clear` - Limpeza de cache

#### **Authentication Module** (`/api/v1/auth`)
- Endpoints de autenticação via Supabase
- Gerenciamento de sessões
- Validação de tokens JWT


- Sistema de evolução de agentes
- Aprendizado contínuo
- Otimização de prompts

### Workflows Principais

#### **Fluxo de Chat**
1. Usuário envia mensagem via frontend
2. Backend valida autenticação e tenant
3. Sistema verifica cache para resposta similar
4. Se não encontrado, processa com LLM
5. Salva resposta no cache e histórico
6. Retorna resposta ao usuário

#### **Fluxo de Autenticação**
1. Usuário faz login via Supabase Auth
2. Sistema gera JWT token
3. Token é validado em cada requisição
4. Rate limiting aplicado por tenant/usuário

---

## 4. **Fluxo do Usuário**

### Telas Identificadas
- **Login** (`/login`) - Autenticação de usuários
- **Dashboard** (`/`) - Interface principal com navegação
- **Chat** (`/chat`) - Interface de conversa com agentes
- **Tenants** (`/tenants`) - Gerenciamento de organizações
- **Users** (`/users`) - Gerenciamento de usuários
- **Branding** (`/branding`) - Personalização visual
- **Settings** (`/settings`) - Configurações do sistema


### Papéis de Usuário
- **Admin**: Acesso completo ao sistema
- **User**: Acesso limitado ao chat e funcionalidades básicas
- **Tenant Admin**: Gerenciamento de sua organização

### Interação do Usuário
1. **Login** → Autenticação via Supabase
2. **Dashboard** → Seleção de funcionalidade
3. **Chat** → Conversa com agentes AI
4. **Configuração** → Personalização de agentes e branding
5. **Administração** → Gerenciamento de tenants e usuários

---

## 5. **Automação, Bots ou IA**

### Agentes Inteligentes
- **Sistema de Agentes**: Múltiplos chatbots configuráveis
- **Modelos LLM**: Suporte a diferentes modelos (GPT-3.5-turbo padrão)
- **Prompts Dinâmicos**: Templates de prompt configuráveis
- **Contexto de Conversa**: Manutenção de histórico de sessão

### Algoritmos e Processamento
- **Cache Inteligente**: Cache baseado em similaridade de queries
- **Rate Limiting**: Limitação de requisições por tenant/usuário
- **Métricas**: Coleta de dados de performance e uso
- **Evolução**: Sistema de aprendizado contínuo dos agentes

### Funcionalidades AI
- **Processamento de Linguagem Natural**: Integração com LLMs
- **Análise de Sentimento**: Processamento de contexto emocional
- **Geração de Respostas**: Respostas contextualizadas
- **Otimização de Prompts**: Melhoria contínua dos templates

---

## 6. **Integrações Externas**

### APIs Externas
- **Supabase**: Banco de dados, autenticação e real-time
- **LLM APIs**: Integração com modelos de linguagem (configurável)
- **Redis**: Cache distribuído e sessões

### Serviços de Autenticação
- **Supabase Auth**: Sistema completo de autenticação
- **JWT Tokens**: Validação de sessões
- **Row Level Security (RLS)**: Segurança por tenant

### Webhooks e Terceiros
- **Não identificado neste repositório**: Sistema de webhooks não implementado
- **Notificações**: Sistema de notificações não encontrado
- **Integrações**: APIs de terceiros não configuradas

---

## 7. **Requisitos Não Funcionais**

### Performance e Escalabilidade
- **Cache Redis**: Reduz latência de respostas
- **Rate Limiting**: Protege contra sobrecarga
- **Health Checks**: Monitoramento de saúde dos serviços
- **Containerização**: Facilita escalabilidade horizontal

### Segurança
- **Supabase RLS**: Segurança por tenant
- **JWT Validation**: Autenticação segura
- **CORS Configuration**: Controle de origens
- **Input Validation**: Validação via Pydantic

### Observabilidade
- **Prometheus Metrics**: Métricas de performance
- **Structured Logging**: Logs estruturados
- **Health Endpoints**: `/health`, `/metrics`, `/cache/health`
- **Error Tracking**: Logs de erro detalhados

### Deploy e Infraestrutura
- **Docker Compose**: Orquestração local
- **GitHub Actions**: CI/CD automatizado
- **Easypanel**: Deploy em produção
- **Environment Variables**: Configuração flexível

---

## 8. **Roadmap Sugerido**

### Fase 1 - Estabilização (1-2 meses)
- [ ] Completar implementação de testes com Supabase
- [ ] Implementar sistema de webhooks
- [ ] Adicionar sistema de notificações
- [ ] Melhorar documentação da API

### Fase 2 - Funcionalidades Avançadas (2-3 meses)
- [ ] Sistema de analytics e relatórios
- [ ] Integração com múltiplos LLMs
- [ ] Sistema de templates de agentes
- [ ] API de administração completa

### Fase 3 - Escalabilidade (3-4 meses)
- [ ] Implementar filas de processamento (Celery/RQ)
- [ ] Sistema de backup automático
- [ ] Monitoramento avançado (Grafana)
- [ ] Load balancing e auto-scaling

### Fase 4 - Inteligência Avançada (4-6 meses)
- [ ] Sistema de aprendizado contínuo
- [ ] Análise de sentimento avançada
- [ ] Integração com bases de conhecimento
- [ ] Sistema de recomendação de agentes

---

## 9. **Riscos Potenciais**

### Acoplamentos Fortes
- **Supabase Dependency**: Forte dependência do Supabase para dados e auth
- **Redis Dependency**: Cache crítico para performance
- **Single LLM Provider**: Dependência de um provedor de LLM

### Falta de Implementação
- **Testes**: Testes de integração incompletos
- **Webhooks**: Sistema de notificações não implementado
- **Analytics**: Métricas de negócio limitadas
- **Backup**: Estratégia de backup não definida

### Questões de Segurança
- **Rate Limiting**: Implementação básica, pode ser contornada
- **Input Sanitization**: Validação pode ser melhorada
- **Error Handling**: Tratamento de erros pode expor informações sensíveis
- **Audit Logs**: Sistema de auditoria não implementado

### Questões de Escalabilidade
- **Single Instance**: Sem load balancing
- **Database Scaling**: Limitações do Supabase para grandes volumes
- **Cache Strategy**: Estratégia de cache pode ser otimizada
- **Monitoring**: Observabilidade limitada

---

## **Conclusão**

O n.Gabi é uma plataforma sólida e bem arquitetada para chat multi-agente, com uma base técnica robusta usando tecnologias modernas. A arquitetura containerizada e a integração com Supabase fornecem uma base sólida para crescimento. As principais áreas de melhoria estão na implementação de testes, sistema de webhooks, e funcionalidades avançadas de analytics e monitoramento.

A plataforma está pronta para uso em produção com configuração adequada, mas beneficiaria de investimento nas áreas de teste, segurança e escalabilidade para suportar crescimento significativo.

---

**Documento gerado em:** $(date)
**Versão:** 1.0
**Projeto:** n.Gabi Chat Agents Platform Documento gerado em: Tue Jul 22 08:45:28 -03 2025
