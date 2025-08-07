// Configurações de ambiente para o frontend
export const environment = {
  // URLs baseadas no ambiente
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  supabaseUrl: import.meta.env.VITE_SUPABASE_URL || 'https://hyeifxvxifhrapfdvfry.supabase.co',
  supabaseAnonKey: import.meta.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd',
  
  // OpenAI Configuration
  openaiApiKey: import.meta.env.VITE_OPENAI_API_KEY || '',
  openaiModel: import.meta.env.VITE_OPENAI_MODEL || 'gpt-3.5-turbo',
  openaiTemperature: parseFloat(import.meta.env.VITE_OPENAI_TEMPERATURE || '0.7'),
  openaiMaxTokens: parseInt(import.meta.env.VITE_OPENAI_MAX_TOKENS || '2048'),
  
  // Configurações de produção
  production: {
    apiBaseUrl: import.meta.env.VITE_PRODUCTION_API_URL || 'https://ngabi.ness.tec.br/api',
    domain: import.meta.env.VITE_PRODUCTION_DOMAIN || 'ngabi.ness.tec.br',
    protocol: import.meta.env.VITE_PRODUCTION_PROTOCOL || 'https'
  },
  
  // Configurações de desenvolvimento
  development: {
    apiBaseUrl: import.meta.env.VITE_DEVELOPMENT_API_URL || 'http://localhost:8000',
    domain: import.meta.env.VITE_DEVELOPMENT_DOMAIN || 'localhost:3000',
    protocol: import.meta.env.VITE_DEVELOPMENT_PROTOCOL || 'http'
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