import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { ChatMessage } from '../components/chat-message'
import { ProcessingStatus } from '../components/processing-status'
import { Send, Settings, MessageSquare, Bot, Sparkles } from 'lucide-react'

interface Message {
  id: string
  content: string
  sender: 'user' | 'agent'
  timestamp: Date
}

interface KnowledgeBase {
  id: string
  name: string
  selected: boolean
}

interface ChatPageProps {
  agentName: string
  onSendMessage: (message: string, mode: string, selectedKBs: string[]) => void
  messages: Message[]
  knowledgeBases: KnowledgeBase[]
  isLoading: boolean
}

export function ChatPage({
  agentName,
  onSendMessage,
  messages,
  knowledgeBases,
  isLoading
}: ChatPageProps) {
  const [inputMessage, setInputMessage] = useState('')
  const [selectedMode, setSelectedMode] = useState('chat')
  const [selectedKBs, setSelectedKBs] = useState<string[]>([])

  const handleSend = () => {
    if (inputMessage.trim() && !isLoading) {
      onSendMessage(inputMessage, selectedMode, selectedKBs)
      setInputMessage('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleKBChange = (kbId: string, checked: boolean) => {
    if (checked) {
      setSelectedKBs(prev => [...prev, kbId])
    } else {
      setSelectedKBs(prev => prev.filter(id => id !== kbId))
    }
  }

  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between p-4 md:p-6 border-b border-border bg-card/50 rounded-t-lg">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-primary" />
            <h1 className="text-xl md:text-2xl font-semibold text-card-foreground">{agentName}</h1>
          </div>
          <Badge variant="secondary" className="text-xs">
            {selectedMode}
          </Badge>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={selectedMode} onValueChange={setSelectedMode}>
            <SelectTrigger className="w-32 md:w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="chat">Chat</SelectItem>
              <SelectItem value="analysis">Análise</SelectItem>
              <SelectItem value="creative">Criativo</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col md:flex-row">
        {/* Messages */}
        <div className="flex-1 p-4 md:p-6">
          <ScrollArea className="h-full">
            <div className="space-y-4">
              {messages.length === 0 ? (
                <div className="text-center py-12">
                  <div className="flex justify-center mb-6">
                    <div className="w-16 h-16 bg-gray-800 rounded-2xl flex items-center justify-center">
                      <MessageSquare className="w-8 h-8 text-gray-400" />
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">
                    Bem-vindo ao {agentName}
                  </h3>
                  <p className="text-gray-400 mb-4">
                    Comece uma conversa para explorar as capacidades do agente
                  </p>
                  <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
                    <Sparkles className="w-4 h-4" />
                    <span>Powered by AI</span>
                  </div>
                </div>
              ) : (
                messages.map((message) => (
                  <ChatMessage
                    key={message.id}
                    message={message}
                    agentName={agentName}
                  />
                ))
              )}
              {isLoading && (
                <ChatMessage
                  message={{
                    id: 'loading',
                    content: '',
                    sender: 'agent',
                    timestamp: new Date()
                  }}
                  agentName={agentName}
                  isTyping={true}
                />
              )}
            </div>
          </ScrollArea>
        </div>

        {/* Knowledge Bases Sidebar */}
        <div className="w-full md:w-80 p-4 md:p-6 border-t md:border-t-0 md:border-l border-gray-700 bg-gray-800/30">
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="w-5 h-5 text-[#00ade8]" />
                <span>Bases de Conhecimento</span>
                <Badge variant="secondary" className="text-xs">
                  {selectedKBs.length} selecionadas
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {knowledgeBases.map((kb) => (
                  <div key={kb.id} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-700/50 transition-colors">
                    <Checkbox
                      id={kb.id}
                      checked={selectedKBs.includes(kb.id)}
                      onCheckedChange={(checked) => handleKBChange(kb.id, checked as boolean)}
                    />
                    <label htmlFor={kb.id} className="text-sm text-gray-300 cursor-pointer flex-1">
                      {kb.name}
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 md:p-6 border-t border-gray-700 bg-gray-800/50 rounded-b-lg">
        <div className="flex space-x-3">
          <Textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite sua mensagem..."
            className="flex-1 resize-none min-h-[60px] max-h-[120px]"
            disabled={isLoading}
            rows={3}
          />
          <Button
            onClick={handleSend}
            disabled={!inputMessage.trim() || isLoading}
            className="px-6 h-[60px]"
            size="lg"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
        <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
          <span>Pressione Enter para enviar, Shift+Enter para nova linha</span>
          <span>{inputMessage.length} caracteres</span>
        </div>
      </div>
    </div>
  )
} 