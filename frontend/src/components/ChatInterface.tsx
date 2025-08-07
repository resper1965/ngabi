import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import { ChatMessage } from './chat-message'
import { ProcessingStatus } from './processing-status'
import { Send, Settings, Bot, Sparkles, RefreshCw } from 'lucide-react'
import { useChat } from '../hooks/use-chat'

export function ChatInterface() {
  const {
    messages,
    isLoading,
    agents,
    selectedAgent,
    sendMessage,
    loadAgents,
    setSelectedAgent,
    clearMessages
  } = useChat()

  const [inputMessage, setInputMessage] = useState('')

  const handleSend = async () => {
    if (inputMessage.trim() && !isLoading) {
      await sendMessage(inputMessage)
      setInputMessage('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleAgentChange = (agentId: string) => {
    const agent = agents.find(a => a.id === agentId)
    setSelectedAgent(agent || null)
  }

  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between p-4 md:p-6 border-b border-border bg-card/50 rounded-t-lg">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-primary" />
            <h1 className="text-xl md:text-2xl font-semibold text-card-foreground">
              {selectedAgent?.name || 'Chat AI'}
            </h1>
          </div>
          {selectedAgent && (
            <Badge variant="secondary" className="text-xs">
              {selectedAgent.model}
            </Badge>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <Select 
            value={selectedAgent?.id || ''} 
            onValueChange={handleAgentChange}
          >
            <SelectTrigger className="w-32 md:w-40">
              <SelectValue placeholder="Selecionar agente" />
            </SelectTrigger>
            <SelectContent>
              {agents.map((agent) => (
                <SelectItem key={agent.id} value={agent.id}>
                  {agent.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={loadAgents}
            disabled={isLoading}
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button 
            variant="outline" 
            size="sm"
            onClick={clearMessages}
          >
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col md:flex-row">
        {/* Messages */}
        <div className="flex-1 flex flex-col">
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-64 text-center">
                  <Bot className="w-16 h-16 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-semibold text-card-foreground mb-2">
                    Bem-vindo ao n.Gabi!
                  </h3>
                  <p className="text-muted-foreground max-w-md">
                    {selectedAgent 
                      ? `Converse com ${selectedAgent.name} sobre qualquer assunto.`
                      : 'Selecione um agente para começar a conversar.'
                    }
                  </p>
                  {selectedAgent && (
                    <div className="mt-4 p-3 bg-muted rounded-lg">
                      <p className="text-sm text-muted-foreground">
                        <strong>Descrição:</strong> {selectedAgent.description || 'Sem descrição'}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                messages.map((message) => (
                  <ChatMessage
                    key={message.id}
                    message={message}
                    agentName={selectedAgent?.name}
                  />
                ))
              )}
            </div>
          </ScrollArea>

          {/* Processing Status */}
          {isLoading && (
            <ProcessingStatus
              isProcessing={isLoading}
              progress={50}
              currentStep="Processando resposta..."
              totalSteps={4}
              currentStepIndex={2}
            />
          )}

          {/* Input Area */}
          <div className="p-4 border-t border-border bg-card/50">
            <div className="flex space-x-2">
              <Textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={
                  selectedAgent 
                    ? `Mensagem para ${selectedAgent.name}...`
                    : 'Selecione um agente para conversar...'
                }
                className="flex-1 min-h-[60px] resize-none"
                disabled={!selectedAgent || isLoading}
              />
              <Button
                onClick={handleSend}
                disabled={!inputMessage.trim() || !selectedAgent || isLoading}
                className="px-4"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Sidebar - Agent Info */}
        <div className="w-80 border-l border-border bg-card/50 p-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <span>Agente Selecionado</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {selectedAgent ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-card-foreground">{selectedAgent.name}</h4>
                    <p className="text-sm text-muted-foreground">{selectedAgent.description}</p>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Modelo:</span>
                      <span className="font-medium">{selectedAgent.model}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Temperatura:</span>
                      <span className="font-medium">{selectedAgent.temperature}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Max Tokens:</span>
                      <span className="font-medium">{selectedAgent.max_tokens}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Status:</span>
                      <Badge variant={selectedAgent.is_active ? "default" : "secondary"}>
                        {selectedAgent.is_active ? "Ativo" : "Inativo"}
                      </Badge>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-border">
                    <h5 className="font-medium text-card-foreground mb-2">Prompt do Sistema:</h5>
                    <p className="text-sm text-muted-foreground bg-muted p-2 rounded">
                      {selectedAgent.system_prompt}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <Bot className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">
                    Selecione um agente para ver suas configurações
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
} 