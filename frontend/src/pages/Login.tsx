import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';

/**
 * WIREFRAME TEXTUAL:
 * 
 * ┌─────────────────────────────────────┐
 * │                                     │
 * │           [LOGO]                    │
 * │        Chat Multi-Agent             │
 * │                                     │
 * │  ┌─────────────────────────────┐    │
 * │  │         Login               │    │
 * │  │                             │    │
 * │  │  📧 E-mail: [__________]    │    │
 * │  │  🔒 Senha:  [__________] 👁 │    │
 * │  │                             │    │
 * │  │  [     ENTRAR     ]         │    │
 * │  │                             │    │
 * │  └─────────────────────────────┘    │
 * │                                     │
 * └─────────────────────────────────────┘
 */

interface LoginProps {
  onLogin?: (email: string, password: string) => void;
  isLoading?: boolean;
}

export function Login({ onLogin, isLoading = false }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: chamar API - autenticação
    if (onLogin) {
      onLogin(email, password);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center space-y-4">
          {/* TODO: carregar logo do tenant via API */}
          <div className="mx-auto w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white text-2xl font-bold">C</span>
          </div>
          <CardTitle className="text-2xl font-bold text-gray-900">
            Chat Multi-Agent
          </CardTitle>
          <p className="text-gray-600">Faça login para continuar</p>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            {/* Campo de E-mail */}
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium text-gray-700">
                E-mail
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  placeholder="seu@email.com"
                  required
                />
              </div>
            </div>

            {/* Campo de Senha */}
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium text-gray-700">
                Senha
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 pr-12"
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
          </CardContent>

          <CardFooter>
            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </Button>
          </CardFooter>
        </form>

        {/* TODO: implementar recuperação de senha via API */}
        <div className="px-6 pb-6 text-center">
          <a href="#" className="text-sm text-blue-600 hover:text-blue-800">
            Esqueceu sua senha?
          </a>
        </div>
      </Card>
    </div>
  );
} 