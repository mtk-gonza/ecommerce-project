import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios';
import type { AxiosInstance } from 'axios';
import { env } from '@/config/env';

export interface ApiError {
  detail: string | { msg: string }[];
  error?: string;
}

export const api: AxiosInstance = axios.create({
  baseURL: env.API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

// Interceptor para agregar token JWT
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('auth-storage');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);