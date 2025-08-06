import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Bot, Cpu, Database, Network } from 'lucide-react';

interface ProcessingStatusProps {
  isProcessing: boolean;
  progress: number;
  currentStep: string;
  totalSteps: number;
  currentStepIndex: number;
}

export function ProcessingStatus({ 
  isProcessing, 
  progress, 
  currentStep, 
  totalSteps, 
  currentStepIndex 
}: ProcessingStatusProps) {
  if (!isProcessing) return null;

  const steps = [
    { name: 'Analisando', icon: <Cpu className="w-4 h-4" /> },
    { name: 'Consultando', icon: <Database className="w-4 h-4" /> },
    { name: 'Processando', icon: <Bot className="w-4 h-4" /> },
    { name: 'Enviando', icon: <Network className="w-4 h-4" /> }
  ];

  return (
    <Card className="mb-4 bg-gray-800 border-[#00ade8]">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm flex items-center space-x-2">
          <Bot className="w-4 h-4" />
          <span>Processando resposta...</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center justify-between text-xs text-gray-300">
          <span>Progresso</span>
          <span>{Math.round(progress)}%</span>
        </div>
        
        <Progress value={progress} className="h-2" />
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-xs">
            Passo {currentStepIndex + 1} de {totalSteps}
          </Badge>
          <span className="text-xs text-gray-300">
            {currentStep}
          </span>
        </div>
        
        <div className="flex space-x-2">
          {steps.map((step, index) => (
            <div
              key={index}
              className={`flex items-center space-x-1 text-xs ${
                index <= currentStepIndex 
                  ? 'text-[#00ade8]' 
                  : 'text-gray-500'
              }`}
            >
              {step.icon}
              <span>{step.name}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 