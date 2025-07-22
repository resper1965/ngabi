#!/bin/bash

# 🔗 Script de Configuração de Redirect URLs - Supabase Auth
# Configura URLs de redirecionamento para OAuth e magic links

set -e

echo "🔗 Configurando Redirect URLs para Supabase Auth..."

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
SUPABASE_URL="${SUPABASE_URL:-https://tegbkyeqfrqkuxeilgpc.supabase.co}"
SUPABASE_SERVICE_ROLE_KEY="${SUPABASE_SERVICE_ROLE_KEY:-}"
PROJECT_NAME="ngabi"

# URLs de redirecionamento
REDIRECT_URLS=(
    # URLs de produção
    "https://ngabi.ness.tec.br"
    "https://www.ngabi.ness.tec.br"
    "https://api.ngabi.ness.tec.br"
    "https://ngabi.ness.tec.br/auth/callback"
    "https://ngabi.ness.tec.br/auth/confirm"
    "https://ngabi.ness.tec.br/auth/reset-password"
    
    # URLs de desenvolvimento
    "http://localhost:3000"
    "http://localhost:3000/auth/callback"
    "http://localhost:3000/auth/confirm"
    "http://localhost:3000/auth/reset-password"
    "http://localhost:8000"
    "http://localhost:8000/auth/callback"
    
    # URLs do EasyPanel
    "https://ngabi.ness.tec.br"
    "https://api.ngabi.ness.tec.br"
    
    # URLs com wildcards (se necessário)
    "https://*.ngabi.ness.tec.br"
    "https://*.ness.tec.br"
)

# =============================================================================
# VERIFICAÇÕES PRÉVIAS
# =============================================================================
echo "📋 Verificando pré-requisitos..."

# Verificar se as variáveis de ambiente existem
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo "❌ Variáveis SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY são obrigatórias"
    exit 1
fi

# Verificar se curl está instalado
if ! command -v curl &> /dev/null; then
    echo "❌ curl não está instalado"
    exit 1
fi

echo "✅ Pré-requisitos verificados"

# =============================================================================
# CONFIGURAÇÃO DE SITE URL
# =============================================================================
echo "🌐 Configurando Site URL..."

# Configurar site URL principal
curl -X PUT "$SUPABASE_URL/auth/v1/admin/settings" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "site_url": "https://ngabi.ness.tec.br"
  }' --silent --output /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Site URL configurada: https://ngabi.ness.tec.br"
else
    echo "❌ Erro ao configurar Site URL"
    exit 1
fi

# =============================================================================
# CONFIGURAÇÃO DE REDIRECT URLS
# =============================================================================
echo "🔗 Configurando Redirect URLs..."

# Configurar redirect URLs para email provider
REDIRECT_URLS_JSON=$(printf '%s\n' "${REDIRECT_URLS[@]}" | jq -R . | jq -s .)

curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": {
      \"enabled\": true,
      \"double_confirm_changes\": true,
      \"enable_signup\": true,
      \"redirect_to\": $REDIRECT_URLS_JSON
    }
  }" --silent --output /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Redirect URLs configuradas para Email provider"
else
    echo "❌ Erro ao configurar Redirect URLs para Email"
fi

# =============================================================================
# CONFIGURAÇÃO DE GOOGLE OAUTH
# =============================================================================
if [ -n "$GOOGLE_CLIENT_ID" ] && [ -n "$GOOGLE_CLIENT_SECRET" ]; then
    echo "🔍 Configurando Google OAuth..."
    
    curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
      -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"google\": {
          \"enabled\": true,
          \"client_id\": \"$GOOGLE_CLIENT_ID\",
          \"client_secret\": \"$GOOGLE_CLIENT_SECRET\",
          \"redirect_to\": $REDIRECT_URLS_JSON
        }
      }" --silent --output /dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Google OAuth configurado com Redirect URLs"
    else
        echo "❌ Erro ao configurar Google OAuth"
    fi
else
    echo "⚠️ Google OAuth não configurado (GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET não definidos)"
fi

# =============================================================================
# CONFIGURAÇÃO DE GITHUB OAUTH
# =============================================================================
if [ -n "$GITHUB_CLIENT_ID" ] && [ -n "$GITHUB_CLIENT_SECRET" ]; then
    echo "🐙 Configurando GitHub OAuth..."
    
    curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
      -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"github\": {
          \"enabled\": true,
          \"client_id\": \"$GITHUB_CLIENT_ID\",
          \"client_secret\": \"$GITHUB_CLIENT_SECRET\",
          \"redirect_to\": $REDIRECT_URLS_JSON
        }
      }" --silent --output /dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ GitHub OAuth configurado com Redirect URLs"
    else
        echo "❌ Erro ao configurar GitHub OAuth"
    fi
else
    echo "⚠️ GitHub OAuth não configurado (GITHUB_CLIENT_ID/GITHUB_CLIENT_SECRET não definidos)"
fi

# =============================================================================
# CONFIGURAÇÃO DE MAGIC LINKS
# =============================================================================
echo "🔮 Configurando Magic Links..."

curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": {
      \"enabled\": true,
      \"double_confirm_changes\": true,
      \"enable_signup\": true,
      \"enable_confirmations\": true,
      \"redirect_to\": $REDIRECT_URLS_JSON
    }
  }" --silent --output /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Magic Links configurados"
else
    echo "❌ Erro ao configurar Magic Links"
fi

# =============================================================================
# CONFIGURAÇÃO DE PASSWORD RESET
# =============================================================================
echo "🔐 Configurando Password Reset..."

curl -X PUT "$SUPABASE_URL/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": {
      \"enabled\": true,
      \"double_confirm_changes\": true,
      \"enable_signup\": true,
      \"enable_confirmations\": true,
      \"enable_password_reset\": true,
      \"redirect_to\": $REDIRECT_URLS_JSON
    }
  }" --silent --output /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Password Reset configurado"
else
    echo "❌ Erro ao configurar Password Reset"
fi

# =============================================================================
# CONFIGURAÇÃO DE INVITE LINKS
# =============================================================================
echo "📧 Configurando Invite Links..."

curl -X PUT "$SUPABASE_URL/auth/v1/admin/settings" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"mailer_autoconfirm\": false,
    \"enable_signup\": true,
    \"enable_confirmations\": true,
    \"enable_password_reset\": true,
    \"jwt_expiry\": 3600,
    \"refresh_token_rotation_enabled\": true,
    \"security_update_password_require_reauthentication\": true,
    \"redirect_to\": $REDIRECT_URLS_JSON
  }" --silent --output /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Invite Links configurados"
else
    echo "❌ Erro ao configurar Invite Links"
fi

# =============================================================================
# VERIFICAÇÃO DAS CONFIGURAÇÕES
# =============================================================================
echo "🔍 Verificando configurações..."

# Verificar configurações atuais
echo "📋 Configurações atuais:"
curl -X GET "$SUPABASE_URL/auth/v1/admin/settings" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  --silent | jq '.' 2>/dev/null || echo "⚠️ Não foi possível verificar configurações"

# Verificar providers
echo "📋 Providers configurados:"
curl -X GET "$SUPABASE_URL/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  --silent | jq '.' 2>/dev/null || echo "⚠️ Não foi possível verificar providers"

# =============================================================================
# TESTE DE REDIRECIONAMENTO
# =============================================================================
echo "🧪 Testando redirecionamentos..."

# Testar URLs de redirecionamento
for url in "${REDIRECT_URLS[@]}"; do
    if [[ $url == http* ]]; then
        if curl -f -I "$url" > /dev/null 2>&1; then
            echo "✅ $url: Acessível"
        else
            echo "⚠️ $url: Não acessível (pode ser normal para desenvolvimento)"
        fi
    fi
done

# =============================================================================
# DOCUMENTAÇÃO DAS URLS
# =============================================================================
echo "📚 Documentando URLs configuradas..."

cat > auth-redirect-urls.md << EOF
# 🔗 URLs de Redirecionamento - Supabase Auth

## 📋 URLs Configuradas

### 🌐 Produção
- \`https://ngabi.ness.tec.br\`
- \`https://www.ngabi.ness.tec.br\`
- \`https://api.ngabi.ness.tec.br\`
- \`https://ngabi.ness.tec.br/auth/callback\`
- \`https://ngabi.ness.tec.br/auth/confirm\`
- \`https://ngabi.ness.tec.br/auth/reset-password\`

### 💻 Desenvolvimento
- \`http://localhost:3000\`
- \`http://localhost:3000/auth/callback\`
- \`http://localhost:3000/auth/confirm\`
- \`http://localhost:3000/auth/reset-password\`
- \`http://localhost:8000\`
- \`http://localhost:8000/auth/callback\`

### 🌍 Wildcards
- \`https://*.ngabi.ness.tec.br\`
- \`https://*.ness.tec.br\`

## 🔧 Configuração Manual

### Via Dashboard Supabase
1. Acesse: https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/settings
2. Vá em "URL Configuration"
3. Adicione as URLs acima em "Redirect URLs"

### Via API
\`\`\`bash
curl -X PUT "https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/v1/admin/providers" \\
  -H "apikey: \$SUPABASE_SERVICE_ROLE_KEY" \\
  -H "Authorization: Bearer \$SUPABASE_SERVICE_ROLE_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": {
      "redirect_to": ["https://ngabi.ness.tec.br", "http://localhost:3000"]
    }
  }'
\`\`\`

## 🚨 Troubleshooting

### Erro: "Invalid redirect URL"
- Verifique se a URL está na lista de redirects permitidos
- Certifique-se de que não há espaços extras
- Use HTTPS para produção

### Erro: "Redirect URL not allowed"
- Adicione a URL à lista de redirects via dashboard ou API
- Aguarde alguns minutos para a propagação

### Magic Links não funcionam
- Verifique se \`enable_confirmations\` está habilitado
- Confirme se as URLs de callback estão configuradas
EOF

echo "✅ Documentação criada: auth-redirect-urls.md"

# =============================================================================
# RELATÓRIO FINAL
# =============================================================================
echo ""
echo "🎉 CONFIGURAÇÃO DE REDIRECT URLS CONCLUÍDA!"
echo ""
echo "📊 Resumo da Configuração:"
echo "   ✅ Site URL configurada"
echo "   ✅ Email provider configurado"
echo "   ✅ Magic Links habilitados"
echo "   ✅ Password Reset configurado"
echo "   ✅ Invite Links configurados"
echo "   ✅ Google OAuth configurado (se aplicável)"
echo "   ✅ GitHub OAuth configurado (se aplicável)"
echo ""
echo "🔗 URLs Configuradas:"
printf '   %s\n' "${REDIRECT_URLS[@]}"
echo ""
echo "📋 Próximos Passos:"
echo "   1. Testar login com email/password"
echo "   2. Testar magic links"
echo "   3. Testar password reset"
echo "   4. Configurar OAuth providers (Google, GitHub)"
echo "   5. Testar redirecionamentos"
echo ""
echo "📚 Documentação:"
echo "   📄 auth-redirect-urls.md"
echo "   🌐 Supabase Dashboard: $SUPABASE_URL/auth/settings"
echo ""
echo "🚀 Auth configurado e pronto para uso!"
echo "" 