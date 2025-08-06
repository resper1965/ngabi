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
import { Send, Settings, MessageSquare } from 'lucide-react'

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
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-[#00ade8] rounded-full"></div>
          <h1 className="text-xl font-semibold text-white">{agentName}</h1>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={selectedMode} onValueChange={setSelectedMode}>
            <SelectTrigger className="w-32">
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
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 p-4">
          <ScrollArea className="h-full">
            <div className="space-y-4">
              {messages.length === 0 ? (
                <div className="text-center py-8 text-gray-400">
                  <MessageSquare className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Nenhuma mensagem ainda</p>
                  <p className="text-sm">Comece uma conversa com {agentName}</p>
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

        {/* Knowledge Bases */}
        <Card className="m-4">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MessageSquare className="w-5 h-5 text-gray-500" />
              <span>Bases de Conhecimento</span>
              <Badge variant="secondary" className="text-xs">
                {selectedKBs.length} selecionadas
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {knowledgeBases.map((kb) => (
                <div key={kb.id} className="flex items-center space-x-2">
                  <Checkbox
                    id={kb.id}
                    checked={selectedKBs.includes(kb.id)}
                    onCheckedChange={(checked) => handleKBChange(kb.id, checked as boolean)}
                  />
                  <label htmlFor={kb.id} className="text-sm text-gray-300">
                    {kb.name}
                  </label>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex space-x-2">
            <Textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Digite sua mensagem..."
              className="flex-1 resize-none"
              disabled={isLoading}
              rows={3}
            />
            <Button
              onClick={handleSend}
              disabled={!inputMessage.trim() || isLoading}
              className="px-4"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
} 