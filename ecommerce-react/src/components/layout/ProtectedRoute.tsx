import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore.ts';

interface ProtectedRouteProps {
  children: React.ReactNode;
  roles?: string[];
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  roles = [] 
}) => {
  const { isAuthenticated, user } = useAuthStore();
  const location = useLocation();

  if (!isAuthenticated || !user) {
    // Redirigir a login guardando la ubicación original
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Validar roles si se especificaron
  if (roles.length > 0 && !roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};