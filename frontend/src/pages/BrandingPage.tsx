import React, { useState, useRef } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Upload, Palette, Image, Save, Phone, Mail, MapPin } from 'lucide-react';

/**
 * WIREFRAME TEXTUAL:
 * 
 * ┌─────────────────────────────────────────────────────────┐
 * │ Branding & Identidade Visual                            │
 * ├─────────────────────────────────────────────────────────┤
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Logo da Empresa                                     │ │
 * │ │                                                     │ │
 * │ │ ┌─────────────────────────────────────────────────┐ │ │
 * │ │ │                                                 │ │ │
 * │ │ │              [Upload Logo]                      │ │ │
 * │ │ │                                                 │ │ │
 * │ │ └─────────────────────────────────────────────────┘ │ │
 * │ │                                                     │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Cores da Marca                                      │ │
 * │ │                                                     │ │
 * │ │ Cor Primária: [🟦] #3B82F6                         │ │
 * │ │ Cor Secundária: [🟨] #F59E0B                       │ │
 * │ │                                                     │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Informações de Contato                              │ │
 * │ │                                                     │ │
 * │ │ Telefone: [________________]                        │ │
 * │ │ E-mail: [________________]                          │ │
 * │ │ Endereço: [________________]                        │ │
 * │ │                                                     │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ [Salvar Configurações]                                 │
 * │                                                         │
 * └─────────────────────────────────────────────────────────┘
 */

interface BrandingData {
  logo?: File | string;
  primaryColor: string;
  secondaryColor: string;
  orchestratorName: string;
  contact: {
    phone: string;
    email: string;
    address: string;
  };
}

interface BrandingPageProps {
  branding?: BrandingData;
  onSave?: (data: BrandingData) => void;
  isLoading?: boolean;
}

export function BrandingPage({
  branding,
  onSave,
  isLoading = false
}: BrandingPageProps) {
  const [formData, setFormData] = useState<BrandingData>({
    logo: branding?.logo || '',
    primaryColor: branding?.primaryColor || '#3B82F6',
    secondaryColor: branding?.secondaryColor || '#F59E0B',
    orchestratorName: branding?.orchestratorName || 'Agente Orquestrador',
    contact: {
      phone: branding?.contact.phone || '',
      email: branding?.contact.email || '',
      address: branding?.contact.address || ''
    }
  });

  const [logoPreview, setLogoPreview] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleLogoUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFormData({ ...formData, logo: file });
      
      // Criar preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setLogoPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = () => {
    // TODO: chamar API - salvar configurações de branding
    if (onSave) {
      onSave(formData);
    }
  };

  const handleColorChange = (type: 'primary' | 'secondary', value: string) => {
    setFormData({
      ...formData,
      [type === 'primary' ? 'primaryColor' : 'secondaryColor']: value
    });
  };

  const handleContactChange = (field: keyof BrandingData['contact'], value: string) => {
    setFormData({
      ...formData,
      contact: {
        ...formData.contact,
        [field]: value
      }
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Branding & Identidade Visual</h1>
        <p className="text-gray-600">Personalize a aparência e identidade da sua plataforma</p>
      </div>

      {/* Logo Upload */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Image className="w-5 h-5 mr-2" />
            Logo da Empresa
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Logo Preview */}
            {(logoPreview || formData.logo) && (
              <div className="flex items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg">
                <img
                  src={logoPreview || (typeof formData.logo === 'string' ? formData.logo : '')}
                  alt="Logo preview"
                  className="max-h-32 max-w-full object-contain"
                />
              </div>
            )}

            {/* Upload Area */}
            <div className="flex items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors">
              <div className="text-center">
                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-600 mb-2">
                  Clique para fazer upload ou arraste o arquivo
                </p>
                <p className="text-xs text-gray-500">
                  PNG, JPG até 5MB
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  className="mt-2"
                  onClick={() => fileInputRef.current?.click()}
                >
                  Selecionar Arquivo
                </Button>
              </div>
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleLogoUpload}
              className="hidden"
            />
          </div>
        </CardContent>
      </Card>

      {/* Color Scheme */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Palette className="w-5 h-5 mr-2" />
            Cores da Marca
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Primary Color */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cor Primária
              </label>
              <div className="flex items-center space-x-3">
                <input
                  type="color"
                  value={formData.primaryColor}
                  onChange={(e) => handleColorChange('primary', e.target.value)}
                  className="w-12 h-12 rounded border border-gray-300 cursor-pointer"
                />
                <Input
                  type="text"
                  value={formData.primaryColor}
                  onChange={(e) => handleColorChange('primary', e.target.value)}
                  placeholder="#3B82F6"
                />
              </div>
            </div>

            {/* Secondary Color */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cor Secundária
              </label>
              <div className="flex items-center space-x-3">
                <input
                  type="color"
                  value={formData.secondaryColor}
                  onChange={(e) => handleColorChange('secondary', e.target.value)}
                  className="w-12 h-12 rounded border border-gray-300 cursor-pointer"
                />
                <Input
                  type="text"
                  value={formData.secondaryColor}
                  onChange={(e) => handleColorChange('secondary', e.target.value)}
                  placeholder="#F59E0B"
                />
              </div>
            </div>
          </div>

          {/* Color Preview */}
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Preview das Cores</h4>
            <div className="flex space-x-4">
              <div className="flex items-center space-x-2">
                <div 
                  className="w-6 h-6 rounded border border-gray-300"
                  style={{ backgroundColor: formData.primaryColor }}
                />
                <span className="text-sm text-gray-600">Primária</span>
              </div>
              <div className="flex items-center space-x-2">
                <div 
                  className="w-6 h-6 rounded border border-gray-300"
                  style={{ backgroundColor: formData.secondaryColor }}
                />
                <span className="text-sm text-gray-600">Secundária</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Orchestrator Name */}
      <Card>
        <CardHeader>
          <CardTitle>Nome do Orquestrador</CardTitle>
        </CardHeader>
        <CardContent>
          <div>
            <label htmlFor="orchestratorName" className="block text-sm font-medium text-gray-700 mb-2">
              Nome do Agente Orquestrador
            </label>
            <Input
              id="orchestratorName"
              type="text"
              value={formData.orchestratorName}
              onChange={(e) => setFormData({ ...formData, orchestratorName: e.target.value })}
              placeholder="Agente Orquestrador"
            />
            <p className="text-xs text-gray-500 mt-1">
              Este nome aparecerá na interface do chat
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Contact Information */}
      <Card>
        <CardHeader>
          <CardTitle>Informações de Contato</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                Telefone
              </label>
              <div className="relative">
                <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="phone"
                  type="tel"
                  value={formData.contact.phone}
                  onChange={(e) => handleContactChange('phone', e.target.value)}
                  className="pl-10"
                  placeholder="(11) 99999-9999"
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                E-mail de Contato
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="email"
                  type="email"
                  value={formData.contact.email}
                  onChange={(e) => handleContactChange('email', e.target.value)}
                  className="pl-10"
                  placeholder="contato@empresa.com"
                />
              </div>
            </div>

            <div>
              <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-2">
                Endereço
              </label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="address"
                  type="text"
                  value={formData.contact.address}
                  onChange={(e) => handleContactChange('address', e.target.value)}
                  className="pl-10"
                  placeholder="Rua Exemplo, 123 - São Paulo, SP"
                />
              </div>
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