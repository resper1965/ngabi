import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { Separator } from './ui/separator';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';
import { Bot, User, Clock } from 'lucide-react';

interface ChatMessageProps {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: Date;
  agentName?: string;
  isTyping?: boolean;
}

export function ChatMessage({ 
  content, 
  sender, 
  timestamp, 
  agentName = 'n.Gabi',
  isTyping = false 
}: ChatMessageProps) {
  const isUser = sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex items-start space-x-3 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Avatar className="w-8 h-8">
                <AvatarImage src={isUser ? undefined : `/api/avatar/${agentName}`} />
                <AvatarFallback className={isUser ? 'bg-[#00ade8] text-white' : 'bg-green-500 text-white'}>
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </AvatarFallback>
              </Avatar>
            </TooltipTrigger>
            <TooltipContent>
              <p>{isUser ? 'Você' : agentName}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
        
        <Card className={`${isUser ? 'bg-[#00ade8] text-white' : 'bg-gray-800 text-gray-100'}`}>
          <CardContent className="p-3">
            <div className="flex items-center justify-between mb-2">
              <Badge variant={isUser ? 'secondary' : 'default'} className="text-xs">
                {isUser ? 'Você' : agentName}
              </Badge>
              <div className="flex items-center space-x-1 text-xs opacity-70">
                <Clock className="w-3 h-3" />
                <span>{timestamp.toLocaleTimeString('pt-BR', { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}</span>
              </div>
            </div>
            
            <Separator className="mb-2" />
            
            <div className="text-sm">
              {isTyping ? (
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              ) : (
                <p className="whitespace-pre-wrap">{content}</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 