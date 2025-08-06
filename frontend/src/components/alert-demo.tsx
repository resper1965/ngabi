import { Alert, AlertDescription, AlertTitle } from './ui/alert'
import { Terminal, AlertTriangle, Info, CheckCircle } from 'lucide-react'

export function AlertDemo() {
  return (
    <div className="space-y-4">
      <Alert>
        <Terminal className="h-4 w-4" />
        <AlertTitle>Heads up!</AlertTitle>
        <AlertDescription>
          You can add components to your app using the cli.
        </AlertDescription>
      </Alert>
      
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          Your session has expired. Please log in again.
        </AlertDescription>
      </Alert>
      
      <Alert>
        <Info className="h-4 w-4" />
        <AlertTitle>Note</AlertTitle>
        <AlertDescription>
          Add your components to the registry to use them in your app.
        </AlertDescription>
      </Alert>
      
      <Alert>
        <CheckCircle className="h-4 w-4" />
        <AlertTitle>Success</AlertTitle>
        <AlertDescription>
          Your changes have been saved successfully.
        </AlertDescription>
      </Alert>
    </div>
  )
} 