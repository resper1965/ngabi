# 🏠 Variáveis de Ambiente para Supabase LOCAL

## 📋 **Configuração do Backend n.Gabi com Supabase Self-Hosted**

### **🔑 Variáveis OBRIGATÓRIAS para Supabase Local:**

```env
# Supabase Local Configuration
SUPABASE_URL=http://your-vps-ip:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0

# Redis Configuration (opcional)
REDIS_URL=redis://ngabi-redis:6379

# CORS Configuration
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br

# Application Configuration
APP_NAME=n.Gabi Backend
APP_VERSION=2.0.0
```

## 🎯 **Como Obter Credenciais do Supabase Local:**

### **1. Acessar Supabase Local**
```bash
# Se estiver rodando via Docker
docker exec -it supabase-db psql -U postgres -d postgres

# Ou acessar via navegador
http://your-vps-ip:54321
```

### **2. Obter URL e Chave**
```bash
# URL do Supabase Local
SUPABASE_URL=http://your-vps-ip:54321

# Chave anônima padrão (geralmente é esta)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```

### **3. Verificar Configuração**
```bash
# Testar conexão com Supabase Local
curl http://your-vps-ip:54321/rest/v1/
```

## 🔧 **Configuração no Easypanel:**

### **1. Variáveis de Ambiente**
| **Variável** | **Valor** | **Descrição** |
|--------------|-----------|---------------|
| `SUPABASE_URL` | `http://your-vps-ip:54321` | URL do Supabase local |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Chave anônima do Supabase local |
| `REDIS_URL` | `redis://ngabi-redis:6379` | URL do Redis |
| `CORS_ORIGINS` | `https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br` | Domínios permitidos |

### **2. Substituir IP do VPS**
- Substitua `your-vps-ip` pelo IP real do seu VPS
- Exemplo: `http://192.168.1.100:54321`

## 🗄️ **Configurar Tabelas no Supabase Local:**

### **1. Acessar SQL Editor**
```bash
# Via navegador
http://your-vps-ip:54321/project/default/sql

# Ou via psql
docker exec -it supabase-db psql -U postgres -d postgres
```

### **2. Executar Scripts**
```sql
-- Executar os scripts do arquivo SUPABASE-SETUP.md
-- Todas as tabelas e políticas de segurança
```

## 🚨 **Diferenças do Supabase Local:**

### **1. URL**
- **Cloud**: `https://project.supabase.co`
- **Local**: `http://your-vps-ip:54321`

### **2. Chave Anônima**
- **Cloud**: Única por projeto
- **Local**: Geralmente padrão (ver acima)

### **3. Configuração**
- **Cloud**: Gerenciado pelo Supabase
- **Local**: Você gerencia tudo

## ✅ **Checklist para Supabase Local:**

- [ ] Supabase local rodando no VPS
- [ ] IP do VPS identificado
- [ ] Porta 54321 acessível
- [ ] Chave anônima obtida
- [ ] Tabelas criadas no Supabase local
- [ ] Variáveis configuradas no Easypanel
- [ ] Deploy realizado

## 🧪 **Testar Conexão:**

```bash
# Testar Supabase Local
curl http://your-vps-ip:54321/rest/v1/

# Testar após deploy
curl https://api.ngabi.ness.tec.br/health
```

## 🎉 **Vantagens do Supabase Local:**

- ✅ **Controle total** dos dados
- ✅ **Sem limites** de uso
- ✅ **Privacidade** completa
- ✅ **Custo zero** (apenas VPS)
- ✅ **Personalização** total

**Agora configure com o IP do seu VPS!** 🚀 