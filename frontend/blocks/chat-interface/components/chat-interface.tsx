import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/registry/new-york/card'
import { Button } from '@/registry/new-york/button'
import { Input } from '@/registry/new-york/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/registry/new-york/select'
import { ScrollArea } from '@/registry/new-york/scroll-area'
import { Badge } from '@/registry/new-york/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/registry/new-york/avatar'
import { Separator } from '@/registry/new-york/separator'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/registry/new-york/tooltip'
import { Progress } from '@/registry/new-york/progress'
import { Send, Bot, User, Clock, Settings } from 'lucide-react'

interface Message {
  id: string
  content: string
  sender: 'user' | 'agent'
  timestamp: Date
  agentName?: string
}

interface ChatInterfaceProps {
  messages: Message[]
  onSendMessage: (message: string) => void
  isLoading: boolean
  selectedAgent: string
  onAgentChange: (agent: string) => void
}

export function ChatInterface({
  messages,
  onSendMessage,
  isLoading,
  selectedAgent,
  onAgentChange
}: ChatInterfaceProps) {
  const [message, setMessage] = useState('')

  const handleSendMessage = () => {
    if (!message.trim()) return
    onSendMessage(message)
    setMessage('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full space-y-4">
      {/* Header with Agent Selection */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h2 className="text-xl font-semibold">Chat with {selectedAgent}</h2>
          <Badge variant="outline">AI Assistant</Badge>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={selectedAgent} onValueChange={onAgentChange}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Select agent" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="n.Gabi">n.Gabi</SelectItem>
              <SelectItem value="Assistant">Assistant</SelectItem>
              <SelectItem value="Specialist">Specialist</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="icon">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Processing Status */}
      {isLoading && (
        <Card className="bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Bot className="w-4 h-4" />
              <span className="text-sm font-medium">Processing response...</span>
            </div>
            <Progress value={33} className="h-2" />
          </CardContent>
        </Card>
      )}

      {/* Messages */}
      <Card className="flex-1 min-h-0">
        <CardContent className="p-4 h-full flex flex-col">
          <ScrollArea className="flex-1">
            <div className="space-y-4">
              {messages.length === 0 ? (
                <div className="flex justify-center items-center h-32 text-muted-foreground">
                  <div className="text-center">
                    <Bot className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>Start a conversation with {selectedAgent}</p>
                  </div>
                </div>
              ) : (
                messages.map((msg) => (
                  <ChatMessage key={msg.id} message={msg} />
                ))
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Input */}
      <div className="flex space-x-2">
        <Input
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          className="flex-1"
        />
        <Button onClick={handleSendMessage} disabled={isLoading || !message.trim()}>
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </div>
  )
}

function ChatMessage({ message }: { message: Message }) {
  const isUser = message.sender === 'user'
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start space-x-3 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Avatar className="w-8 h-8">
                <AvatarImage src={isUser ? undefined : `/api/avatar/${message.agentName}`} />
                <AvatarFallback className={isUser ? 'bg-blue-500 text-white' : 'bg-green-500 text-white'}>
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </AvatarFallback>
              </Avatar>
            </TooltipTrigger>
            <TooltipContent>
              <p>{isUser ? 'You' : message.agentName || 'AI Assistant'}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
        
        <Card className={`${isUser ? 'bg-blue-500 text-white' : 'bg-muted'}`}>
          <CardContent className="p-3">
            <div className="flex items-center justify-between mb-2">
              <Badge variant={isUser ? 'secondary' : 'default'} className="text-xs">
                {isUser ? 'You' : message.agentName || 'AI Assistant'}
              </Badge>
              <div className="flex items-center space-x-1 text-xs opacity-70">
                <Clock className="w-3 h-3" />
                <span>{message.timestamp.toLocaleTimeString()}</span>
              </div>
            </div>
            
            <Separator className="mb-2" />
            
            <div className="text-sm">
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 