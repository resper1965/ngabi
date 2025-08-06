import { Bell, X } from 'lucide-react'
import { useState } from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { ScrollArea } from './ui/scroll-area'
import { Separator } from './ui/separator'

interface Notification {
  id: string
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  timestamp: Date
  read: boolean
}

export const NotificationCenter = () => {
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: '1',
      title: 'Sistema Online',
      message: 'O n.Gabi está funcionando normalmente',
      type: 'success',
      timestamp: new Date(),
      read: false
    },
    {
      id: '2',
      title: 'Atualização Disponível',
      message: 'Nova versão do sistema está disponível',
      type: 'info',
      timestamp: new Date(Date.now() - 3600000),
      read: true
    }
  ])

  const unreadCount = notifications.filter(n => !n.read).length

  const markAsRead = (id: string) => {
    setNotifications(prev => 
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    )
  }

  const clearAll = () => {
    setNotifications([])
  }

  return (
    <div className="relative">
      <Button variant="outline" size="icon" className="relative">
        <Bell className="h-4 w-4" />
        {unreadCount > 0 && (
          <Badge variant="destructive" className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
            {unreadCount}
          </Badge>
        )}
      </Button>
    </div>
  )
} 