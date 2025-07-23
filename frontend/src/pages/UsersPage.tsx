import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Edit, Trash2, Search, Users, Shield, Mail } from 'lucide-react';
import { fetchUsers } from '@/services/api';

/**
 * WIREFRAME TEXTUAL:
 * 
 * ┌─────────────────────────────────────────────────────────┐
 * │ Gestão de Usuários                 [��] [Novo Usuário]  │
 * ├─────────────────────────────────────────────────────────┤
 * │                                                         │
 * │ ┌─────────────────────────────────────────────────────┐ │
 * │ │ E-mail        │ Role         │ Status    │ Ações    │ │
 * │ ├─────────────────────────────────────────────────────┤ │
 * │ │ user@emp.com  │ Admin        │ Ativo     │ [✏️][🗑️] │ │
 * │ │ dev@emp.com   │ Developer    │ Ativo     │ [✏️][🗑️] │ │
 * │ │ test@emp.com  │ User         │ Inativo   │ [✏️][🗑️] │ │
 * │ └─────────────────────────────────────────────────────┘ │
 * │                                                         │
 * │ ← Tabela de usuários com ações                         │
 * │                                                         │
 * └─────────────────────────────────────────────────────────┘
 * 
 * MODAL:
 * ┌─────────────────────────────────────┐
 * │ Novo Usuário                        │
 * ├─────────────────────────────────────┤
 * │ E-mail: [________________]          │
 * │ Role: [Admin ▼]                     │
 * │ Senha: [____________] (opcional)    │
 * │                                     │
 * │ [Cancelar] [Salvar]                │
 * └─────────────────────────────────────┘
 */

interface User {
  id: string;
  email: string;
  role: 'admin' | 'developer' | 'user';
  status: 'active' | 'inactive';
  createdAt: Date;
  lastLogin?: Date;
}

interface UserFormData {
  email: string;
  role: 'admin' | 'developer' | 'user';
  password?: string;
}

interface UsersPageProps {
  onCreateUser?: (data: UserFormData) => void;
  onUpdateUser?: (id: string, data: UserFormData) => void;
  onDeleteUser?: (id: string) => void;
  isLoading?: boolean;
  users?: User[];
}

const roleLabels = {
  admin: 'Administrador',
  developer: 'Desenvolvedor',
  user: 'Usuário'
};

const roleColors = {
  admin: 'bg-red-100 text-red-800',
  developer: 'bg-blue-100 text-blue-800',
  user: 'bg-gray-100 text-gray-800'
};

export function UsersPage({
  users: _users = [],
  onCreateUser,
  onUpdateUser,
  onDeleteUser
}: UsersPageProps) {
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState<UserFormData>({
    email: '',
    role: 'user',
    password: ''
  });
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchUsers().then(data => {
      setUsers(data as unknown as User[]);
    }).finally(() => setLoading(false));
  }, []);

  const filteredUsers = users.filter(user =>
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    roleLabels[user.role].toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleOpenModal = (user?: User) => {
    if (user) {
      setEditingUser(user);
      setFormData({ email: user.email, role: user.role });
    } else {
      setEditingUser(null);
      setFormData({ email: '', role: 'user', password: '' });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingUser(null);
    setFormData({ email: '', role: 'user', password: '' });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (editingUser && onUpdateUser) {
      // TODO: chamar API - atualizar usuário
      onUpdateUser(editingUser.id, formData);
    } else if (onCreateUser) {
      // TODO: chamar API - criar usuário
      onCreateUser(formData);
    }
    
    handleCloseModal();
  };

  const handleDelete = (id: string) => {
    if (confirm('Tem certeza que deseja excluir este usuário?')) {
      // TODO: chamar API - excluir usuário
      onDeleteUser?.(id);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestão de Usuários</h1>
          <p className="text-gray-600">Gerencie os usuários da plataforma</p>
        </div>
        <Button onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          Novo Usuário
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
                placeholder="Buscar usuários..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="w-5 h-5 mr-2" />
            Usuários ({filteredUsers.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Usuário</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Role</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Criado em</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Último login</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Ações</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={6} className="text-center py-8 text-gray-500">
                      Carregando usuários...
                    </td>
                  </tr>
                ) : filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="text-center py-8 text-gray-500">
                      {searchTerm ? 'Nenhum usuário encontrado' : 'Nenhum usuário cadastrado'}
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((user) => (
                    <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div className="flex items-center">
                          <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center mr-3">
                            <Mail className="w-4 h-4 text-gray-600" />
                          </div>
                          <div>
                            <span className="font-medium text-gray-900">{user.email}</span>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${roleColors[user.role]}`}>
                          <Shield className="w-3 h-3 mr-1" />
                          {roleLabels[user.role]}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          user.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {user.status === 'active' ? 'Ativo' : 'Inativo'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600">
                        {user.createdAt.toLocaleDateString('pt-BR')}
                      </td>
                      <td className="py-3 px-4 text-gray-600">
                        {user.lastLogin 
                          ? user.lastLogin.toLocaleDateString('pt-BR')
                          : 'Nunca'
                        }
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleOpenModal(user)}
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(user.id)}
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
              {editingUser ? 'Editar Usuário' : 'Novo Usuário'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  E-mail
                </label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="usuario@empresa.com"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">
                  Role
                </label>
                <select
                  id="role"
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value as any })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="user">Usuário</option>
                  <option value="developer">Desenvolvedor</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
              
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                  Senha {!editingUser && '(opcional)'}
                </label>
                <Input
                  id="password"
                  type="password"
                  value={formData.password || ''}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  placeholder={editingUser ? 'Deixe em branco para manter' : '••••••••'}
                  required={!editingUser}
                />
                {editingUser && (
                  <p className="text-xs text-gray-500 mt-1">
                    Deixe em branco para manter a senha atual
                  </p>
                )}
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
                  {editingUser ? 'Atualizar' : 'Criar'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 