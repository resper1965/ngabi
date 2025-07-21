import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Edit, Trash2, Search, Building2 } from 'lucide-react';
import { fetchTenants, Tenant } from '@/services/api';

/**
 * WIREFRAME TEXTUAL:
 * 
 * ┌─────────────────────────────────────────────────────────┐
 * │ Gestão de Tenants                    [🔍] [Novo Tenant] │
 * ├─────────────────────────────────────────────────────────┤
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ Nome          │ Subdomínio    │ Ações               │ │
 * │ ├─────────────────────────────────────────────────────┤ │
 * │ │ Empresa A     │ empresa-a     │ [✏️] [🗑️]          │ │
 * │ │ Empresa B     │ empresa-b     │ [✏️] [🗑️]          │ │
 * │ │ Startup C     │ startup-c     │ [✏️] [🗑️]          │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ ← Tabela de tenants com ações                          │
 * │                                                         │
 * └─────────────────────────────────────────────────────────┘
 * 
 * MODAL:
 * ┌─────────────────────────────────────┐
 * │ Novo Tenant                         │
 * ├─────────────────────────────────────┤
 * │ Nome: [________________]            │
 * │ Subdomínio: [____________]          │
 * │                                     │
 * │ [Cancelar] [Salvar]                │
 * └─────────────────────────────────────┘
 */

interface Tenant {
  id: string;
  name: string;
  subdomain: string;
  createdAt: Date;
  status: 'active' | 'inactive';
}

interface TenantFormData {
  name: string;
  subdomain: string;
}

interface TenantsPageProps {
  onCreateTenant?: (data: TenantFormData) => void;
  onUpdateTenant?: (id: string, data: TenantFormData) => void;
  onDeleteTenant?: (id: string) => void;
  isLoading?: boolean;
  tenants?: Tenant[];
}

export function TenantsPage({
  tenants: _tenants = [],
  onCreateTenant,
  onUpdateTenant,
  onDeleteTenant
}: TenantsPageProps) {
  const [showModal, setShowModal] = useState(false);
  const [editingTenant, setEditingTenant] = useState<Tenant | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState<TenantFormData>({
    name: '',
    subdomain: ''
  });
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchTenants().then(data => {
      setTenants(data);
    }).finally(() => setLoading(false));
  }, []);

  const filteredTenants = tenants.filter(tenant =>
    tenant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tenant.subdomain.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleOpenModal = (tenant?: Tenant) => {
    if (tenant) {
      setEditingTenant(tenant);
      setFormData({ name: tenant.name, subdomain: tenant.subdomain });
    } else {
      setEditingTenant(null);
      setFormData({ name: '', subdomain: '' });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingTenant(null);
    setFormData({ name: '', subdomain: '' });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (editingTenant && onUpdateTenant) {
      // TODO: chamar API - atualizar tenant
      onUpdateTenant(editingTenant.id, formData);
    } else if (onCreateTenant) {
      // TODO: chamar API - criar tenant
      onCreateTenant(formData);
    }
    
    handleCloseModal();
  };

  const handleDelete = (id: string) => {
    if (confirm('Tem certeza que deseja excluir este tenant?')) {
      // TODO: chamar API - excluir tenant
      onDeleteTenant?.(id);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestão de Tenants</h1>
          <p className="text-gray-600">Gerencie os tenants da plataforma</p>
        </div>
        <Button onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          Novo Tenant
        </Button>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center space-x-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Buscar tenants..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tenants Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Building2 className="w-5 h-5 mr-2" />
            Tenants ({filteredTenants.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Nome</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Subdomínio</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Criado em</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredTenants.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="text-center py-8 text-gray-500">
                      {searchTerm ? 'Nenhum tenant encontrado' : 'Nenhum tenant cadastrado'}
                    </td>
                  </tr>
                ) : (
                  filteredTenants.map((tenant) => (
                    <tr key={tenant.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div className="flex items-center">
                          <div className="w-8 h-8 bg-blue-100 rounded flex items-center justify-center mr-3">
                            <Building2 className="w-4 h-4 text-blue-600" />
                          </div>
                          <span className="font-medium text-gray-900">{tenant.name}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-600">
                        {tenant.subdomain}.seudominio.com
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          tenant.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {tenant.status === 'active' ? 'Ativo' : 'Inativo'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600">
                        {tenant.createdAt.toLocaleDateString('pt-BR')}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleOpenModal(tenant)}
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(tenant.id)}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {editingTenant ? 'Editar Tenant' : 'Novo Tenant'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                  Nome
                </label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Nome da empresa"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="subdomain" className="block text-sm font-medium text-gray-700 mb-1">
                  Subdomínio
                </label>
                <Input
                  id="subdomain"
                  type="text"
                  value={formData.subdomain}
                  onChange={(e) => setFormData({ ...formData, subdomain: e.target.value })}
                  placeholder="empresa"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  Será acessível em: {formData.subdomain}.seudominio.com
                </p>
              </div>
              
              <div className="flex justify-end space-x-2 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleCloseModal}
                >
                  Cancelar
                </Button>
                <Button type="submit">
                  {editingTenant ? 'Atualizar' : 'Criar'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 