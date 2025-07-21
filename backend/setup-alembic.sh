#!/bin/bash

# Script para configurar Alembic no backend
# Uso: ./setup-alembic.sh [database_url]

set -e

echo "🐍 Configurando Alembic..."

# Verificar argumentos
DATABASE_URL=${1:-"postgresql://postgres:postgres@localhost:5432/chat_app"}

# Verificar se estamos no diretório backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ Execute este script no diretório backend"
    exit 1
fi

# Verificar se Alembic está instalado
if ! command -v alembic &> /dev/null; then
    echo "📦 Instalando Alembic..."
    pip install alembic psycopg2-binary
fi

# Verificar se já existe configuração do Alembic
if [ -f "alembic.ini" ]; then
    echo "⚠️  Configuração do Alembic já existe. Fazendo backup..."
    cp alembic.ini alembic.ini.backup
fi

# Inicializar Alembic se não existir
if [ ! -d "alembic" ]; then
    echo "🚀 Inicializando Alembic..."
    alembic init alembic
fi

# Configurar alembic.ini
echo "⚙️  Configurando alembic.ini..."
sed -i "s|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = $DATABASE_URL|g" alembic.ini

# Configurar env.py
echo "🔧 Configurando env.py..."
cat > alembic/env.py << 'EOF'
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.models import Base
from app.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    return settings.DATABASE_URL

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF

# Criar primeira migration se não existir
if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
    echo "📝 Criando primeira migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Criar script de teste de migrations
echo "🧪 Criando script de teste..."
cat > test-migrations.sh << 'EOF'
#!/bin/bash

echo "🧪 Testando migrations..."

# Verificar status atual
echo "📊 Status atual:"
alembic current

# Verificar heads
echo "📋 Heads disponíveis:"
alembic heads

# Verificar se há migrations pendentes
echo "⏳ Migrations pendentes:"
alembic show $alembic current

# Testar upgrade
echo "⬆️  Testando upgrade..."
alembic upgrade head

# Verificar se upgrade foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "✅ Upgrade bem-sucedido!"
else
    echo "❌ Falha no upgrade"
    exit 1
fi

# Verificar status final
echo "📊 Status final:"
alembic current

echo "✅ Teste de migrations concluído!"
EOF

chmod +x test-migrations.sh

# Criar script de rollback
echo "🔄 Criando script de rollback..."
cat > rollback-migration.sh << 'EOF'
#!/bin/bash

# Script para fazer rollback de migrations
# Uso: ./rollback-migration.sh [revision_id]

set -e

REVISION=${1:-"head-1"}

echo "🔄 Fazendo rollback para revision: $REVISION"

# Verificar status atual
echo "📊 Status atual:"
alembic current

# Fazer rollback
echo "⬇️  Fazendo rollback..."
alembic downgrade $REVISION

# Verificar se rollback foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "✅ Rollback bem-sucedido!"
else
    echo "❌ Falha no rollback"
    exit 1
fi

# Verificar status final
echo "📊 Status final:"
alembic current

echo "✅ Rollback concluído!"
EOF

chmod +x rollback-migration.sh

# Criar documentação
echo "📚 Criando documentação..."
cat > ALEMBIC_README.md << 'EOF'
# Configuração Alembic - Chat App

## Visão Geral

Este projeto usa Alembic para gerenciar migrations do banco de dados PostgreSQL.

## Comandos Básicos

### Verificar Status
```bash
# Status atual
alembic current

# Histórico de migrations
alembic history

# Heads disponíveis
alembic heads
```

### Executar Migrations
```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Aplicar até uma revision específica
alembic upgrade <revision_id>

# Aplicar apenas a próxima migration
alembic upgrade +1
```

### Criar Migrations
```bash
# Criar migration automática baseada nas mudanças dos modelos
alembic revision --autogenerate -m "Descrição da migration"

# Criar migration vazia
alembic revision -m "Descrição da migration"
```

### Rollback
```bash
# Voltar uma migration
alembic downgrade -1

# Voltar para uma revision específica
alembic downgrade <revision_id>

# Voltar para o início
alembic downgrade base
```

## Scripts Úteis

### Testar Migrations
```bash
./test-migrations.sh
```

### Fazer Rollback
```bash
./rollback-migration.sh [revision_id]
```

## Configuração

### Variáveis de Ambiente
- `DATABASE_URL`: URL de conexão com o banco de dados

### Arquivos de Configuração
- `alembic.ini`: Configuração principal do Alembic
- `alembic/env.py`: Configuração do ambiente Python
- `alembic/versions/`: Diretório com as migrations

## Troubleshooting

### Migration Falhou
1. Verificar logs de erro
2. Verificar se o banco está acessível
3. Verificar se as dependências estão instaladas
4. Fazer rollback se necessário

### Conflito de Migrations
1. Verificar se há múltiplos heads
2. Resolver conflitos manualmente
3. Criar migration de merge se necessário

### Banco Inconsistente
1. Verificar status atual: `alembic current`
2. Verificar heads: `alembic heads`
3. Sincronizar manualmente se necessário
EOF

echo "✅ Configuração do Alembic concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure a DATABASE_URL se necessário"
echo "2. Execute: alembic upgrade head"
echo "3. Teste com: ./test-migrations.sh"
echo ""
echo "📚 Documentação: ALEMBIC_README.md" 