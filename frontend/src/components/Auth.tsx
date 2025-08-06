import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabase } from '../lib/supabase'

export const AuthComponent = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            n.Gabi Chat
          </h2>
          <p className="mt-2 text-center text-sm text-gray-300">
            Faça login para acessar a plataforma
          </p>
        </div>
        <div className="mt-8 space-y-6">
          <Auth
            supabaseClient={supabase}
            appearance={{
              theme: ThemeSupa,
              variables: {
                default: {
                  colors: {
                    brand: '#00ade0',
                    brandAccent: '#0091cc',
                  },
                },
              },
            }}
            providers={['google', 'github']}
            redirectTo={window.location.origin}
          />
        </div>
      </div>
    </div>
  )
} 