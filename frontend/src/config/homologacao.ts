/**
 * Configuração para Ambiente de Homologação - Frontend
 */

export const HOMOLOGACAO_CONFIG = {
  // URLs
  API_BASE_URL: 'https://ngabi.ness.tec.br/backend',
  FRONTEND_URL: 'https://ngabi.ness.tec.br',
  
  // Supabase
  SUPABASE_URL: import.meta.env.VITE_SUPABASE_URL,
  SUPABASE_ANON_KEY: import.meta.env.VITE_SUPABASE_ANON_KEY,
  
  // OpenAI (para testes diretos)
  OPENAI_API_KEY: import.meta.env.VITE_OPENAI_API_KEY,
  
  // Ambiente
  ENVIRONMENT: 'homologacao',
  DEBUG: false,
  
  // Features
  FEATURES: {
    chat_enabled: true,
    agents_enabled: true,
    langchain_enabled: true,
    voice_style_enabled: true,
    rag_enabled: true,
    streaming_enabled: true,
    caching_enabled: true,
    rate_limiting_enabled: true,
    monitoring_enabled: true,
  },
  
  // Endpoints
  ENDPOINTS: {
    // Auth
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    
    // Chat
    CHAT: '/api/v1/chat/',
    CHAT_STREAM: '/api/v1/chat/stream',
    CHAT_HISTORY: '/api/v1/chat/history',
    
    // Agents
    AGENTS: '/api/v1/agents/',
    AGENTS_TEMPLATES: '/api/v1/agents/templates',
    AGENTS_SPECIALISTS: '/api/v1/agents/specialists',
    AGENTS_TEST: '/api/v1/agents/{id}/test',
    
    // Voice Style
    VOICE_STYLE_INIT: '/api/v1/agents/voice-style/initialize',
    VOICE_STYLE_SPECIALIST: '/api/v1/agents/voice-style/specialist',
    VOICE_STYLE_DOCUMENTS: '/api/v1/agents/voice-style/documents',
    VOICE_STYLE_TEST: '/api/v1/agents/voice-style/test',
    
    // Health
    HEALTH: '/health',
    HEALTH_REDIS: '/health/redis',
    HEALTH_LANGCHAIN: '/api/v1/agents/langchain/health',
    HEALTH_VECTORSTORE: '/api/v1/agents/vectorstore/health',
  },
  
  // Rate Limiting
  RATE_LIMITS: {
    CHAT: 200,
    AUTH: 100,
    API: 500,
  },
  
  // Timeouts
  TIMEOUTS: {
    REQUEST: 30000,
    CHAT: 60000,
    STREAM: 300000,
  },
  
  // UI/UX
  UI: {
    THEME: 'dark',
    FONT: 'Montserrat',
    PRIMARY_COLOR: '#00ade0',
    LOADING_TIMEOUT: 5000,
    ERROR_TIMEOUT: 3000,
    SUCCESS_TIMEOUT: 2000,
  },
}

export const getApiUrl = (endpoint: string): string => {
  return `${HOMOLOGACAO_CONFIG.API_BASE_URL}${endpoint}`
}

export const getFullUrl = (path: string): string => {
  return `${HOMOLOGACAO_CONFIG.FRONTEND_URL}${path}`
}

export const isHomologacao = (): boolean => {
  return HOMOLOGACAO_CONFIG.ENVIRONMENT === 'homologacao'
}

export const getConfig = () => {
  return HOMOLOGACAO_CONFIG
} 