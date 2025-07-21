import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { ChatPage } from './pages/ChatPage'
import { TenantsPage } from './pages/TenantsPage'
import { UsersPage } from './pages/UsersPage'
import { BrandingPage } from './pages/BrandingPage'
import { SettingsPage } from './pages/SettingsPage'
import './App.css'

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: Date;
}

interface KnowledgeBase {
  id: string;
  name: string;
  selected: boolean;
}

// Componente para rotas protegidas
function ProtectedRoute({ children, isAuthenticated }: { children: React.ReactNode; isAuthenticated: boolean }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
}

// Componente para o layout do Dashboard com rotas aninhadas
function DashboardLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Dados mockados para demonstração
  const mockKnowledgeBases: KnowledgeBase[] = [
    { id: '1', name: 'Base de Conhecimento Geral', selected: true },
    { id: '2', name: 'Documentação Técnica', selected: false },
    { id: '3', name: 'FAQ', selected: true }
  ];

  const handleSendMessage = (message: string, mode: string, selectedKBs: string[]) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content: message,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Simular resposta do agente
    setTimeout(() => {
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Entendi sua mensagem: "${message}". Estou processando no modo ${mode} com ${selectedKBs.length} bases de conhecimento selecionadas. Como posso ajudá-lo?`,
        sender: 'agent',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, agentMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const handleNavigate = (page: string) => {
    navigate(page);
  };

  // Determinar a página atual baseada na rota
  const getCurrentPage = () => {
    const path = location.pathname;
    if (path === '/' || path === '/chat') return 'chat';
    if (path === '/tenants') return 'tenants';
    if (path === '/users') return 'users';
    if (path === '/branding') return 'branding';
    if (path === '/settings') return 'settings';
    return 'chat';
  };

  return (
    <Dashboard
      currentPage={getCurrentPage()}
      onNavigate={handleNavigate}
      tenantLogo=""
      orchestratorName="n.Gabi"
      userName="Admin"
    >
      <Routes>
        <Route path="/" element={
          <ChatPage
            agentName="n.Gabi"
            onSendMessage={handleSendMessage}
            messages={messages}
            knowledgeBases={mockKnowledgeBases}
            isLoading={isLoading}
          />
        } />
        <Route path="/chat" element={
          <ChatPage
            agentName="n.Gabi"
            onSendMessage={handleSendMessage}
            messages={messages}
            knowledgeBases={mockKnowledgeBases}
            isLoading={isLoading}
          />
        } />
        <Route path="/tenants" element={<TenantsPage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/branding" element={<BrandingPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Dashboard>
  );
}

function App() {
  // Iniciar como autenticado para permitir acesso direto
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  const handleLogin = (email: string, password: string) => {
    // TODO: Implementar autenticação real
    console.log('Login:', { email, password });
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={
            isAuthenticated ? (
              <Navigate to="/" replace />
            ) : (
              <Login onLogin={handleLogin} />
            )
          } 
        />
        <Route 
          path="/*" 
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <DashboardLayout />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App
