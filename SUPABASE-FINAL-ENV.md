# 🔐 Variáveis Finais do Supabase - Easypanel

## 📋 **VARIÁVEIS PARA O SERVIÇO SUPABASE**

### **Secrets (Obrigatórias)**
```env
POSTGRES_PASSWORD=your-super-secret-and-long-postgres-password
JWT_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
DASHBOARD_USERNAME=supabase
DASHBOARD_PASSWORD=this_password_is_insecure_and_should_be_updated
SECRET_KEY_BASE=UpNVntn3cDxHJpq99YMc1T1AQgQpc8kfYTuRgBiYa15BLrx8etQoXz3gZv1/u2oq
VAULT_ENC_KEY=your-encryption-key-32-chars-min
```

### **Database**
```env
POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
```

### **Supavisor**
```env
POOLER_PROXY_PORT_TRANSACTION=6543
POOLER_DEFAULT_POOL_SIZE=20
POOLER_MAX_CLIENT_CONN=100
POOLER_TENANT_ID=your-tenant-id
```

### **API Proxy**
```env
KONG_HTTP_PORT=8000
KONG_HTTPS_PORT=8443
```

### **API**
```env
PGRST_DB_SCHEMAS=public,storage,graphql_public
```

### **Auth**
```env
SITE_URL=http://localhost:3000
ADDITIONAL_REDIRECT_URLS=
JWT_EXPIRY=3600
DISABLE_SIGNUP=false
API_EXTERNAL_URL=http://localhost:8000
```

### **Studio**
```env
STUDIO_DEFAULT_ORGANIZATION=Default Organization
STUDIO_DEFAULT_PROJECT=Default Project
STUDIO_PORT=3000
SUPABASE_PUBLIC_URL=http://localhost:8000
IMGPROXY_ENABLE_WEBP_DETECTION=true
OPENAI_API_KEY=
```

### **Functions**
```env
FUNCTIONS_VERIFY_JWT=false
```

### **Logs**
```env
LOGFLARE_LOGGER_BACKEND_API_KEY=your-super-secret-and-long-logflare-key
LOGFLARE_API_KEY=your-super-secret-and-long-logflare-key
DOCKER_SOCKET_LOCATION=/var/run/docker.sock
```

## 📋 **VARIÁVEIS PARA O SERVIÇO ngabi-backend**

```env
SUPABASE_URL=http://supabase:8000
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
REDIS_URL=redis://ngabi-redis:6379
JWT_SECRET_KEY=your-super-secret-jwt-token-with-at-least-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br
```

## 📋 **VARIÁVEIS PARA O SERVIÇO ngabi-frontend**

```env
VITE_API_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
```

## 🎯 **IMPORTANTE**

- **SUPABASE_URL**: Use `http://supabase:8000` para conexão interna entre serviços
- **ANON_KEY**: Mantenha exatamente como fornecido
- **JWT_SECRET**: Use o mesmo valor para Supabase e ngabi-backend
- **Domínios**: Configure DNS A Records para `ngabi.ness.tec.br`, `api.ngabi.ness.tec.br`, `n8n.ngabi.ness.tec.br`

## ✅ **Checklist**

- [ ] Supabase com todas as variáveis configuradas
- [ ] ngabi-backend com SUPABASE_URL=http://supabase:8000
- [ ] ngabi-frontend com VITE_API_URL=https://api.ngabi.ness.tec.br
- [ ] DNS configurado
- [ ] Traefik labels configurados 