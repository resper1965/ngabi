import React from 'react'
import { Alert, AlertDescription, AlertTitle } from './ui/alert'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  XCircle,
  Bell,
  Shield,
  Zap
} from 'lucide-react'

export function AlertDemo() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bell className="w-5 h-5" />
            <span>Demonstração de Alertas</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Success Alert */}
          <Alert>
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertTitle>Sucesso!</AlertTitle>
            <AlertDescription>
              A operação foi concluída com sucesso. Os dados foram salvos corretamente.
            </AlertDescription>
          </Alert>

          {/* Warning Alert */}
          <Alert>
            <AlertTriangle className="h-4 w-4 text-yellow-600" />
            <AlertTitle>Atenção</AlertTitle>
            <AlertDescription>
              Esta ação não pode ser desfeita. Tem certeza que deseja continuar?
            </AlertDescription>
          </Alert>

          {/* Error Alert */}
          <Alert variant="destructive">
            <XCircle className="h-4 w-4" />
            <AlertTitle>Erro</AlertTitle>
            <AlertDescription>
              Ocorreu um erro ao processar sua solicitação. Tente novamente.
            </AlertDescription>
          </Alert>

          {/* Info Alert */}
          <Alert>
            <Info className="h-4 w-4 text-blue-600" />
            <AlertTitle>Informação</AlertTitle>
            <AlertDescription>
              O sistema será atualizado em 5 minutos. Salve seu trabalho.
            </AlertDescription>
          </Alert>

          {/* Security Alert */}
          <Alert>
            <Shield className="h-4 w-4 text-purple-600" />
            <AlertTitle>Segurança</AlertTitle>
            <AlertDescription>
              Sua sessão expira em 10 minutos. Faça login novamente para continuar.
            </AlertDescription>
          </Alert>

          {/* Performance Alert */}
          <Alert>
            <Zap className="h-4 w-4 text-orange-600" />
            <AlertTitle>Performance</AlertTitle>
            <AlertDescription>
              O sistema está funcionando com alta performance. Tempo de resposta: 0.2s
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Interactive Alerts */}
      <Card>
        <CardHeader>
          <CardTitle>Alertas Interativos</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex space-x-2">
            <Button 
              onClick={() => {
                // Simular notificação de sucesso
                console.log('Sucesso!')
              }}
              className="bg-green-600 hover:bg-green-700"
            >
              <CheckCircle className="w-4 h-4 mr-2" />
              Sucesso
            </Button>
            <Button 
              onClick={() => {
                // Simular notificação de aviso
                console.log('Aviso!')
              }}
              className="bg-yellow-600 hover:bg-yellow-700"
            >
              <AlertTriangle className="w-4 h-4 mr-2" />
              Aviso
            </Button>
            <Button 
              onClick={() => {
                // Simular notificação de erro
                console.log('Erro!')
              }}
              variant="destructive"
            >
              <XCircle className="w-4 h-4 mr-2" />
              Erro
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 