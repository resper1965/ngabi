import React from 'react'
import { ChatInterface } from './components/chat-interface'
import { useChat } from './hooks/use-chat'
import { formatTimestamp } from './lib/utils'

export default function ChatInterfacePage() {
  const { messages, sendMessage, isLoading, selectedAgent, setSelectedAgent } = useChat()

  return (
    <div className="h-screen bg-background">
      <div className="container mx-auto h-full p-4">
        <div className="flex flex-col h-full space-y-4">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Chat Interface</h1>
              <p className="text-muted-foreground">
                A modern chat interface with AI agents
              </p>
            </div>
          </div>

          {/* Chat Interface */}
          <ChatInterface
            messages={messages}
            onSendMessage={sendMessage}
            isLoading={isLoading}
            selectedAgent={selectedAgent}
            onAgentChange={setSelectedAgent}
          />
        </div>
      </div>
    </div>
  )
} 