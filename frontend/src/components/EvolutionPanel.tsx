import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Instance {
  instance: {
    instanceName: string;
    status: string;
    qrcode?: string;
  };
}

interface EvolutionPanelProps {
  apiBaseUrl: string;
}

const EvolutionPanel: React.FC<EvolutionPanelProps> = ({ apiBaseUrl }) => {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [newInstanceName, setNewInstanceName] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedInstance, setSelectedInstance] = useState<string>('');
  const [qrCode, setQrCode] = useState<string>('');
  const [message, setMessage] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  // Carregar instâncias
  const loadInstances = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${apiBaseUrl}/api/v1/evolution/instances`);
      setInstances(response.data as Instance[]);
    } catch (error) {
      console.error('Erro ao carregar instâncias:', error);
    } finally {
      setLoading(false);
    }
  };

  // Criar nova instância
  const createInstance = async () => {
    if (!newInstanceName.trim()) return;
    
    try {
      setLoading(true);
      await axios.post(`${apiBaseUrl}/api/v1/evolution/instance/create`, {
        instanceName: newInstanceName
      });
      setNewInstanceName('');
      await loadInstances();
    } catch (error) {
      console.error('Erro ao criar instância:', error);
    } finally {
      setLoading(false);
    }
  };

  // Gerar QR Code
  const generateQRCode = async (instanceName: string) => {
    try {
      setLoading(true);
      const response = await axios.get(`${apiBaseUrl}/api/v1/evolution/instance/${instanceName}/qr`);
      setQrCode((response.data as any).qrcode);
      setSelectedInstance(instanceName);
    } catch (error) {
      console.error('Erro ao gerar QR code:', error);
    } finally {
      setLoading(false);
    }
  };

  // Enviar mensagem
  const sendMessage = async () => {
    if (!selectedInstance || !phoneNumber || !message.trim()) return;
    
    try {
      setLoading(true);
      await axios.post(`${apiBaseUrl}/api/v1/evolution/instance/${selectedInstance}/send`, {
        number: phoneNumber,
        text: message
      });
      setMessage('');
      alert('Mensagem enviada com sucesso!');
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      alert('Erro ao enviar mensagem');
    } finally {
      setLoading(false);
    }
  };

  // Deletar instância
  const deleteInstance = async (instanceName: string) => {
    if (!confirm(`Tem certeza que deseja deletar a instância ${instanceName}?`)) return;
    
    try {
      setLoading(true);
      await axios.delete(`${apiBaseUrl}/api/v1/evolution/instance/${instanceName}`);
      await loadInstances();
    } catch (error) {
      console.error('Erro ao deletar instância:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInstances();
  }, []);

  return (
    <div className="evolution-panel p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">📱 Evolution API - WhatsApp</h2>
      
      {/* Criar Nova Instância */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-blue-800">Criar Nova Instância</h3>
        <div className="flex gap-2">
          <input
            type="text"
            value={newInstanceName}
            onChange={(e) => setNewInstanceName(e.target.value)}
            placeholder="Nome da instância (ex: ngabi-whatsapp)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={createInstance}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Criando...' : 'Criar'}
          </button>
        </div>
      </div>

      {/* Lista de Instâncias */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3 text-gray-800">Instâncias WhatsApp</h3>
        <div className="space-y-3">
          {instances.map((instance) => (
            <div key={instance.instance.instanceName} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold">{instance.instance.instanceName}</h4>
                  <p className="text-sm text-gray-600">Status: {instance.instance.status}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => generateQRCode(instance.instance.instanceName)}
                    className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                  >
                    QR Code
                  </button>
                  <button
                    onClick={() => deleteInstance(instance.instance.instanceName)}
                    className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
                  >
                    Deletar
                  </button>
                </div>
              </div>
            </div>
          ))}
          {instances.length === 0 && (
            <p className="text-gray-500 text-center py-4">Nenhuma instância criada</p>
          )}
        </div>
      </div>

      {/* QR Code Modal */}
      {qrCode && (
        <div className="mb-6 p-4 bg-green-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-green-800">QR Code - {selectedInstance}</h3>
          <div className="text-center">
            <img src={qrCode} alt="QR Code" className="mx-auto mb-3" />
            <p className="text-sm text-gray-600">
              Escaneie este QR code no WhatsApp para conectar a instância
            </p>
            <button
              onClick={() => setQrCode('')}
              className="mt-2 px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700"
            >
              Fechar
            </button>
          </div>
        </div>
      )}

      {/* Enviar Mensagem */}
      <div className="p-4 bg-purple-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-purple-800">Enviar Mensagem</h3>
        <div className="space-y-3">
          <select
            value={selectedInstance}
            onChange={(e) => setSelectedInstance(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">Selecione uma instância</option>
            {instances.map((instance) => (
              <option key={instance.instance.instanceName} value={instance.instance.instanceName}>
                {instance.instance.instanceName}
              </option>
            ))}
          </select>
          
          <input
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="Número (ex: 5511999999999)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Digite sua mensagem..."
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          
          <button
            onClick={sendMessage}
            disabled={loading || !selectedInstance || !phoneNumber || !message.trim()}
            className="w-full px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
          >
            {loading ? 'Enviando...' : 'Enviar Mensagem'}
          </button>
        </div>
      </div>

      {/* Status da API */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-gray-800">Status da API</h3>
        <button
          onClick={loadInstances}
          disabled={loading}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
        >
          {loading ? 'Atualizando...' : 'Atualizar Status'}
        </button>
      </div>
    </div>
  );
};

export default EvolutionPanel; 