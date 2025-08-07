import { useState, useEffect, useCallback } from 'react'
import { apiService, type ChatMessage as ApiChatMessage, type Agent } from '../services/api'

interface Message {
  id: string
  content: string
  sender: 'user' | 'agent'
  timestamp: Date
}

interface UseChatReturn {
  messages: Message[]
  isLoading: boolean
  agents: Agent[]
  selectedAgent: Agent | null
  sendMessage: (message: string, agentId?: string) => Promise<void>
  loadAgents: () => Promise<void>
  setSelectedAgent: (agent: Agent | null) => void
  clearMessages: () => void
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null)

  // Carregar agentes disponíveis
  const loadAgents = useCallback(async () => {
    try {
      const response = await apiService.getAgents()
      setAgents(response.agents)
      
      // Selecionar o primeiro agente por padrão
      if (response.agents.length > 0 && !selectedAgent) {
        setSelectedAgent(response.agents[0])
      }
    } catch (error) {
      console.error('Erro ao carregar agentes:', error)
    }
  }, [selectedAgent])

  // Enviar mensagem
  const sendMessage = useCallback(async (message: string, agentId?: string) => {
    if (!message.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: message,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await apiService.sendChatMessage({
        message,
        agent_id: agentId || selectedAgent?.id
      })

      const agentMessage: Message = {
        id: response.message_id,
        content: response.response,
        sender: 'agent',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, agentMessage])
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      
      // Adicionar mensagem de erro
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.',
        sender: 'agent',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [selectedAgent])

  // Limpar mensagens
  const clearMessages = useCallback(() => {
    setMessages([])
  }, [])

  // Carregar agentes na inicialização
  useEffect(() => {
    loadAgents()
  }, [loadAgents])

  return {
    messages,
    isLoading,
    agents,
    selectedAgent,
    sendMessage,
    loadAgents,
    setSelectedAgent,
    clearMessages
  }
} 