import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { Separator } from './ui/separator';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';
import { Bot, User, Clock } from 'lucide-react';

interface ChatMessageProps {
  message: {
    id: string;
    content: string;
    sender: 'user' | 'agent';
    timestamp: Date;
  };
  agentName?: string;
  isTyping?: boolean;
}

export function ChatMessage({ 
  message, 
  agentName = 'n.Gabi',
  isTyping = false 
}: ChatMessageProps) {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start space-x-2 max-w-[80%]`}>
        <Avatar className={`h-8 w-8 ${isUser ? 'ml-2' : 'mr-2'}`}>
          <AvatarImage src={isUser ? undefined : undefined} />
          <AvatarFallback className={isUser ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}>
            {isUser ? 'U' : 'G'}
          </AvatarFallback>
        </Avatar>
        
        <Card className={`${isUser ? 'bg-primary text-primary-foreground' : 'bg-card text-card-foreground'} border-0`}>
          <CardContent className="p-3">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium opacity-80">
                {isUser ? 'Você' : agentName}
              </span>
              <div className="flex items-center space-x-1 text-xs opacity-70">
                <span>{message.timestamp.toLocaleTimeString('pt-BR', { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}</span>
              </div>
            </div>
            <div>
              {isTyping ? (
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              ) : (
                <p className="whitespace-pre-wrap">{message.content}</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 