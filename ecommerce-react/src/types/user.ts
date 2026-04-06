export interface User {
  id: number;
  email: string;
  name: string;
  role: 'customer' | 'admin';
  phone?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  phone?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}