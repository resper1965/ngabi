# 🗄️ Configuração das Tabelas no Supabase

## 📋 **Tabelas Necessárias para n.Gabi**

### **1. Tabela: tenants**
```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  subdomain TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

### **2. Tabela: users**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'user',
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_tenant ON users(tenant_id);
```

### **3. Tabela: agents**
```sql
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  config JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (tenant_id, name)
);

CREATE INDEX idx_agents_tenant ON agents(tenant_id);
```

### **4. Tabela: tenant_settings**
```sql
CREATE TABLE tenant_settings (
  tenant_id UUID PRIMARY KEY REFERENCES tenants(id) ON DELETE CASCADE,
  logo_path TEXT,
  orchestrator_name TEXT,
  theme_primary CHAR(7),
  theme_secondary CHAR(7),
  contact_email TEXT,
  contact_phone TEXT,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

### **5. Tabela: chat_history**
```sql
CREATE TABLE chat_history (
  id BIGSERIAL PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE SET NULL,
  message TEXT NOT NULL,
  response TEXT NOT NULL,
  chat_mode TEXT NOT NULL,
  use_author_voice BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_chat_tenant_created ON chat_history(tenant_id, created_at DESC);
```

### **6. Tabela: messages**
```sql
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  chat_id BIGINT NOT NULL REFERENCES chat_history(id) ON DELETE CASCADE,
  speaker TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_messages_chat ON messages(chat_id);
```

## 🔐 **Configuração de Row Level Security (RLS)**

### **1. Habilitar RLS em todas as tabelas**
```sql
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
```

### **2. Políticas para tenants**
```sql
-- Usuários podem ver apenas seus próprios tenants
CREATE POLICY "Users can view own tenant" ON tenants
  FOR SELECT USING (auth.uid() IN (
    SELECT user_id FROM users WHERE tenant_id = tenants.id
  ));

-- Apenas admins podem criar/editar tenants
CREATE POLICY "Only admins can manage tenants" ON tenants
  FOR ALL USING (auth.jwt() ->> 'role' = 'admin');
```

### **3. Políticas para users**
```sql
-- Usuários podem ver usuários do mesmo tenant
CREATE POLICY "Users can view same tenant users" ON users
  FOR SELECT USING (tenant_id IN (
    SELECT tenant_id FROM users WHERE user_id = auth.uid()
  ));

-- Usuários podem editar apenas seus próprios dados
CREATE POLICY "Users can edit own data" ON users
  FOR UPDATE USING (user_id = auth.uid());
```

### **4. Políticas para agents**
```sql
-- Usuários podem ver agentes do mesmo tenant
CREATE POLICY "Users can view same tenant agents" ON agents
  FOR SELECT USING (tenant_id IN (
    SELECT tenant_id FROM users WHERE user_id = auth.uid()
  ));

-- Apenas admins podem gerenciar agentes
CREATE POLICY "Only admins can manage agents" ON agents
  FOR ALL USING (auth.jwt() ->> 'role' = 'admin');
```

### **5. Políticas para chat_history**
```sql
-- Usuários podem ver apenas seu próprio histórico
CREATE POLICY "Users can view own chat history" ON chat_history
  FOR SELECT USING (user_id = auth.uid());

-- Usuários podem criar apenas em seu próprio tenant
CREATE POLICY "Users can create in own tenant" ON chat_history
  FOR INSERT WITH CHECK (tenant_id IN (
    SELECT tenant_id FROM users WHERE user_id = auth.uid()
  ));
```

## 🎯 **Como Configurar no Supabase Dashboard**

### **1. Acessar SQL Editor**
1. Vá para o Supabase Dashboard
2. Clique em "SQL Editor"
3. Clique em "New Query"

### **2. Executar Scripts**
1. **Criar tabelas**: Execute o script SQL das tabelas
2. **Habilitar RLS**: Execute os comandos ALTER TABLE
3. **Criar políticas**: Execute as políticas de segurança

### **3. Verificar Configuração**
1. Vá para "Table Editor"
2. Verifique se todas as tabelas foram criadas
3. Verifique se RLS está habilitado
4. Teste as políticas

## ✅ **Checklist de Configuração**

- [ ] Todas as tabelas criadas
- [ ] RLS habilitado em todas as tabelas
- [ ] Políticas de segurança configuradas
- [ ] Índices criados
- [ ] Teste de inserção/consulta funcionando
- [ ] Autenticação testada

## 🚀 **Próximos Passos**

1. **Configurar tabelas** no Supabase Dashboard
2. **Testar conexão** do backend
3. **Deploy da aplicação** no Easypanel
4. **Testar funcionalidades** completas

**Agora o n.Gabi está totalmente adaptado para Supabase!** 🎉 