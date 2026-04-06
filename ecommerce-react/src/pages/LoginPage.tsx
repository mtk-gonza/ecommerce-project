import { useState, type FormEvent } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/common/Button';
import type { LoginCredentials } from '@/types/user';
import styles from './../styles/pages/LoginPage.module.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const { login, isLoggingIn, loginError } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  const from = (location.state as { from?: Location })?.from?.pathname;
  const redirectTo = from && from !== '/' ? from : '/dashboard';

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const credentials: LoginCredentials = { email, password };
      await login(credentials);
      navigate(redirectTo, { replace: true });
    } catch (error) {
      console.error('❌ [LoginPage] Login failed:', error);
      console.error('❌ [LoginPage] loginError =', loginError);
    }
  };

  const getErrorMessage = () => {
    if (!loginError) return null;
    
    const status = loginError.message;
    
    // ✅ Mensajes específicos según el error
    if (status?.includes('401')) {
      return 'Email o contraseña incorrectos. Por favor verificá tus credenciales.';
    }
    if (status?.includes('403')) {
      return 'Tu cuenta está desactivada. Contactá a soporte.';
    }
    if (status?.includes('500')) {
      return 'Error del servidor. Por favor intentá de nuevo más tarde.';
    }
    if (status?.includes('Network Error') || status?.includes('Failed to fetch')) {
      return 'No se pudo conectar con el servidor. Verificá tu conexión.';
    }
    
    // ✅ Mensaje por defecto
    return 'Ocurrió un error al iniciar sesión. Por favor intentá de nuevo.';
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>Mi E-commerce</h1>
          <p className={styles.subtitle}>Iniciá sesión para continuar</p>
        </div>
        
        {getErrorMessage() && (
          <div className={styles.error} role="alert">
            <span className={styles.errorIcon}>⚠️</span>
            {getErrorMessage()}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="email" className={styles.label}>Email</label>
            <input
              id="email"
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoggingIn}
              className={styles.input}
              autoComplete="email"
            />
          </div>
          
          <div className={styles.field}>
            <label htmlFor="password" className={styles.label}>Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoggingIn}
              className={styles.input}
              autoComplete="current-password"
            />
          </div>
          
          <Button 
            type="submit" 
            variant="primary" 
            fullWidth 
            isLoading={isLoggingIn}
          >
            Iniciar Sesión
          </Button>
        </form>
        
        <div className={styles.footer}>
          <p>
            ¿No tenés cuenta?{' '}
            <Link to="/register" className={styles.link}>
              Registrate acá
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}