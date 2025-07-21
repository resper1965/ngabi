# 🔐 Variáveis de Ambiente Supabase - n.Gabi

## ############
## Secrets - CONFIGURADOS PARA PRODUÇÃO
## ############

POSTGRES_PASSWORD=NgabiSupabase2024!SecurePassword123
JWT_SECRET=NgabiJWT2024!SuperSecretKeyWithAtLeast32CharactersLong
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
DASHBOARD_USERNAME=ngabi-admin
DASHBOARD_PASSWORD=NgabiDashboard2024!Secure
SECRET_KEY_BASE=NgabiSecretKeyBase2024!UpNVntn3cDxHJpq99YMc1T1AQgQpc8kfYTuRgBiYa15BLrx8etQoXz3gZv1/u2oq
VAULT_ENC_KEY=NgabiVaultEncKey2024!32CharsMin

## ############
## Database - Configuração PostgreSQL
## ############

POSTGRES_HOST=db
POSTGRES_DB=ngabi_chat_agents
POSTGRES_PORT=5432
# default user is postgres

## ############
## Supavisor -- Database pooler
## ############

POOLER_PROXY_PORT_TRANSACTION=6543
POOLER_DEFAULT_POOL_SIZE=20
POOLER_MAX_CLIENT_CONN=100
POOLER_TENANT_ID=ngabi-tenant-2024

## ############
## API Proxy - Configuration for the Kong Reverse proxy.
## ############

KONG_HTTP_PORT=8000
KONG_HTTPS_PORT=8443

## ############
## API - Configuration for PostgREST.
## ############

PGRST_DB_SCHEMAS=public,storage,graphql_public

## ############
## Auth - Configuration for the GoTrue authentication server.
## ############

## General
SITE_URL=https://ngabi.ness.tec.br
ADDITIONAL_REDIRECT_URLS=https://api.ngabi.ness.tec.br,https://n8n.ngabi.ness.tec.br
JWT_EXPIRY=3600
DISABLE_SIGNUP=false
API_EXTERNAL_URL=https://api.ngabi.ness.tec.br

## Mailer Config
MAILER_URLPATHS_CONFIRMATION="/auth/v1/verify"
MAILER_URLPATHS_INVITE="/auth/v1/verify"
MAILER_URLPATHS_RECOVERY="/auth/v1/verify"
MAILER_URLPATHS_EMAIL_CHANGE="/auth/v1/verify"

## Email auth
ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=false
SMTP_ADMIN_EMAIL=admin@ngabi.ness.tec.br
SMTP_HOST=supabase-mail
SMTP_PORT=2500
SMTP_USER=ngabi_mail_user
SMTP_PASS=NgabiMail2024!Secure
SMTP_SENDER_NAME=n.Gabi Support
ENABLE_ANONYMOUS_USERS=false

## Phone auth
ENABLE_PHONE_SIGNUP=true
ENABLE_PHONE_AUTOCONFIRM=true

## ############
## Studio - Configuration for the Dashboard
## ############

STUDIO_DEFAULT_ORGANIZATION=n.Gabi Organization
STUDIO_DEFAULT_PROJECT=n.Gabi Chat Agents

STUDIO_PORT=3000
# replace if you intend to use Studio outside of localhost
SUPABASE_PUBLIC_URL=https://api.ngabi.ness.tec.br

# Enable webp support
IMGPROXY_ENABLE_WEBP_DETECTION=true

# Add your OpenAI API key to enable SQL Editor Assistant
OPENAI_API_KEY=sk-your-openai-api-key-here

## ############
## Functions - Configuration for Functions
## ############
# NOTE: VERIFY_JWT applies to all functions. Per-function VERIFY_JWT is not supported yet.
FUNCTIONS_VERIFY_JWT=false

## ############
## Logs - Configuration for Logflare
## Please refer to https://supabase.com/docs/reference/self-hosting-analytics/introduction
## ############

LOGFLARE_LOGGER_BACKEND_API_KEY=NgabiLogflare2024!SuperSecretAndLongKey
LOGFLARE_API_KEY=NgabiLogflare2024!SuperSecretAndLongKey

# Docker socket location - this value will differ depending on your OS
DOCKER_SOCKET_LOCATION=/var/run/docker.sock

## ############
## n.Gabi Specific Variables
## ############

# Backend API Configuration
NGABI_API_URL=https://api.ngabi.ness.tec.br
NGABI_FRONTEND_URL=https://ngabi.ness.tec.br
NGABI_N8N_URL=https://n8n.ngabi.ness.tec.br

# Redis Configuration
REDIS_URL=redis://ngabi-redis:6379

# JWT Configuration for n.Gabi Backend
JWT_SECRET_KEY=NgabiJWT2024!SuperSecretKey123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=https://ngabi.ness.tec.br,https://www.ngabi.ness.tec.br,https://api.ngabi.ness.tec.br

# Frontend Configuration
VITE_API_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_URL=https://api.ngabi.ness.tec.br
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE 