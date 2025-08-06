import React from 'react'
import { useTheme } from '../hooks/use-theme'
import { Button } from './ui/button'

export function ThemeTest() {
  const { theme, setTheme, mounted } = useTheme()

  if (!mounted) {
    return <div>Carregando tema...</div>
  }

  return (
    <div className="p-8 space-y-4">
      <h1 className="text-2xl font-bold text-foreground">
        Teste do Tema OKLCH - n.Gabi
      </h1>
      
      <div className="space-y-2">
        <p className="text-muted-foreground">
          Tema atual: <span className="font-semibold text-foreground">{theme}</span>
        </p>
        
        <div className="flex space-x-2">
          <Button 
            variant={theme === 'light' ? 'default' : 'outline'}
            onClick={() => setTheme('light')}
          >
            Claro
          </Button>
          <Button 
            variant={theme === 'dark' ? 'default' : 'outline'}
            onClick={() => setTheme('dark')}
          >
            Escuro
          </Button>
          <Button 
            variant={theme === 'system' ? 'default' : 'outline'}
            onClick={() => setTheme('system')}
          >
            Sistema
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 border rounded-lg bg-card text-card-foreground">
          <h3 className="font-semibold mb-2">Card</h3>
          <p className="text-muted-foreground">
            Este é um exemplo de card com o tema OKLCH aplicado.
          </p>
        </div>
        
        <div className="p-4 border rounded-lg bg-primary text-primary-foreground">
          <h3 className="font-semibold mb-2">Primary</h3>
          <p>
            Este é um exemplo de componente primary com o tema OKLCH.
          </p>
        </div>
        
        <div className="p-4 border rounded-lg bg-secondary text-secondary-foreground">
          <h3 className="font-semibold mb-2">Secondary</h3>
          <p>
            Este é um exemplo de componente secondary com o tema OKLCH.
          </p>
        </div>
        
        <div className="p-4 border rounded-lg bg-accent text-accent-foreground">
          <h3 className="font-semibold mb-2">Accent</h3>
          <p>
            Este é um exemplo de componente accent com o tema OKLCH.
          </p>
        </div>
      </div>

      <div className="p-4 border rounded-lg bg-sidebar text-sidebar-foreground">
        <h3 className="font-semibold mb-2">Sidebar</h3>
        <p>
          Este é um exemplo de componente sidebar com o tema OKLCH.
        </p>
      </div>
    </div>
  )
} 