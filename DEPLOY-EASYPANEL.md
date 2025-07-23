# 🚀 Deploy n.Gabi no EasyPanel

## 📋 Pré-requisitos

1. EasyPanel configurado com Traefik
2. Rede `traefik-public` criada
3. Variáveis de ambiente configuradas

## 🔧 Configuração no EasyPanel

### 1. Criar Projeto
- Nome: `ngabi`
- Descrição: `Chat Multi-Agente n.Gabi`

### 2. Configurar Variáveis de Ambiente
```bash
SUPABASE_URL=sua_url_do_supabase
SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
```

### 3. Deploy dos Serviços

#### Frontend
- **Imagem**: `resper1965/ngabi-frontend:latest`
- **Porta**: `3000`
- **Domínio**: `ngabi.ness.tec.br`
- **SSL**: Automático (Let's Encrypt)

#### Backend
- **Imagem**: `resper1965/ngabi-backend:latest`
- **Porta**: `8000`
- **Domínio**: `api.ngabi.ness.tec.br`
- **SSL**: Automático (Let's Encrypt)

#### Redis
- **Imagem**: `redis:7-alpine`
- **Porta**: `6379`

### 4. Configurar Traefik Labels

#### Frontend Labels:
```yaml
- "traefik.enable=true"
- "traefik.http.routers.ngabi-frontend.rule=Host(`ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-frontend.entrypoints=websecure"
- "traefik.http.routers.ngabi-frontend.tls.certresolver=letsencrypt"
- "traefik.http.services.ngabi-frontend.loadbalancer.server.port=3000"
- "traefik.docker.network=traefik-public"
```

#### Backend Labels:
```yaml
- "traefik.enable=true"
- "traefik.http.routers.ngabi-backend.rule=Host(`api.ngabi.ness.tec.br`)"
- "traefik.http.routers.ngabi-backend.entrypoints=websecure"
- "traefik.http.routers.ngabi-backend.tls.certresolver=letsencrypt"
- "traefik.http.services.ngabi-backend.loadbalancer.server.port=8000"
- "traefik.docker.network=traefik-public"
```

## 🌐 URLs de Produção

- **Frontend**: https://ngabi.ness.tec.br
- **Backend API**: https://api.ngabi.ness.tec.br
- **Health Check**: https://api.ngabi.ness.tec.br/health

## 🔍 Verificação

1. Acesse https://ngabi.ness.tec.br
2. Verifique se a página carrega corretamente
3. Teste a API em https://api.ngabi.ness.tec.br/health
4. Verifique os logs no EasyPanel

## 🛠️ Troubleshooting

### Se a página não carregar:
1. Verifique se as imagens foram baixadas corretamente
2. Confirme se as variáveis de ambiente estão configuradas
3. Verifique os logs dos containers
4. Confirme se o Traefik está roteando corretamente

### Se a API não responder:
1. Verifique se o Redis está rodando
2. Confirme as credenciais do Supabase
3. Verifique os logs do backend

## 📞 Suporte

Para problemas técnicos, verifique:
- Logs dos containers no EasyPanel
- Status dos serviços
- Configuração do Traefik
- Variáveis de ambiente
