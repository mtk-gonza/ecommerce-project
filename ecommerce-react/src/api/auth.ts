import { api } from './client';
import type { LoginCredentials, RegisterData, User, LoginResponse } from '@/types/user';

export const authApi = {
  login: (credentials: LoginCredentials) =>
    api.post<LoginResponse>('/auth/login', credentials),

  register: (data: RegisterData) =>
    api.post<User>('/auth/register', data),

  me: () => api.get<User>('/auth/me'),
};