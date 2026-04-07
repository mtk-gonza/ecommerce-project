import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios';
import type { AxiosInstance } from 'axios';
import { env } from '@/config/env';

// 📋 Tipos
/**
 * Estructura de error de la API (coincide con FastAPI HTTPException)
 */
export interface ApiError {
  detail: string | { msg: string }[];
  error?: string;
  error_type?: string;
}

// 🔧 Configuración
const API_CONFIG = {
  baseURL: env.API_URL + env.API_V1_PREFIX,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
} as const;

// 🚀 Instancia de Axios
export const api: AxiosInstance = axios.create(API_CONFIG);

// 🔐 Interceptor de Request (Agrega token JWT)
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


// ⚠️ Interceptor de Response (Maneja errores globalmente)
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    const status = error.response?.status;
    const hasToken = !!localStorage.getItem('access_token');
    // Manejo por código de estado
    switch (status) {
      case 401:
        if (hasToken) {
          console.warn('⚠️ [API] Sesión expirada, redirigiendo a login');
          clearAuthStorage();
          window.location.href = '/login';
        }
        break;
        
      case 403:
        console.warn('⚠️ [API] Acceso denegado (403)');
        break;
        
      case 404:
        console.warn('⚠️ [API] Recurso no encontrado (404)');
        break;
        
      case 500:
        console.error('❌ [API] Error interno del servidor (500)');
        break;
        
      case 503:
        console.error('❌ [API] Servicio no disponible (503)');
        break;
        
      default:
        console.error(`❌ [API] Error ${status || 'desconocido'}`);
    }
    return Promise.reject(error);
  }
);


// 🧹 Funciones Auxiliares
function clearAuthStorage(): void {
  localStorage.removeItem('access_token');
  localStorage.removeItem('auth-storage');
}
/**
 * Obtiene el mensaje de error amigable desde una respuesta de API
 * @param error - Error de Axios
 * @returns Mensaje de error legible para el usuario
 */
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError<ApiError>(error)) {
    const detail = error.response?.data?.detail;
    if (Array.isArray(detail)) {
      return detail[0]?.msg || 'Error de validación';
    }
    if (typeof detail === 'string') {
      return detail;
    }
    return error.message || 'Ocurrió un error inesperado';
  }
  return error instanceof Error ? error.message : 'Ocurrió un error inesperado';
}

export type { AxiosInstance, AxiosError };
export { axios };