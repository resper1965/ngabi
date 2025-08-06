import { useState, useCallback } from 'react'

interface Message {
  id: string
  content: string
  sender: 'user' | 'agent'
  timestamp: Date
  agentName?: string
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedAgent, setSelectedAgent] = useState('n.Gabi')

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Thank you for your message: "${content}". I'm ${selectedAgent} and I'm here to help you. How can I assist you further?`,
        sender: 'agent',
        timestamp: new Date(),
        agentName: selectedAgent
      }

      setMessages(prev => [...prev, agentMessage])
      setIsLoading(false)
    }, 2000)
  }, [selectedAgent])

  return {
    messages,
    sendMessage,
    isLoading,
    selectedAgent,
    setSelectedAgent
  }
} 