# 🔗 Configuração Manual de Redirect URLs - Supabase Auth

## 📋 Visão Geral

Este guia mostra como configurar manualmente as URLs de redirecionamento para autenticação no Supabase via dashboard web.

## 🌐 URLs Necessárias

### **URLs de Produção**
```
https://ngabi.ness.tec.br
https://www.ngabi.ness.tec.br
https://api.ngabi.ness.tec.br
https://ngabi.ness.tec.br/auth/callback
https://ngabi.ness.tec.br/auth/confirm
https://ngabi.ness.tec.br/auth/reset-password
```

### **URLs de Desenvolvimento**
```
http://localhost:3000
http://localhost:3000/auth/callback
http://localhost:3000/auth/confirm
http://localhost:3000/auth/reset-password
http://localhost:8000
http://localhost:8000/auth/callback
```

### **URLs com Wildcards**
```
https://*.ngabi.ness.tec.br
https://*.ness.tec.br
```

## 🔧 Configuração via Dashboard

### **1. Acessar o Dashboard**
1. Vá para: https://tegbkyeqfrqkuxeilgpc.supabase.co
2. Faça login na sua conta
3. Selecione o projeto `ngabi`

### **2. Configurar Site URL**
1. Vá para **Authentication** → **Settings**
2. Em **Site URL**, configure:
   ```
   https://ngabi.ness.tec.br
   ```

### **3. Configurar Redirect URLs**
1. Vá para **Authentication** → **URL Configuration**
2. Em **Redirect URLs**, adicione cada URL:

#### **URLs de Produção**
```
https://ngabi.ness.tec.br
https://www.ngabi.ness.tec.br
https://api.ngabi.ness.tec.br
https://ngabi.ness.tec.br/auth/callback
https://ngabi.ness.tec.br/auth/confirm
https://ngabi.ness.tec.br/auth/reset-password
```

#### **URLs de Desenvolvimento**
```
http://localhost:3000
http://localhost:3000/auth/callback
http://localhost:3000/auth/confirm
http://localhost:3000/auth/reset-password
http://localhost:8000
http://localhost:8000/auth/callback
```

#### **URLs com Wildcards**
```
https://*.ngabi.ness.tec.br
https://*.ness.tec.br
```

### **4. Configurar Providers**

#### **Email Provider**
1. Vá para **Authentication** → **Providers**
2. Clique em **Email**
3. Configure:
   - ✅ **Enable Email Signup**
   - ✅ **Enable Email Confirmations**
   - ✅ **Enable Password Reset**
   - ✅ **Double Confirm Changes**
4. Em **Redirect URLs**, adicione as URLs acima

#### **Google OAuth (Opcional)**
1. Vá para **Authentication** → **Providers**
2. Clique em **Google**
3. Configure:
   - ✅ **Enable Google Sign In**
   - **Client ID**: `your_google_client_id`
   - **Client Secret**: `your_google_client_secret`
4. Em **Redirect URLs**, adicione as URLs acima

#### **GitHub OAuth (Opcional)**
1. Vá para **Authentication** → **Providers**
2. Clique em **GitHub**
3. Configure:
   - ✅ **Enable GitHub Sign In**
   - **Client ID**: `your_github_client_id`
   - **Client Secret**: `your_github_client_secret`
4. Em **Redirect URLs**, adicione as URLs acima

## 🔧 Configuração via API

### **Configurar Site URL**
```bash
curl -X PUT "https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/v1/admin/settings" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "site_url": "https://ngabi.ness.tec.br"
  }'
```

### **Configurar Email Provider**
```bash
curl -X PUT "https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": {
      "enabled": true,
      "double_confirm_changes": true,
      "enable_signup": true,
      "enable_confirmations": true,
      "enable_password_reset": true,
      "redirect_to": [
        "https://ngabi.ness.tec.br",
        "https://www.ngabi.ness.tec.br",
        "https://api.ngabi.ness.tec.br",
        "https://ngabi.ness.tec.br/auth/callback",
        "https://ngabi.ness.tec.br/auth/confirm",
        "https://ngabi.ness.tec.br/auth/reset-password",
        "http://localhost:3000",
        "http://localhost:3000/auth/callback",
        "http://localhost:3000/auth/confirm",
        "http://localhost:3000/auth/reset-password",
        "http://localhost:8000",
        "http://localhost:8000/auth/callback",
        "https://*.ngabi.ness.tec.br",
        "https://*.ness.tec.br"
      ]
    }
  }'
```

### **Configurar Google OAuth**
```bash
curl -X PUT "https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "google": {
      "enabled": true,
      "client_id": "your_google_client_id",
      "client_secret": "your_google_client_secret",
      "redirect_to": [
        "https://ngabi.ness.tec.br",
        "https://www.ngabi.ness.tec.br",
        "https://api.ngabi.ness.tec.br",
        "https://ngabi.ness.tec.br/auth/callback",
        "https://ngabi.ness.tec.br/auth/confirm",
        "https://ngabi.ness.tec.br/auth/reset-password",
        "http://localhost:3000",
        "http://localhost:3000/auth/callback",
        "http://localhost:3000/auth/confirm",
        "http://localhost:3000/auth/reset-password",
        "http://localhost:8000",
        "http://localhost:8000/auth/callback",
        "https://*.ngabi.ness.tec.br",
        "https://*.ness.tec.br"
      ]
    }
  }'
```

### **Configurar GitHub OAuth**
```bash
curl -X PUT "https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/v1/admin/providers" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "github": {
      "enabled": true,
      "client_id": "your_github_client_id",
      "client_secret": "your_github_client_secret",
      "redirect_to": [
        "https://ngabi.ness.tec.br",
        "https://www.ngabi.ness.tec.br",
        "https://api.ngabi.ness.tec.br",
        "https://ngabi.ness.tec.br/auth/callback",
        "https://ngabi.ness.tec.br/auth/confirm",
        "https://ngabi.ness.tec.br/auth/reset-password",
        "http://localhost:3000",
        "http://localhost:3000/auth/callback",
        "http://localhost:3000/auth/confirm",
        "http://localhost:3000/auth/reset-password",
        "http://localhost:8000",
        "http://localhost:8000/auth/callback",
        "https://*.ngabi.ness.tec.br",
        "https://*.ness.tec.br"
      ]
    }
  }'
```

## 🧪 Testando as Configurações

### **1. Testar Login com Email**
```typescript
// Frontend
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'test@example.com',
  password: 'password'
})

if (error) {
  console.error('Erro de login:', error.message)
} else {
  console.log('Login bem-sucedido:', data.user)
}
```

### **2. Testar Magic Links**
```typescript
// Frontend
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'test@example.com',
  options: {
    emailRedirectTo: 'https://ngabi.ness.tec.br/auth/callback'
  }
})

if (error) {
  console.error('Erro magic link:', error.message)
} else {
  console.log('Magic link enviado')
}
```

### **3. Testar Password Reset**
```typescript
// Frontend
const { data, error } = await supabase.auth.resetPasswordForEmail('test@example.com', {
  redirectTo: 'https://ngabi.ness.tec.br/auth/reset-password'
})

if (error) {
  console.error('Erro password reset:', error.message)
} else {
  console.log('Email de reset enviado')
}
```

### **4. Testar OAuth (Google)**
```typescript
// Frontend
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://ngabi.ness.tec.br/auth/callback'
  }
})

if (error) {
  console.error('Erro OAuth:', error.message)
} else {
  console.log('Redirecionamento OAuth iniciado')
}
```

## 🚨 Troubleshooting

### **Erro: "Invalid redirect URL"**
- ✅ Verifique se a URL está na lista de redirects permitidos
- ✅ Certifique-se de que não há espaços extras
- ✅ Use HTTPS para produção
- ✅ Aguarde alguns minutos para propagação

### **Erro: "Redirect URL not allowed"**
- ✅ Adicione a URL à lista de redirects via dashboard
- ✅ Verifique se a URL está exatamente igual
- ✅ Teste com e sem trailing slash
- ✅ Verifique se não há caracteres especiais

### **Magic Links não funcionam**
- ✅ Verifique se `enable_confirmations` está habilitado
- ✅ Confirme se as URLs de callback estão configuradas
- ✅ Verifique se o email está sendo enviado
- ✅ Teste com diferentes URLs de redirecionamento

### **OAuth não funciona**
- ✅ Verifique se o provider está habilitado
- ✅ Confirme se Client ID e Secret estão corretos
- ✅ Verifique se as redirect URLs estão configuradas no provider (Google/GitHub)
- ✅ Teste com URLs de desenvolvimento primeiro

### **Password Reset não funciona**
- ✅ Verifique se `enable_password_reset` está habilitado
- ✅ Confirme se as URLs de redirecionamento estão configuradas
- ✅ Verifique se o email está sendo enviado
- ✅ Teste com diferentes URLs

## 📋 Checklist de Configuração

### **Configurações Básicas**
- [ ] Site URL configurada
- [ ] Redirect URLs adicionadas
- [ ] Email provider habilitado
- [ ] Magic links habilitados
- [ ] Password reset habilitado

### **Configurações OAuth (Opcional)**
- [ ] Google OAuth configurado
- [ ] GitHub OAuth configurado
- [ ] Redirect URLs configuradas para OAuth
- [ ] Client IDs e Secrets configurados

### **Testes**
- [ ] Login com email/password funciona
- [ ] Magic links funcionam
- [ ] Password reset funciona
- [ ] OAuth funciona (se configurado)
- [ ] Redirecionamentos funcionam corretamente

## 🔗 URLs de Acesso

### **Dashboard Supabase**
- 🌐 **Auth Settings**: https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/settings
- 🔧 **Providers**: https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/providers
- 📋 **URL Configuration**: https://tegbkyeqfrqkuxeilgpc.supabase.co/auth/url-configuration

### **Documentação**
- 📚 **Supabase Auth Docs**: https://supabase.com/docs/guides/auth
- 🔗 **Redirect URLs Guide**: https://supabase.com/docs/guides/auth/auth-redirect-urls

---

## 🎉 **Configuração Concluída!**

Com essas configurações, o Supabase Auth estará pronto para:
- ✅ **Login com email/password**
- ✅ **Magic links**
- ✅ **Password reset**
- ✅ **OAuth (Google, GitHub)**
- ✅ **Redirecionamentos seguros**

**🚀 Auth configurado e pronto para uso!** 