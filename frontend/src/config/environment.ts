/**
 * Configuração de ambiente - Frontend n.Gabi
 */

export const environment = {
  development: {
    apiBaseUrl: import.meta.env.VITE_DEVELOPMENT_API_URL || 'http://localhost:8000',
    domain: import.meta.env.VITE_DEVELOPMENT_DOMAIN || 'localhost:3000',
    protocol: import.meta.env.VITE_DEVELOPMENT_PROTOCOL || 'http',
    supabaseUrl: import.meta.env.VITE_SUPABASE_URL || '',
    supabaseAnonKey: import.meta.env.VITE_SUPABASE_ANON_KEY || '',
    supabaseServiceRoleKey: import.meta.env.VITE_SUPABASE_SERVICE_ROLE_KEY || '',
    openaiApiKey: import.meta.env.VITE_OPENAI_API_KEY || '',
    openaiModel: import.meta.env.VITE_OPENAI_MODEL || 'gpt-3.5-turbo',
    openaiTemperature: parseFloat(import.meta.env.VITE_OPENAI_TEMPERATURE || '0.7'),
    openaiMaxTokens: parseInt(import.meta.env.VITE_OPENAI_MAX_TOKENS || '2048'),
  },
  production: {
    apiBaseUrl: import.meta.env.VITE_PRODUCTION_API_URL || 'https://ngabi.ness.tec.br/api',
    domain: import.meta.env.VITE_PRODUCTION_DOMAIN || 'ngabi.ness.tec.br',
    protocol: import.meta.env.VITE_PRODUCTION_PROTOCOL || 'https',
    supabaseUrl: import.meta.env.VITE_SUPABASE_URL || '',
    supabaseAnonKey: import.meta.env.VITE_SUPABASE_ANON_KEY || '',
    supabaseServiceRoleKey: import.meta.env.VITE_SUPABASE_SERVICE_ROLE_KEY || '',
    openaiApiKey: import.meta.env.VITE_OPENAI_API_KEY || '',
    openaiModel: import.meta.env.VITE_OPENAI_MODEL || 'gpt-3.5-turbo',
    openaiTemperature: parseFloat(import.meta.env.VITE_OPENAI_TEMPERATURE || '0.7'),
    openaiMaxTokens: parseInt(import.meta.env.VITE_OPENAI_MAX_TOKENS || '2048'),
  },
};

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