# 🗄️ Configuração Manual das Tabelas - Supabase

## 📋 Instruções para Python 3.13 Migration

### 1. Acesse o Supabase Dashboard
🔗 **URL**: https://supabase.com/dashboard/project/tegbkyeqfrqkuxeilgpc

### 2. Vá para o SQL Editor
- Clique em "SQL Editor" no menu lateral
- Clique em "New query"

### 3. Execute o SQL Básico
Copie e cole o seguinte SQL:

```sql
-- Extensões básicas
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de agentes (essencial)
CREATE TABLE IF NOT EXISTS agents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    model VARCHAR(100) DEFAULT 'gpt-3.5-turbo',
    temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 2048,
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Histórico de chat (essencial)
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    chat_mode VARCHAR(50) DEFAULT 'UsoCotidiano',
    tokens_used INTEGER DEFAULT 0,
    response_time_ms INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Políticas básicas para agents
CREATE POLICY "Users can view their own agents" ON agents
    FOR SELECT USING (auth.uid() = created_by);

CREATE POLICY "Users can create agents" ON agents
    FOR INSERT WITH CHECK (auth.uid() = created_by);

-- Políticas básicas para chat_history
CREATE POLICY "Users can view their own chat history" ON chat_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own chat history" ON chat_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### 4. Clique em "Run"
- Execute o SQL clicando no botão "Run"
- Verifique se não há erros

### 5. Verifique as Tabelas
- Vá para "Table Editor" no menu lateral
- Confirme que as tabelas `agents` e `chat_history` foram criadas

### 6. Teste a Aplicação
Após criar as tabelas, teste a aplicação:

```bash
curl http://localhost:8000/health
```

## ✅ Próximos Passos

1. **Criar as tabelas** seguindo as instruções acima
2. **Testar a aplicação** com Python 3.13
3. **Fazer commit** das mudanças
4. **Deploy** no EasyPanel (opcional)

## 🔧 Troubleshooting

Se houver erros:
- Verifique se o projeto Supabase está ativo
- Confirme se as credenciais no `.env` estão corretas
- Verifique os logs da aplicação: `docker logs ngabi-backend` 