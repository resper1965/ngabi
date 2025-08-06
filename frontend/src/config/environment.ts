// Configurações de ambiente para o frontend
export const environment = {
  // URLs baseadas no ambiente
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  supabaseUrl: 'https://hyeifxvxifhrapfdvfry.supabase.co',
  supabaseAnonKey: 'sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd',
  
  // Configurações de produção
  production: {
    apiBaseUrl: 'https://ngabi.ness.tec.br/api',
    domain: 'ngabi.ness.tec.br',
    protocol: 'https'
  },
  
  // Configurações de desenvolvimento
  development: {
    apiBaseUrl: 'http://localhost:8000',
    domain: 'localhost:3000',
    protocol: 'http'
  }
}

// Função para obter a URL base da API
export function getApiBaseUrl(): string {
  const isProduction = window.location.hostname === 'ngabi.ness.tec.br'
  return isProduction ? environment.production.apiBaseUrl : environment.development.apiBaseUrl
}

// Função para obter a URL base do frontend
export function getFrontendUrl(): string {
  const isProduction = window.location.hostname === 'ngabi.ness.tec.br'
  const config = isProduction ? environment.production : environment.development
  return `${config.protocol}://${config.domain}`
}

// Função para verificar se está em produção
export function isProduction(): boolean {
  return window.location.hostname === 'ngabi.ness.tec.br'
} 