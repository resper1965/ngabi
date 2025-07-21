import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Moon, Sun, Thermometer, Download, Upload, Save, RefreshCw } from 'lucide-react';

/**
 * WIREFRAME TEXTUAL:
 * 
 * ┌─────────────────────────────────────────────────────────┐
 * │ Configurações Gerais                                   │
 * ├─────────────────────────────────────────────────────────┤
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Aparência                                           │ │
 * │ │                                                     │ │
 * │ │ Tema: [☀️ Claro] [🌙 Escuro]                       │ │
 * │ │                                                     │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Configurações do Modelo                             │ │
 * │ │                                                     │ │
 * │ │ Temperatura: [▁▂▃▄▅▆▇█] 0.7                        │ │
 * │ │                                                     │ │
 * │ │ Criatividade: [▁▂▃▄▅▆▇█] 0.8                      │ │
 * │ │                                                     │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Workflows                                           │ │
 * │ │                                                     │ │
 * │ │ [📥 Exportar Workflows]                             │ │
 * │ │ [📤 Importar Workflows]                             │ │
 * │ │ [🔄 Sincronizar com n8n]                            │ │
 * │ │                                                     │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ [Salvar Configurações]                                 │
 * │                                                         │
 * └─────────────────────────────────────────────────────────┘
 */

interface SettingsData {
  theme: 'light' | 'dark';
  modelSettings: {
    temperature: number;
    creativity: number;
    maxTokens: number;
  };
  notifications: {
    email: boolean;
    browser: boolean;
    slack: boolean;
  };
  autoSave: boolean;
}

interface SettingsPageProps {
  settings?: SettingsData;
  onSave?: (data: SettingsData) => void;
  onExportWorkflows?: () => void;
  onImportWorkflows?: (file: File) => void;
  onSyncWorkflows?: () => void;
  isLoading?: boolean;
}

export function SettingsPage({
  settings,
  onSave,
  onExportWorkflows,
  onImportWorkflows,
  onSyncWorkflows,
  isLoading = false
}: SettingsPageProps) {
  const [formData, setFormData] = useState<SettingsData>({
    theme: settings?.theme || 'light',
    modelSettings: {
      temperature: settings?.modelSettings.temperature || 0.7,
      creativity: settings?.modelSettings.creativity || 0.8,
      maxTokens: settings?.modelSettings.maxTokens || 2048
    },
    notifications: {
      email: settings?.notifications.email || false,
      browser: settings?.notifications.browser || true,
      slack: settings?.notifications.slack || false
    },
    autoSave: settings?.autoSave || true
  });

  const handleSave = () => {
    // TODO: chamar API - salvar configurações
    if (onSave) {
      onSave(formData);
    }
  };

  const handleThemeChange = (theme: 'light' | 'dark') => {
    setFormData({ ...formData, theme });
    // TODO: implementar mudança de tema global
  };

  const handleModelSettingChange = (setting: keyof SettingsData['modelSettings'], value: number) => {
    setFormData({
      ...formData,
      modelSettings: {
        ...formData.modelSettings,
        [setting]: value
      }
    });
  };

  const handleNotificationChange = (type: keyof SettingsData['notifications'], value: boolean) => {
    setFormData({
      ...formData,
      notifications: {
        ...formData.notifications,
        [type]: value
      }
    });
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && onImportWorkflows) {
      // TODO: chamar API - importar workflows
      onImportWorkflows(file);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configurações Gerais</h1>
        <p className="text-gray-600">Personalize a experiência da plataforma</p>
      </div>

      {/* Appearance Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            {formData.theme === 'light' ? <Sun className="w-5 h-5 mr-2" /> : <Moon className="w-5 h-5 mr-2" />}
            Aparência
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Tema
              </label>
              <div className="flex space-x-3">
                <Button
                  variant={formData.theme === 'light' ? 'default' : 'outline'}
                  onClick={() => handleThemeChange('light')}
                  className="flex items-center space-x-2"
                >
                  <Sun className="w-4 h-4" />
                  <span>Claro</span>
                </Button>
                <Button
                  variant={formData.theme === 'dark' ? 'default' : 'outline'}
                  onClick={() => handleThemeChange('dark')}
                  className="flex items-center space-x-2"
                >
                  <Moon className="w-4 h-4" />
                  <span>Escuro</span>
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Model Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Thermometer className="w-5 h-5 mr-2" />
            Configurações do Modelo
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Temperature */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Temperatura: {formData.modelSettings.temperature}
              </label>
              <div className="space-y-2">
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={formData.modelSettings.temperature}
                  onChange={(e) => handleModelSettingChange('temperature', parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Mais Determinístico</span>
                  <span>Mais Criativo</span>
                </div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Controla a aleatoriedade das respostas do modelo
              </p>
            </div>

            {/* Creativity */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Criatividade: {formData.modelSettings.creativity}
              </label>
              <div className="space-y-2">
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={formData.modelSettings.creativity}
                  onChange={(e) => handleModelSettingChange('creativity', parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Mais Conservador</span>
                  <span>Mais Inovador</span>
                </div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Controla o nível de criatividade nas respostas
              </p>
            </div>

            {/* Max Tokens */}
            <div>
              <label htmlFor="maxTokens" className="block text-sm font-medium text-gray-700 mb-2">
                Máximo de Tokens
              </label>
              <Input
                id="maxTokens"
                type="number"
                min="100"
                max="4096"
                step="100"
                value={formData.modelSettings.maxTokens}
                onChange={(e) => handleModelSettingChange('maxTokens', parseInt(e.target.value))}
              />
              <p className="text-xs text-gray-500 mt-1">
                Limite máximo de tokens por resposta
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle>Notificações</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Notificações por E-mail</label>
                <p className="text-xs text-gray-500">Receba notificações importantes por e-mail</p>
              </div>
              <input
                type="checkbox"
                checked={formData.notifications.email}
                onChange={(e) => handleNotificationChange('email', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Notificações do Navegador</label>
                <p className="text-xs text-gray-500">Receba notificações push no navegador</p>
              </div>
              <input
                type="checkbox"
                checked={formData.notifications.browser}
                onChange={(e) => handleNotificationChange('browser', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Notificações do Slack</label>
                <p className="text-xs text-gray-500">Envie notificações para o Slack</p>
              </div>
              <input
                type="checkbox"
                checked={formData.notifications.slack}
                onChange={(e) => handleNotificationChange('slack', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Salvamento Automático</label>
                <p className="text-xs text-gray-500">Salve automaticamente as configurações</p>
              </div>
              <input
                type="checkbox"
                checked={formData.autoSave}
                onChange={(e) => setFormData({ ...formData, autoSave: e.target.checked })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Workflows */}
      <Card>
        <CardHeader>
          <CardTitle>Workflows</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button
                variant="outline"
                onClick={onExportWorkflows}
                className="flex items-center space-x-2"
              >
                <Download className="w-4 h-4" />
                <span>Exportar Workflows</span>
              </Button>

              <Button
                variant="outline"
                onClick={() => document.getElementById('workflow-upload')?.click()}
                className="flex items-center space-x-2"
              >
                <Upload className="w-4 h-4" />
                <span>Importar Workflows</span>
              </Button>

              <Button
                variant="outline"
                onClick={onSyncWorkflows}
                className="flex items-center space-x-2"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Sincronizar com n8n</span>
              </Button>
            </div>

            <input
              id="workflow-upload"
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              className="hidden"
            />

            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="text-sm font-medium text-blue-900 mb-2">Dica</h4>
              <p className="text-sm text-blue-700">
                Exporte seus workflows para fazer backup ou importe workflows de outros ambientes.
                A sincronização com n8n atualiza automaticamente os workflows da plataforma.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button
          onClick={handleSave}
          disabled={isLoading}
          className="px-8"
        >
          <Save className="w-4 h-4 mr-2" />
          {isLoading ? 'Salvando...' : 'Salvar Configurações'}
        </Button>
      </div>
    </div>
  );
} 