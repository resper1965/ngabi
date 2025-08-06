import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabase } from '../lib/supabase'
import { Bot, Sparkles } from 'lucide-react'

export const AuthComponent = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-card to-background py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center shadow-lg">
              <Bot className="w-8 h-8 text-primary-foreground" />
            </div>
          </div>
          <h2 className="text-4xl font-bold text-foreground mb-2">
            n.Gabi
          </h2>
          <p className="text-lg text-muted-foreground mb-1">
            Chat Multi-Agent
          </p>
          <div className="flex items-center justify-center space-x-2 text-sm text-muted-foreground">
            <Sparkles className="w-4 h-4" />
            <span>Powered by AI</span>
          </div>
        </div>

        {/* Auth Form */}
        <div className="bg-card rounded-2xl p-8 shadow-2xl border border-border">
          <div className="text-center mb-6">
            <h3 className="text-xl font-semibold text-card-foreground mb-2">
              Bem-vindo de volta
            </h3>
            <p className="text-muted-foreground">
              Faça login para acessar a plataforma
            </p>
          </div>
          
          <Auth
            supabaseClient={supabase}
            appearance={{
              theme: ThemeSupa,
              variables: {
                default: {
                  colors: {
                    brand: '#00ade8',
                    brandAccent: '#0091cc',
                    brandButtonText: '#ffffff',
                    defaultButtonBackground: '#374151',
                    defaultButtonBackgroundHover: '#4b5563',
                    defaultButtonBorder: '#4b5563',
                    defaultButtonText: '#ffffff',
                    dividerBackground: '#374151',
                    inputBackground: '#374151',
                    inputBorder: '#4b5563',
                    inputBorderHover: '#6b7280',
                    inputBorderFocus: '#00ade8',
                    inputLabelText: '#d1d5db',
                    inputPlaceholder: '#9ca3af',
                    messageText: '#d1d5db',
                    messageTextDanger: '#f87171',
                    anchorTextColor: '#00ade8',
                    anchorTextHoverColor: '#0091cc',
                  },
                },
              },
            }}
            providers={['google', 'github']}
            redirectTo={window.location.origin}
            localization={{
              variables: {
                sign_in: {
                  email_label: 'Email',
                  password_label: 'Senha',
                  button_label: 'Entrar',
                  loading_button_label: 'Entrando...',
                  social_provider_text: 'Entrar com {{provider}}',
                  link_text: 'Já tem uma conta? Entre aqui',
                },
                sign_up: {
                  email_label: 'Email',
                  password_label: 'Senha',
                  button_label: 'Criar conta',
                  loading_button_label: 'Criando conta...',
                  social_provider_text: 'Criar conta com {{provider}}',
                  link_text: 'Não tem uma conta? Crie aqui',
                },
                forgotten_password: {
                  email_label: 'Email',
                  button_label: 'Enviar instruções de recuperação',
                  loading_button_label: 'Enviando...',
                  link_text: 'Esqueceu sua senha?',
                },
              },
            }}
          />
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-sm text-gray-500">
            © 2024 n.Gabi. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </div>
  )
} 