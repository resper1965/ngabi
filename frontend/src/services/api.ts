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

export function fetchTenants(): Promise<Tenant[]> {
  // TODO: GET /tenants
  return axios.get<Tenant[]>('/tenants').then(res => res.data);
}

export function fetchUsers(): Promise<User[]> {
  // TODO: GET /users
  return axios.get<User[]>('/users').then(res => res.data);
}

export function fetchSettings(tenantId: string): Promise<Settings> {
  // TODO: GET /settings?tenant_id=
  return axios.get<Settings>(`/settings?tenant_id=${tenantId}`).then(res => res.data);
}

export function updateSettings(data: Settings): Promise<void> {
  // TODO: PUT /settings
  return axios.put('/settings', data).then(() => {});
}

export function sendChat(req: ChatRequest): Promise<ChatResponse> {
  // TODO: POST /chat
  return axios.post<ChatResponse>('/chat', req).then(res => res.data);
} 