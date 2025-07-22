# 🚀 Executar Scripts SQL Manualmente no Supabase

## 📋 **Problema Identificado**

O script automático não conseguiu criar as tabelas porque a função `exec_sql` não existe no Supabase. Precisamos executar os scripts SQL manualmente no SQL Editor.

## 🔧 **Como Executar**

### 1. **Acessar SQL Editor**
- 🌐 Acesse: https://tegbkyeqfrqkuxeilgpc.supabase.co/sql
- 🔑 Faça login no Supabase Dashboard

### 2. **Executar Scripts em Ordem**

#### **Passo 1: Banco de Dados Principal**
1. Abra o arquivo `supabase/create-database.sql`
2. Copie todo o conteúdo
3. Cole no SQL Editor
4. Clique em **"Run"**

#### **Passo 2: Realtime**
1. Abra o arquivo `supabase/realtime-setup.sql`
2. Copie todo o conteúdo
3. Cole no SQL Editor
4. Clique em **"Run"**

#### **Passo 3: Storage**
1. Abra o arquivo `supabase/storage-setup.sql`
2. Copie todo o conteúdo
3. Cole no SQL Editor
4. Clique em **"Run"**

#### **Passo 4: Auth**
1. Abra o arquivo `supabase/auth-setup.sql`
2. Copie todo o conteúdo
3. Cole no SQL Editor
4. Clique em **"Run"**

## 📊 **Verificar se Funcionou**

Após executar todos os scripts, verifique se as tabelas foram criadas:

```sql
-- Listar todas as tabelas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

Você deve ver:
- tenants
- users
- agents
- chat_history
- events
- webhooks
- files
- chat_sessions
- audit_logs
- presence

## 🔍 **Testar Dados Iniciais**

```sql
-- Verificar tenant padrão
SELECT * FROM tenants;

-- Verificar agente padrão
SELECT * FROM agents;
```

## 🚨 **Se Houver Erros**

### Erro: "relation already exists"
- ✅ Normal, significa que a tabela já existe
- Continue com o próximo script

### Erro: "permission denied"
- ❌ Verifique se está logado no Supabase
- ❌ Verifique se tem permissões de admin

### Erro: "function does not exist"
- ❌ Execute os scripts na ordem correta
- ❌ Verifique se o script anterior foi executado completamente

## 📋 **Ordem de Execução**

1. ✅ `create-database.sql` - Cria tabelas e estrutura básica
2. ✅ `realtime-setup.sql` - Configura realtime (depende das tabelas)
3. ✅ `storage-setup.sql` - Configura storage (depende das tabelas)
4. ✅ `auth-setup.sql` - Configura auth (depende das tabelas)

## 🎯 **Resultado Esperado**

Após executar todos os scripts, você terá:

- ✅ **10 tabelas** criadas
- ✅ **Índices** de performance
- ✅ **RLS** habilitado
- ✅ **Funções** e triggers
- ✅ **Dados iniciais** inseridos
- ✅ **Realtime** configurado
- ✅ **Storage** configurado
- ✅ **Auth** configurado

## 🔗 **URLs Úteis**

- 🌐 **SQL Editor**: https://tegbkyeqfrqkuxeilgpc.supabase.co/sql
- 📊 **Table Editor**: https://tegbkyeqfrqkuxeilgpc.supabase.co/table-editor
- 📁 **Storage**: https://tegbkyeqfrqkuxeilgpc.supabase.co/storage/buckets
- 🔐 **Auth**: https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/settings

## 📞 **Suporte**

Se encontrar problemas:
1. Verifique a ordem de execução
2. Execute um script por vez
3. Verifique os logs de erro no SQL Editor
4. Consulte a documentação do Supabase 