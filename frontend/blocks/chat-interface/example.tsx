import React from 'react'
import { ChatInterface } from './components/chat-interface'
import { useChat } from './hooks/use-chat'

export function ChatInterfaceExample() {
  const { messages, sendMessage, isLoading, selectedAgent, setSelectedAgent } = useChat()

  return (
    <div className="h-screen bg-background">
      <div className="container mx-auto h-full p-4">
        <div className="flex flex-col h-full space-y-4">
          {/* Header */}
          <div className="text-center">
            <h1 className="text-3xl font-bold">Chat Interface Example</h1>
            <p className="text-muted-foreground mt-2">
              A modern chat interface with AI agents
            </p>
          </div>

          {/* Chat Interface */}
          <div className="flex-1">
            <ChatInterface
              messages={messages}
              onSendMessage={sendMessage}
              isLoading={isLoading}
              selectedAgent={selectedAgent}
              onAgentChange={setSelectedAgent}
            />
          </div>

          {/* Footer */}
          <div className="text-center text-sm text-muted-foreground">
            <p>Built with shadcn/ui and n.Gabi</p>
          </div>
        </div>
      </div>
    </div>
  )
} 