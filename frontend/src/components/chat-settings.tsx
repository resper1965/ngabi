import React from 'react'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from './ui/accordion'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Switch } from './ui/switch'
import { Label } from './ui/label'
import { Badge } from './ui/badge'
import { 
  Settings, 
  Bot, 
  Database, 
  Shield, 
  Palette, 
  Zap,
  ChevronDown
} from 'lucide-react'

interface ChatSettingsProps {
  onSave?: (settings: any) => void
}

export function ChatSettings({ onSave }: ChatSettingsProps) {
  const [settings, setSettings] = React.useState({
    agentName: 'n.Gabi',
    model: 'gpt-4',
    temperature: 0.7,
    maxTokens: 1000,
    enableStreaming: true,
    enableHistory: true,
    theme: 'auto',
    language: 'pt-BR'
  })

  const handleSettingChange = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Settings className="w-5 h-5" />
          <span>Chat Settings</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {/* Agent Configuration */}
          <AccordionItem value="agent">
            <AccordionTrigger className="flex items-center space-x-2">
              <Bot className="w-4 h-4" />
              <span>Agent Configuration</span>
              <Badge variant="secondary" className="ml-2">AI</Badge>
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="agent-name">Agent Name</Label>
                  <Input
                    id="agent-name"
                    value={settings.agentName}
                    onChange={(e) => handleSettingChange('agentName', e.target.value)}
                    placeholder="Enter agent name"
                  />
                </div>
                <div>
                  <Label htmlFor="model">AI Model</Label>
                  <Select value={settings.model} onValueChange={(value) => handleSettingChange('model', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select model" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="gpt-4">GPT-4</SelectItem>
                      <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                      <SelectItem value="claude-3">Claude 3</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="temperature">Temperature</Label>
                    <Input
                      id="temperature"
                      type="number"
                      min="0"
                      max="2"
                      step="0.1"
                      value={settings.temperature}
                      onChange={(e) => handleSettingChange('temperature', parseFloat(e.target.value))}
                    />
                  </div>
                  <div>
                    <Label htmlFor="max-tokens">Max Tokens</Label>
                    <Input
                      id="max-tokens"
                      type="number"
                      min="100"
                      max="4000"
                      value={settings.maxTokens}
                      onChange={(e) => handleSettingChange('maxTokens', parseInt(e.target.value))}
                    />
                  </div>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Knowledge Base */}
          <AccordionItem value="knowledge">
            <AccordionTrigger className="flex items-center space-x-2">
              <Database className="w-4 h-4" />
              <span>Knowledge Base</span>
              <Badge variant="outline" className="ml-2">KB</Badge>
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label htmlFor="enable-history">Enable Chat History</Label>
                  <Switch
                    id="enable-history"
                    checked={settings.enableHistory}
                    onCheckedChange={(checked) => handleSettingChange('enableHistory', checked)}
                  />
                </div>
                <div>
                  <Label>Selected Knowledge Bases</Label>
                  <div className="mt-2 space-y-2">
                    {['General Knowledge', 'Technical Docs', 'Company Policies'].map((kb) => (
                      <div key={kb} className="flex items-center space-x-2">
                        <input type="checkbox" id={kb} className="rounded" />
                        <Label htmlFor={kb} className="text-sm">{kb}</Label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Security & Privacy */}
          <AccordionItem value="security">
            <AccordionTrigger className="flex items-center space-x-2">
              <Shield className="w-4 h-4" />
              <span>Security & Privacy</span>
              <Badge variant="destructive" className="ml-2">SEC</Badge>
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label htmlFor="enable-streaming">Enable Streaming</Label>
                  <Switch
                    id="enable-streaming"
                    checked={settings.enableStreaming}
                    onCheckedChange={(checked) => handleSettingChange('enableStreaming', checked)}
                  />
                </div>
                <div>
                  <Label>Data Retention</Label>
                  <Select value="30" onValueChange={() => {}}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select retention period" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="7">7 days</SelectItem>
                      <SelectItem value="30">30 days</SelectItem>
                      <SelectItem value="90">90 days</SelectItem>
                      <SelectItem value="365">1 year</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Appearance */}
          <AccordionItem value="appearance">
            <AccordionTrigger className="flex items-center space-x-2">
              <Palette className="w-4 h-4" />
              <span>Appearance</span>
              <Badge variant="secondary" className="ml-2">UI</Badge>
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="theme">Theme</Label>
                  <Select value={settings.theme} onValueChange={(value) => handleSettingChange('theme', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select theme" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="light">Light</SelectItem>
                      <SelectItem value="dark">Dark</SelectItem>
                      <SelectItem value="auto">Auto</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="language">Language</Label>
                  <Select value={settings.language} onValueChange={(value) => handleSettingChange('language', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select language" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pt-BR">Português (Brasil)</SelectItem>
                      <SelectItem value="en-US">English (US)</SelectItem>
                      <SelectItem value="es-ES">Español</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Performance */}
          <AccordionItem value="performance">
            <AccordionTrigger className="flex items-center space-x-2">
              <Zap className="w-4 h-4" />
              <span>Performance</span>
              <Badge variant="outline" className="ml-2">PERF</Badge>
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div>
                  <Label>Response Time</Label>
                  <div className="mt-2 text-sm text-muted-foreground">
                    Average: 1.2s | Peak: 3.5s
                  </div>
                </div>
                <div>
                  <Label>Memory Usage</Label>
                  <div className="mt-2 text-sm text-muted-foreground">
                    Current: 128MB | Peak: 256MB
                  </div>
                </div>
                <div>
                  <Label>Active Connections</Label>
                  <div className="mt-2 text-sm text-muted-foreground">
                    WebSocket: 12 | HTTP: 45
                  </div>
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>

        {/* Save Button */}
        <div className="mt-6 flex justify-end">
          <Button onClick={() => onSave?.(settings)}>
            Save Settings
          </Button>
        </div>
      </CardContent>
    </Card>
  )
} 