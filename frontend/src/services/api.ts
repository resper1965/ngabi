import axios from 'axios'
import { getApiBaseUrl } from '../config/environment'

// Tipos para as respostas da API
interface ChatMessage {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: string
  agent_id?: string
}

interface ChatRequest {
  message: string
  agent_id?: string
  system_prompt?: string
  temperature?: number
  max_tokens?: number
}

interface ChatResponse {
  response: string
  message_id: string
  agent_id?: string
  usage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

interface Agent {
  id: string
  name: string
  description?: string
  system_prompt: string
  model: string
  temperature: number
  max_tokens: number
  is_active: boolean
  created_at: string
  updated_at: string
}

interface AgentCreate {
  name: string
  description?: string
  system_prompt: string
  model?: string
  temperature?: number
  max_tokens?: number
  is_active?: boolean
}

interface AgentUpdate {
  name?: string
  description?: string
  system_prompt?: string
  model?: string
  temperature?: number
  max_tokens?: number
  is_active?: boolean
}

interface AgentTestRequest {
  message: string
}

interface AgentTestResponse {
  response: string
  agent_id: string
  usage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

// Classe principal da API
class ApiService {
  private api: any

  constructor() {
    this.api = axios.create({
      baseURL: getApiBaseUrl(),
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Interceptor para adicionar token de autenticação
    this.api.interceptors.request.use(
      (config: any) => {
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error: any) => {
        return Promise.reject(error)
      }
    )

    // Interceptor para tratamento de erros
    this.api.interceptors.response.use(
      (response: any) => response,
      (error: any) => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  // =============================================================================
  // CHAT ENDPOINTS
  // =============================================================================

  async sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.api.post('/api/v1/chat/', request)
    return response.data
  }

  async sendChatMessageStream(request: ChatRequest): Promise<ReadableStream<ChatResponse>> {
    const response = await this.api.post('/api/v1/chat/stream', request, {
      responseType: 'stream',
    })
    return response.data
  }

  async getChatHistory(limit: number = 50, offset: number = 0): Promise<ChatMessage[]> {
    const response = await this.api.get('/api/v1/chat/history', {
      params: { limit, offset }
    })
    return response.data
  }

  // =============================================================================
  // AGENTS ENDPOINTS
  // =============================================================================

  async getAgents(limit: number = 50, offset: number = 0): Promise<{ agents: Agent[], total: number }> {
    const response = await this.api.get('/api/v1/agents/', {
      params: { limit, offset }
    })
    return response.data
  }

  async getAgentById(agentId: string): Promise<Agent> {
    const response = await this.api.get(`/api/v1/agents/${agentId}`)
    return response.data
  }

  async createAgent(agentData: AgentCreate): Promise<Agent> {
    const response = await this.api.post('/api/v1/agents/', agentData)
    return response.data
  }

  async updateAgent(agentId: string, agentData: AgentUpdate): Promise<Agent> {
    const response = await this.api.put(`/api/v1/agents/${agentId}`, agentData)
    return response.data
  }

  async deleteAgent(agentId: string): Promise<void> {
    await this.api.delete(`/api/v1/agents/${agentId}`)
  }

  async getAgentTemplates(): Promise<Agent[]> {
    const response = await this.api.get('/api/v1/agents/templates')
    return response.data
  }

  async testAgent(agentId: string, testRequest: AgentTestRequest): Promise<AgentTestResponse> {
    const response = await this.api.post(
      `/api/v1/agents/${agentId}/test`,
      testRequest
    )
    return response.data
  }

  // =============================================================================
  // AUTH ENDPOINTS
  // =============================================================================

  async login(email: string, password: string): Promise<{ token: string, user: any }> {
    const response = await this.api.post('/api/v1/auth/login', {
      email,
      password
    })
    return response.data
  }

  async register(email: string, password: string, name: string): Promise<{ token: string, user: any }> {
    const response = await this.api.post('/api/v1/auth/register', {
      email,
      password,
      name
    })
    return response.data
  }

  async logout(): Promise<void> {
    await this.api.post('/api/v1/auth/logout')
    localStorage.removeItem('auth_token')
  }

  async getCurrentUser(): Promise<any> {
    const response = await this.api.get('/api/v1/auth/me')
    return response.data
  }

  // =============================================================================
  // HEALTH CHECK
  // =============================================================================

  async healthCheck(): Promise<{ status: string, timestamp: string }> {
    const response = await this.api.get('/health')
    return response.data
  }
}

// Instância singleton
export const apiService = new ApiService()

// Exportar tipos
export type {
  ChatMessage,
  ChatRequest,
  ChatResponse,
  Agent,
  AgentCreate,
  AgentUpdate,
  AgentTestRequest,
  AgentTestResponse
} 