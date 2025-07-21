import React from 'react';
import EvolutionPanel from '../components/EvolutionPanel';

const EvolutionPage: React.FC = () => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'https://api.ngabi.ness.tec.br';

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📱 WhatsApp Business API</h1>
          <p className="text-gray-600">
            Gerencie suas instâncias do WhatsApp e envie mensagens através da Evolution API
          </p>
        </div>
        
        <EvolutionPanel apiBaseUrl={apiBaseUrl} />
        
        <div className="mt-8 p-6 bg-blue-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-blue-800">ℹ️ Como usar</h3>
          <div className="space-y-2 text-sm text-blue-700">
            <p><strong>1.</strong> Crie uma nova instância do WhatsApp</p>
            <p><strong>2.</strong> Gere o QR Code e escaneie no seu WhatsApp</p>
            <p><strong>3.</strong> Aguarde a conexão ser estabelecida</p>
            <p><strong>4.</strong> Use a instância para enviar mensagens</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EvolutionPage; 