// import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Textarea } from '@/components/ui/textarea';
import { Send, Bot, User, Database } from 'lucide-react';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: Date;
}

interface KnowledgeBase {
  id: string;
  name: string;
  selected: boolean;
}

interface ChatPageProps {
  agentName: string;
  onSendMessage?: (message: string, mode: string, selectedKBs: string[]) => void;
  messages?: Message[];
  knowledgeBases?: KnowledgeBase[];
  isLoading?: boolean;
}

export function ChatPage({ agentName }: ChatPageProps) {
  // TODO: carregar agentes via fetchAgents()
  // TODO: carregar bases via fetchKBs()

  return (
    <div className="h-full flex flex-col space-y-4">
      {/* Header com título e AgentSelector */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Chat com {agentName}</h1>
        <div className="w-64">
          <Select>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Selecione um agente" />
            </SelectTrigger>
            <SelectContent>
              {/* TODO: mapear agentes do tenant */}
              <SelectItem value="agent1">Agente 1</SelectItem>
              <SelectItem value="agent2">Agente 2</SelectItem>
              <SelectItem value="agent3">Agente 3</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* KBSelector */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="w-5 h-5 text-gray-500" />
            <span>Bases de Conhecimento</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-6">
            {/* TODO: mapear bases de conhecimento */}
            <label className="flex items-center space-x-2">
              <Checkbox id="kb-livros" />
              <span>Livros</span>
            </label>
            <label className="flex items-center space-x-2">
              <Checkbox id="kb-processos" />
              <span>Processos</span>
            </label>
            <label className="flex items-center space-x-2">
              <Checkbox id="kb-jurisprudencia" />
              <span>Jurisprudência</span>
            </label>
          </div>
        </CardContent>
      </Card>

      {/* ModeSelector */}
      <div className="flex items-center space-x-4">
        <span className="text-sm font-medium text-gray-700">Modo:</span>
        <div className="w-56">
          <Select>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Selecione o modo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="daily">Uso Cotidiano</SelectItem>
              <SelectItem value="long">Escrita Longa</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* MessageList */}
      <Card className="flex-1 min-h-0">
        <CardContent className="p-4 h-full flex flex-col">
          <div className="flex-1 overflow-y-auto space-y-4 mb-4">
            {/* TODO: mapear mensagens */}
            <div className="flex justify-start">
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100 text-gray-800 flex items-start space-x-2">
                <Bot className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm">Olá! Como posso ajudar?</p>
                  <p className="text-xs mt-1 text-gray-500">09:00</p>
                </div>
              </div>
            </div>
            <div className="flex justify-end">
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-blue-500 text-white flex items-start space-x-2">
                <div className="flex-1">
                  <p className="text-sm">Preciso de ajuda com um processo.</p>
                  <p className="text-xs mt-1 text-blue-100">09:01</p>
                </div>
                <User className="w-4 h-4 mt-0.5 flex-shrink-0" />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* MessageInput */}
      <form className="flex space-x-2 pt-2" onSubmit={e => { e.preventDefault(); /* TODO: chamar sendChat({ agent_id, message, kb_filters, chatMode }) */ }}>
        <Textarea
          className="flex-1 resize-none"
          placeholder="Digite sua mensagem..."
          rows={2}
        />
        <Button type="submit" size="sm" className="h-10">
          <Send className="w-4 h-4" />
        </Button>
      </form>
    </div>
  );
} 