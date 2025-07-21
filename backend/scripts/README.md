# Scripts do Backend

Este diretório contém scripts utilitários para gerenciar o banco de dados e popular dados de exemplo.

## 📁 Arquivos

### `seed.py`
Script principal para popular o banco de dados com dados de exemplo para desenvolvimento.

### `run_migrations.py`
Script para executar migrations do Alembic automaticamente.

### `create_initial_migration.py`
Script para criar a revisão inicial do Alembic (quando disponível).

## 🚀 Como Usar

### 1. Configurar Ambiente

Primeiro, configure o arquivo `.env` na raiz do backend:

```bash
# Copiar exemplo
cp .env.example .env

# Editar com suas configurações
nano .env
```

**Variáveis obrigatórias:**
```env
# Opção 1: URL completa
POSTGRES_URL=postgresql://user:password@host:port/database

# Opção 2: Configuração individual
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chat_agents
```

### 2. Executar Migrations

```bash
# Executar migrations automaticamente
python scripts/run_migrations.py

# Ou manualmente
alembic upgrade head
```

### 3. Popular Dados de Exemplo

```bash
# Executar seed
python scripts/seed.py
```

## 📊 Dados Criados pelo Seed

### 🏢 Tenants (Organizações)
- **Empresa ABC Ltda** (empresa-abc) - Soluções jurídicas
- **Startup XYZ** (startup-xyz) - Fintech
- **Consultoria Legal** (consultoria-legal) - Advocacia
- **TechCorp Solutions** (techcorp) - Tecnologia

### 👤 Usuários
- `admin@empresa-abc.com` / `admin123` (admin)
- `user@empresa-abc.com` / `user123` (user)
- `dev@empresa-abc.com` / `dev123` (developer)
- `admin@startup-xyz.com` / `admin123` (admin)
- `dev@startup-xyz.com` / `dev123` (developer)
- `advogado@consultoria-legal.com` / `adv123` (admin)
- `assistente@consultoria-legal.com` / `ass123` (user)
- `admin@techcorp.com` / `admin123` (admin)

### 🤖 Agentes de IA
- **LexAI** - Assistente jurídico (Empresa ABC)
- **JurisBot** - Consultoria jurídica (Consultoria Legal)
- **FinBot** - Análise financeira (Startup XYZ)
- **InvestAI** - Investimentos (Startup XYZ)
- **SuporteAI** - Suporte ao cliente (TechCorp)
- **TechHelper** - Suporte técnico (TechCorp)

### 🎨 Configurações de Branding
Cada tenant recebe configurações personalizadas:
- Nome do orquestrador
- Cores do tema (primária e secundária)
- Informações de contato
- Caminho do logo

## 🔧 Funcionalidades do Script

### ✅ Verificações Automáticas
- Carrega configurações do `.env`
- Testa conexão com PostgreSQL
- Verifica se dados já existem (não duplica)
- Tratamento de erros com rollback

### 🔒 Segurança
- Senhas hasheadas com bcrypt
- URLs mascaradas no log
- Transações seguras

### 📈 Relatórios
- Resumo detalhado dos dados criados
- Credenciais de teste
- Próximos passos sugeridos

## 🐛 Troubleshooting

### Erro de Conexão
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão manual
psql -h localhost -U postgres -d chat_agents
```

### Erro de Configuração
```bash
# Verificar variáveis de ambiente
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('POSTGRES_URL:', os.getenv('POSTGRES_URL'))"
```

### Erro de Permissão
```bash
# Tornar script executável
chmod +x scripts/seed.py

# Executar com python explicitamente
python3 scripts/seed.py
```

## 📝 Logs de Exemplo

```
🌱 Iniciando seed do banco de dados...
============================================================
📋 Carregando configurações...
✅ Arquivo .env carregado: /path/to/backend/.env
🔌 Conectando ao banco de dados...
   URL: postgresql://postgres:***@localhost:5432/chat_agents
✅ Conectado ao PostgreSQL: PostgreSQL 15.5

🏢 Criando tenants...
   ✅ Tenant criado: Empresa ABC Ltda (empresa-abc)
   ✅ Tenant criado: Startup XYZ (startup-xyz)
   ✅ Tenant criado: Consultoria Legal (consultoria-legal)
   ✅ Tenant criado: TechCorp Solutions (techcorp)

👤 Criando usuários...
   ✅ Usuário criado: admin@empresa-abc.com (admin)
   ✅ Usuário criado: user@empresa-abc.com (user)
   ...

🤖 Criando agentes...
   ✅ Agente criado: LexAI (Assistente jurídico especializado...)
   ✅ Agente criado: FinBot (Assistente financeiro para análise...)
   ...

🎨 Criando configurações...
   ✅ Configurações criadas: Assistente Jurídico ABC
   ✅ Configurações criadas: FinBot XYZ
   ...

============================================================
📊 RESUMO DOS DADOS CRIADOS
============================================================
🏢 Tenants: 4
   - Empresa ABC Ltda (empresa-abc)
   - Startup XYZ (startup-xyz)
   ...

👤 Usuários: 8
   - admin@empresa-abc.com (admin)
   - user@empresa-abc.com (user)
   ...

🤖 Agentes: 6
   - LexAI
   - FinBot
   ...

🎨 Configurações: 4
   - Assistente Jurídico ABC
   - FinBot XYZ
   ...

🔑 CREDENCIAIS DE TESTE
------------------------------
   admin@empresa-abc.com / admin123 (admin)
   user@empresa-abc.com / user123 (user)
   ...

🚀 PRÓXIMOS PASSOS
------------------------------
1. Testar conexão com o banco
2. Executar aplicação FastAPI
3. Acessar endpoints de autenticação
4. Testar funcionalidades por tenant

🎉 Seed concluído com sucesso!
```

## 🔄 Reexecutar Seed

Para reexecutar o seed (por exemplo, após limpar o banco):

```bash
# Limpar banco
alembic downgrade base
alembic upgrade head

# Reexecutar seed
python scripts/seed.py
```

O script detecta dados existentes e não os duplica, então é seguro executar múltiplas vezes. 