import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { useAuth } from '../contexts/AuthContext';
import { ModeToggle } from '../components/mode-toggle';
import { NotificationCenter } from '../components/notification-center';
import { 
  MessageSquare, 
  Building2, 
  Users, 
  Palette, 
  Settings, 
  ChevronLeft, 
  ChevronRight,
  User,
  Menu,
  Bot,
  LogOut,
  Sparkles
} from 'lucide-react';

interface SidebarItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  href: string;
  description?: string;
}

interface DashboardProps {
  children: React.ReactNode;
  currentPage: string;
  onNavigate: (page: string) => void;
  tenantLogo?: string;
  orchestratorName?: string;
  userName?: string;
}

const sidebarItems: SidebarItem[] = [
  {
    id: 'chat',
    label: 'Chat',
    icon: <MessageSquare className="w-5 h-5" />,
    href: '/chat',
    description: 'Conversa com agentes IA'
  },
  {
    id: 'evolution',
    label: 'Evolution',
    icon: <Sparkles className="w-5 h-5" />,
    href: '/evolution',
    description: 'Evolução de agentes'
  },
  {
    id: 'tenants',
    label: 'Organizações',
    icon: <Building2 className="w-5 h-5" />,
    href: '/tenants',
    description: 'Gerenciar tenants'
  },
  {
    id: 'users',
    label: 'Usuários',
    icon: <Users className="w-5 h-5" />,
    href: '/users',
    description: 'Gerenciar usuários'
  },
  {
    id: 'branding',
    label: 'Branding',
    icon: <Palette className="w-5 h-5" />,
    href: '/branding',
    description: 'Personalização visual'
  },
  {
    id: 'settings',
    label: 'Configurações',
    icon: <Settings className="w-5 h-5" />,
    href: '/settings',
    description: 'Configurações do sistema'
  }
];

export function Dashboard({ 
  children, 
  currentPage, 
  onNavigate, 
  tenantLogo,
  orchestratorName = 'n.Gabi',
  userName
}: DashboardProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, signOut } = useAuth();
  
  const displayName = userName || user?.email || user?.user_metadata?.full_name || 'Usuário';

  return (
    <div className="h-screen flex bg-background">
      {/* Sidebar */}
      <div className={`bg-sidebar border-r border-sidebar-border transition-all duration-300 ${
        sidebarCollapsed ? 'w-16' : 'w-64'
      } ${mobileMenuOpen ? 'fixed inset-y-0 left-0 z-50 w-64' : 'hidden md:block'}`}>
        <div className="flex flex-col h-full">
          {/* Logo/Brand */}
          <div className="p-4 border-b border-sidebar-border">
            {sidebarCollapsed ? (
              <div className="flex justify-center">
                <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                  <Bot className="w-6 h-6 text-primary-foreground" />
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                  <Bot className="w-6 h-6 text-primary-foreground" />
                </div>
                <div>
                  <span className="font-bold text-sidebar-foreground text-lg">n.Gabi</span>
                  <p className="text-xs text-sidebar-accent-foreground">Chat Multi-Agent</p>
                </div>
              </div>
            )}
          </div>

          {/* Navigation Items */}
          <nav className="flex-1 p-4 space-y-2">
            {sidebarItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.href);
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  currentPage === item.id
                    ? 'bg-sidebar-primary text-sidebar-primary-foreground shadow-lg'
                    : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                }`}
                title={item.description}
              >
                {item.icon}
                {!sidebarCollapsed && (
                  <div className="flex-1 text-left">
                    <span className="text-sm font-medium">{item.label}</span>
                    {item.description && (
                      <p className="text-xs opacity-70 mt-0.5">{item.description}</p>
                    )}
                  </div>
                )}
              </button>
            ))}
          </nav>

          {/* User Info */}
          {!sidebarCollapsed && (
            <div className="p-4 border-t border-sidebar-border">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-sidebar-accent rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-sidebar-accent-foreground" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-sidebar-foreground truncate">{displayName}</p>
                  <p className="text-xs text-sidebar-accent-foreground truncate">{user?.email}</p>
                </div>
              </div>
            </div>
          )}

          {/* Collapse Toggle */}
          <div className="p-4 border-t border-sidebar-border">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="w-full text-sidebar-foreground hover:text-sidebar-accent-foreground"
              title={sidebarCollapsed ? "Expandir menu" : "Recolher menu"}
            >
              {sidebarCollapsed ? (
                <ChevronRight className="w-4 h-4" />
              ) : (
                <ChevronLeft className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Overlay */}
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Topbar */}
        <header className="bg-gray-800 border-b border-gray-700 px-4 md:px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* Mobile Menu Button */}
              <Button 
                variant="ghost" 
                size="sm" 
                className="md:hidden"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                title="Abrir menu"
              >
                <Menu className="w-5 h-5" />
              </Button>

              {/* Tenant Logo */}
              {tenantLogo ? (
                <img src={tenantLogo} alt="Logo da organização" className="h-8 w-auto" />
              ) : (
                <div className="h-8 w-8 bg-gray-600 rounded-lg flex items-center justify-center">
                  <Building2 className="w-4 h-4 text-gray-300" />
                </div>
              )}

              {/* Orchestrator Info */}
              <div className="hidden md:block">
                <span className="text-sm text-gray-300">Orquestrador:</span>
                <span className="ml-2 font-medium text-white">{orchestratorName}</span>
              </div>
            </div>

            {/* User Actions */}
            <div className="flex items-center space-x-2 md:space-x-3">
              <span className="text-sm text-gray-300 hidden md:block">{displayName}</span>
              <NotificationCenter />
              <ModeToggle />
              <Button
                variant="ghost"
                size="sm"
                onClick={signOut}
                className="flex items-center space-x-2 text-gray-300 hover:text-red-400 transition-colors"
                title="Sair da aplicação"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden md:block">Sair</span>
              </Button>
              <Button 
                variant="ghost" 
                size="sm"
                title="Perfil do usuário"
              >
                <User className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
} 