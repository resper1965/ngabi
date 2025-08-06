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
  Smartphone,
  LogOut
} from 'lucide-react';

/**
 * WIREFRAME TEXTUAL:
 * 
 * ┌─────────────────────────────────────────────────────────┐
 * │ [🍔] [LOGO] Chat Multi-Agent    [👤 Nome] [⚙️]        │ ← Topbar
 * ├─────────────────────────────────────────────────────────┤
 * │                                                         │
 * │ [💬] Chat                    │                         │
 * │ [🏢] Tenants                 │                         │
 * │ [👥] Usuários               │                         │
 * │ [🎨] Branding               │                         │
 * │ [⚙️] Configurações          │                         │
 * │                                                         │
 * │ ← Sidebar (recolhível)     │     Área Principal       │
 * │                             │                         │
 * │                             │                         │
 * │                             │                         │
 * │                             │                         │
 * └─────────────────────────────────────────────────────────┘
 */

interface SidebarItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  href: string;
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
    href: '/chat'
  },
  {
    id: 'evolution',
    label: 'WhatsApp',
    icon: <Smartphone className="w-5 h-5" />,
    href: '/evolution'
  },
  {
    id: 'tenants',
    label: 'Tenants',
    icon: <Building2 className="w-5 h-5" />,
    href: '/tenants'
  },
  {
    id: 'users',
    label: 'Usuários',
    icon: <Users className="w-5 h-5" />,
    href: '/users'
  },
  {
    id: 'branding',
    label: 'Branding',
    icon: <Palette className="w-5 h-5" />,
    href: '/branding'
  },
  {
    id: 'settings',
    label: 'Configurações',
    icon: <Settings className="w-5 h-5" />,
    href: '/settings'
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
  const { user, signOut } = useAuth();
  
  const displayName = userName || user?.email || user?.user_metadata?.full_name || 'Usuário';

  return (
    <div className="h-screen flex bg-gray-900">
      {/* Sidebar */}
      <div className={`bg-gray-800 border-r border-gray-700 transition-all duration-300 ${
        sidebarCollapsed ? 'w-16' : 'w-64'
      }`}>
        <div className="flex flex-col h-full">
          {/* Logo/Brand */}
          <div className="p-4 border-b border-gray-700">
            {sidebarCollapsed ? (
              <div className="flex justify-center">
                <div className="w-8 h-8 bg-[#00ade8] rounded flex items-center justify-center">
                  <span className="text-white text-sm font-bold">C</span>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-[#00ade8] rounded flex items-center justify-center">
                  <span className="text-white text-sm font-bold">C</span>
                </div>
                <span className="font-semibold text-white">Chat Multi-Agent</span>
              </div>
            )}
          </div>

          {/* Navigation Items */}
          <nav className="flex-1 p-4 space-y-2">
            {sidebarItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onNavigate(item.href)}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md transition-colors ${
                  currentPage === item.id
                    ? 'bg-[#00ade8] text-white'
                    : 'text-gray-200 hover:bg-gray-700 hover:text-white'
                }`}
              >
                {item.icon}
                {!sidebarCollapsed && (
                  <span className="text-sm font-medium">{item.label}</span>
                )}
              </button>
            ))}
          </nav>

          {/* Collapse Toggle */}
          <div className="p-4 border-t border-gray-700">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="w-full"
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

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Topbar */}
        <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* Mobile Menu Button */}
              <Button variant="ghost" size="sm" className="md:hidden">
                <Menu className="w-5 h-5" />
              </Button>

              {/* TODO: carregar logo do tenant via API */}
              {tenantLogo ? (
                <img src={tenantLogo} alt="Logo" className="h-8 w-auto" />
              ) : (
                              <div className="h-8 w-8 bg-gray-600 rounded flex items-center justify-center">
                <span className="text-gray-300 text-sm font-bold">T</span>
                </div>
              )}

              {/* TODO: carregar nome do orquestrador via API */}
              <div className="hidden md:block">
                <span className="text-sm text-gray-300">Orquestrador:</span>
                <span className="ml-2 font-medium text-white">{orchestratorName}</span>
              </div>
            </div>

            {/* User Info and Logout */}
            <div className="flex items-center space-x-3">
              <span className="text-sm text-gray-300 hidden md:block">{displayName}</span>
              <NotificationCenter />
              <ModeToggle />
              <Button
                variant="ghost"
                size="sm"
                onClick={signOut}
                className="flex items-center space-x-2 text-gray-300 hover:text-red-400"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden md:block">Sair</span>
              </Button>
              <Button variant="ghost" size="sm">
                <User className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
} 