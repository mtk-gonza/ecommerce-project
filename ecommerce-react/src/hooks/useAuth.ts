import { useMutation, useQuery, type UseMutationResult } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/api/auth';
import type { LoginCredentials, RegisterData, User, LoginResponse } from '@/types/user';
import type { AxiosError } from 'axios';
import type { ApiError } from '@/api/client';

export const useAuth = () => {
  const { login, logout, user, isAuthenticated } = useAuthStore();

  // Query para obtener usuario actual
  const { data: currentUser, isLoading: isLoadingUser } = useQuery<User | null>({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const response = await authApi.me();
      return response.data;
    },
    enabled: isAuthenticated && !!localStorage.getItem('access_token'),
    retry: false,
    staleTime: 5 * 60 * 1000,
  });

  // Mutación para login
  const loginMutation: UseMutationResult<LoginResponse, Error, LoginCredentials> = 
    useMutation({
      mutationFn: async (credentials: LoginCredentials) => {
        const response = await authApi.login(credentials);
        return response.data;
      },
      onSuccess: (data) => {
        login(data.access_token, data.user);
      },
      // ✅ Capturar error para mostrar mensaje amigable
      onError: (error: AxiosError<ApiError>) => {
        console.error('Login error:', error);
        // El error ya está disponible en loginMutation.error
      },
    });

  // Mutación para registro
  const registerMutation = useMutation({
    mutationFn: async (data: RegisterData) => {
      const response = await authApi.register(data);
      return response.data;
    },
    onSuccess: (user) => {
      console.log('✅ [useAuth] Usuario registrado:', user.email);
      // No hacemos login automático, redirigimos a login para que confirmen email
    },
  });

  return {
    user: currentUser || user,
    isLoadingUser,
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    register: registerMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    registerError: registerMutation.error,
    logout,
    isAuthenticated,
  };
};