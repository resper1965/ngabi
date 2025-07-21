# 🚀 Configuração do Supabase da Nuvem

## 📋 Pré-requisitos

1. **Conta no Supabase**: [https://supabase.com](https://supabase.com)
2. **Projeto criado** no Supabase
3. **Credenciais do projeto** (URL e chave anônima)

## 🔧 Configuração

### 1. Obter Credenciais do Supabase

1. Acesse o [Dashboard do Supabase](https://supabase.com/dashboard)
2. Selecione seu projeto
3. Vá em **Settings** → **API**
4. Copie:
   - **Project URL** (ex: `https://your-project.supabase.co`)
   - **anon public** key

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto:

```bash
# SUPABASE CONFIGURATION (CLOUD)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# REDIS CONFIGURATION
REDIS_URL=redis://localhost:6379

# CORS CONFIGURATION
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# FRONTEND CONFIGURATION
VITE_API_BASE_URL=http://localhost:8000

# APPLICATION CONFIGURATION
APP_NAME=n.Gabi
APP_VERSION=2.0.0
```

### 3. Configurar Banco de Dados

Execute os seguintes comandos SQL no **SQL Editor** do Supabase:

```sql
-- Tabela de tenants
CREATE TABLE tenants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de agentes
CREATE TABLE agents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_prompt TEXT,
    model VARCHAR(100) DEFAULT 'gpt-3.5-turbo',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de histórico de chat
CREATE TABLE chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    user_id UUID,
    session_id VARCHAR(255),
    message TEXT NOT NULL,
    response TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_agents_tenant_id ON agents(tenant_id);
CREATE INDEX idx_chat_history_tenant_id ON chat_history(tenant_id);
CREATE INDEX idx_chat_history_session_id ON chat_history(session_id);
CREATE INDEX idx_chat_history_created_at ON chat_history(created_at);

-- RLS (Row Level Security)
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Políticas básicas (ajuste conforme necessário)
CREATE POLICY "Tenants are viewable by everyone" ON tenants FOR SELECT USING (true);
CREATE POLICY "Agents are viewable by tenant" ON agents FOR SELECT USING (true);
CREATE POLICY "Chat history is viewable by tenant" ON chat_history FOR SELECT USING (true);
```

### 4. Configurar Autenticação

1. Vá em **Authentication** → **Settings**
2. Configure as **URLs permitidas**:
   - `http://localhost:3000`
   - `http://localhost:8000`
   - Sua URL de produção

### 5. Testar a Configuração

```bash
# Iniciar os serviços
docker-compose up -d

# Verificar logs do backend
docker-compose logs backend

# Testar health check
curl http://localhost:8000/health
```

## 🔍 Verificação

### Health Check Esperado

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "2.0.0",
  "services": {
    "database": "Supabase",
    "auth": "Supabase Auth",
    "cache": "Redis"
  }
}
```

### Logs Esperados

```
🚀 Iniciando n.Gabi Backend com Supabase...
✅ Supabase conectado com sucesso
```

## 🚨 Troubleshooting

### Erro: "Supabase não configurado"

1. Verifique se `SUPABASE_URL` e `SUPABASE_ANON_KEY` estão definidos
2. Confirme se as credenciais estão corretas
3. Teste a conexão no SQL Editor do Supabase

### Erro: "Connection refused"

1. Verifique se o projeto está ativo no Supabase
2. Confirme se as políticas RLS estão configuradas
3. Verifique se as tabelas foram criadas

### Erro de CORS

1. Configure as URLs permitidas no Supabase
2. Verifique se `CORS_ORIGINS` está correto
3. Reinicie o backend após mudanças

## 📚 Próximos Passos

1. **Configurar usuários** no Supabase Auth
2. **Implementar autenticação** no frontend
3. **Configurar webhooks** para eventos em tempo real
4. **Implementar backup** automático do banco
5. **Configurar monitoramento** e logs

## 🔗 Links Úteis

- [Documentação do Supabase](https://supabase.com/docs)
- [Guia de RLS](https://supabase.com/docs/guides/auth/row-level-security)
- [API Reference](https://supabase.com/docs/reference/javascript)
- [Dashboard](https://supabase.com/dashboard) 