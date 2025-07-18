# Backend - Chat Multi-Agente

## 🗄️ Configuração do Banco de Dados

### Pré-requisitos
- PostgreSQL 15+
- Python 3.11+
- Alembic

### 1. Configuração do Ambiente

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp ../env.example .env
# Editar .env com suas configurações de banco
```

### 2. Configuração do Alembic

O Alembic está configurado para usar automaticamente a variável `POSTGRES_URL` do arquivo `.env`:

```bash
# Se você tem POSTGRES_URL no .env:
POSTGRES_URL=postgresql://user:password@host:port/database

# Ou configure individualmente:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chat_agents
```

### 3. Executar Migrations

```bash
# Executar migrations automaticamente
python scripts/run_migrations.py

# Ou manualmente:
alembic upgrade head
```

### 4. Inserir Dados de Teste

```bash
# Executar seed com dados de teste
python scripts/seed_data.py
```

## 📊 Schema do Banco

### Tabelas Principais

1. **`tenants`** - Organizações/empresas
   - `id` (UUID) - Chave primária
   - `name` (TEXT) - Nome da empresa
   - `subdomain` (TEXT) - Subdomínio único
   - `created_at` (TIMESTAMP) - Data de criação

2. **`users`** - Usuários por tenant
   - `id` (UUID) - Chave primária
   - `tenant_id` (UUID) - Referência ao tenant
   - `email` (TEXT) - Email único por tenant
   - `password_hash` (TEXT) - Hash da senha
   - `role` (TEXT) - 'admin', 'user', 'developer'
   - `is_active` (BOOLEAN) - Status do usuário

3. **`agents`** - Agentes de IA por tenant
   - `id` (UUID) - Chave primária
   - `tenant_id` (UUID) - Referência ao tenant
   - `name` (TEXT) - Nome do agente
   - `config` (JSONB) - Configuração do agente

4. **`tenant_settings`** - Configurações de branding
   - `tenant_id` (UUID) - Chave primária e referência
   - `logo_path` (TEXT) - Caminho do logo
   - `orchestrator_name` (TEXT) - Nome do orquestrador
   - `theme_primary` (CHAR(7)) - Cor primária
   - `theme_secondary` (CHAR(7)) - Cor secundária

5. **`chat_history`** - Histórico de conversas
   - `id` (BIGSERIAL) - Chave primária
   - `tenant_id` (UUID) - Referência ao tenant
   - `user_id` (UUID) - Referência ao usuário
   - `agent_id` (UUID) - Referência ao agente
   - `message` (TEXT) - Mensagem do usuário
   - `response` (TEXT) - Resposta do agente
   - `chat_mode` (TEXT) - 'UsoCotidiano' ou 'EscritaLonga'

6. **`messages`** - Mensagens individuais (opcional)
   - `id` (BIGSERIAL) - Chave primária
   - `chat_id` (BIGINT) - Referência ao chat
   - `speaker` (TEXT) - 'user' ou 'agent'
   - `content` (TEXT) - Conteúdo da mensagem

## 🔒 Isolamento por Tenant

O sistema implementa isolamento lógico por tenant:

- Todas as queries incluem automaticamente `tenant_id`
- Repositórios base garantem isolamento
- Middleware de sessão configura tenant_id
- Constraints de banco previnem vazamento de dados

## 🧪 Dados de Teste

### Tenants Criados
- **Empresa ABC Ltda** (subdomain: empresa-abc)
- **Startup XYZ** (subdomain: startup-xyz)
- **Consultoria Legal** (subdomain: consultoria-legal)

### Usuários de Teste
- `admin@empresa-abc.com` / `admin123` (admin)
- `user@empresa-abc.com` / `user123` (user)
- `admin@startup-xyz.com` / `admin123` (admin)
- `dev@startup-xyz.com` / `dev123` (developer)
- `advogado@consultoria-legal.com` / `adv123` (admin)

### Agentes por Tenant
- **LexAI** - Assistente jurídico
- **FinBot** - Assistente financeiro
- **SuporteAI** - Assistente de suporte

## 🚀 Comandos Úteis

```bash
# Verificar status das migrations
alembic current

# Criar nova migration (quando Alembic estiver instalado)
alembic revision --autogenerate -m "descrição"

# Reverter migration
alembic downgrade -1

# Ver histórico de migrations
alembic history

# Limpar banco e recriar
alembic downgrade base
alembic upgrade head
python scripts/seed_data.py
```

## 📝 Arquivos de Configuração Alembic

### `alembic.ini`
- Configuração principal do Alembic
- URL do banco configurada dinamicamente no `env.py`

### `migrations/env.py`
- Carrega variáveis do `.env`
- Configura URL do banco dinamicamente
- Importa todos os modelos SQLAlchemy
- Suporte a `POSTGRES_URL` ou configuração individual

### `migrations/script.py.mako`
- Template para geração de migrations
- Configuração padrão do Alembic

## 📝 Notas Importantes

1. **Isolamento**: Sempre use repositórios com tenant_id
2. **UUIDs**: Todos os IDs são UUIDs para segurança
3. **Cascade**: Deletar tenant remove todos os dados relacionados
4. **Índices**: Criados automaticamente para performance
5. **Timestamps**: Todos os registros têm created_at/updated_at
6. **POSTGRES_URL**: Prioridade sobre configuração individual

## 🔧 Troubleshooting

### Erro de Conexão
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar conexão
psql -h localhost -U postgres -d chat_agents
```

### Erro de Migration
```bash
# Verificar logs
alembic upgrade head --verbose

# Reset completo
alembic downgrade base
alembic upgrade head
```

### Erro de Seed
```bash
# Verificar se migrations foram executadas
alembic current

# Executar seed novamente
python scripts/seed_data.py
```

### Erro de Configuração Alembic
```bash
# Verificar se .env está configurado
cat .env | grep POSTGRES

# Verificar se variáveis estão sendo carregadas
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('POSTGRES_URL'))"
``` 