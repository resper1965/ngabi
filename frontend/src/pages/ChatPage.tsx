import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { ChatMessage } from '../components/chat-message';
import { ProcessingStatus } from '../components/processing-status';
import { Send, Bot, User, Database, Settings } from 'lucide-react';

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

export function ChatPage({ 
  agentName, 
  onSendMessage, 
  messages = [], 
  knowledgeBases = [], 
  isLoading = false 
}: ChatPageProps) {
  const [message, setMessage] = useState('');
  const [selectedAgent, setSelectedAgent] = useState(agentName);
  const [selectedMode, setSelectedMode] = useState('daily');
  const [selectedKBs, setSelectedKBs] = useState<string[]>([]);
  const [processingProgress, setProcessingProgress] = useState(0);

  const handleSendMessage = () => {
    if (!message.trim()) return;
    
    onSendMessage?.(message, selectedMode, selectedKBs);
    setMessage('');
    
    // Simular progresso de processamento
    if (isLoading) {
      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        setProcessingProgress(progress);
        if (progress >= 100) {
          clearInterval(interval);
          setProcessingProgress(0);
        }
      }, 200);
    }
  };

  const handleKBChange = (kbId: string, checked: boolean) => {
    if (checked) {
      setSelectedKBs([...selectedKBs, kbId]);
    } else {
      setSelectedKBs(selectedKBs.filter(id => id !== kbId));
    }
  };

  return (
    <div className="h-full flex flex-col space-y-4">
      {/* Header com título e AgentSelector */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h1 className="text-2xl font-bold text-white">Chat com {selectedAgent}</h1>
          <Badge variant="outline" className="text-xs">
            {selectedMode === 'daily' ? 'Uso Cotidiano' : 'Escrita Longa'}
          </Badge>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-48">
            <Select value={selectedAgent} onValueChange={setSelectedAgent}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Selecione um agente" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="n.Gabi">n.Gabi</SelectItem>
                <SelectItem value="assistant">Assistente</SelectItem>
                <SelectItem value="specialist">Especialista</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button variant="outline" size="icon">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* KBSelector */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="w-5 h-5 text-gray-500" />
            <span>Bases de Conhecimento</span>
            <Badge variant="secondary" className="text-xs">
              {selectedKBs.length} selecionadas
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            {knowledgeBases.map((kb) => (
              <label key={kb.id} className="flex items-center space-x-2">
                <Checkbox 
                  id={kb.id}
                  checked={selectedKBs.includes(kb.id)}
                  onCheckedChange={(checked) => handleKBChange(kb.id, checked as boolean)}
                />
                <span className="text-sm">{kb.name}</span>
              </label>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* ModeSelector */}
      <div className="flex items-center space-x-4">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Modo:</span>
        <div className="w-56">
          <Select value={selectedMode} onValueChange={setSelectedMode}>
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

      {/* Processing Status */}
      <ProcessingStatus 
        isProcessing={isLoading}
        progress={processingProgress}
        currentStep="Processando resposta..."
        totalSteps={4}
        currentStepIndex={Math.floor(processingProgress / 25)}
      />

      {/* MessageList */}
      <Card className="flex-1 min-h-0">
        <CardContent className="p-4 h-full flex flex-col">
          <ScrollArea className="flex-1">
            <div className="space-y-4 mb-4">
              {messages.length === 0 ? (
                <div className="flex justify-start">
                  <ChatMessage
                    id="welcome"
                    content="Olá! Como posso ajudá-lo hoje?"
                    sender="agent"
                    timestamp={new Date()}
                    agentName={selectedAgent}
                  />
                </div>
              ) : (
                messages.map((msg) => (
                  <ChatMessage
                    key={msg.id}
                    id={msg.id}
                    content={msg.content}
                    sender={msg.sender}
                    timestamp={msg.timestamp}
                    agentName={selectedAgent}
                    isTyping={isLoading && msg.sender === 'agent'}
                  />
                ))
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* MessageInput */}
      <form className="flex space-x-2 pt-2" onSubmit={(e) => { 
        e.preventDefault(); 
        handleSendMessage();
      }}>
        <Textarea
          className="flex-1 resize-none"
          placeholder="Digite sua mensagem..."
          rows={2}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={isLoading}
        />
        <Button type="submit" size="sm" className="h-10" disabled={isLoading || !message.trim()}>
          <Send className="w-4 h-4" />
        </Button>
      </form>
    </div>
  );
} 