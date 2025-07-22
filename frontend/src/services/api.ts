import axios from 'axios';

// Tipos placeholders (substitua pelos reais do seu domínio)
export interface Tenant {
  id: string;
  name: string;
  subdomain: string;
  status: 'active' | 'inactive';
  createdAt: string;
}

export interface User {
  id: string;
  email: string;
  role: 'admin' | 'developer' | 'user';
  status: 'active' | 'inactive';
  createdAt: string;
  lastLogin?: string;
}

export interface Settings {
  // Defina os campos reais de Settings
  [key: string]: any;
}

export interface ChatRequest {
  message: string;
  mode: string;
  knowledgeBases: string[];
}

export interface ChatResponse {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: string;
}

export async function fetchTenants(): Promise<Tenant[]> {
  // TODO: GET /tenants
  const response = await axios.get<Tenant[]>('/tenants');
  return response.data;
}

export async function fetchUsers(): Promise<User[]> {
  // TODO: GET /users
  const response = await axios.get<User[]>('/users');
  return response.data;
}

export async function fetchSettings(tenantId: string): Promise<Settings> {
  // TODO: GET /settings?tenant_id=
  const response = await axios.get<Settings>(`/settings?tenant_id=${tenantId}`);
  return response.data;
}

export async function updateSettings(data: Settings): Promise<void> {
  // TODO: PUT /settings
  await axios.put('/settings', data);
}

export async function sendChat(req: ChatRequest): Promise<ChatResponse> {
  // TODO: POST /chat
  const response = await axios.post<ChatResponse>('/chat', req);
  return response.data;
} 