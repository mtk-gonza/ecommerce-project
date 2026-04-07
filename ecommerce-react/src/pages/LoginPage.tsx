import { useState, type FormEvent, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/common/Button';
import type { LoginCredentials } from '@/types/user';
import styles from '@/styles/pages/LoginPage.module.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);
  
  const { login, isLoggingIn, loginError } = useAuth();
  const navigate = useNavigate();

  // ✅ Sincronizar loginError con localError
  useEffect(() => {
    if (loginError) {
      console.log('🔍 [LoginPage] loginError detectado:', loginError.message);
      const message = loginError.message;
      
      let errorMessage = 'Ocurrió un error al iniciar sesión.';
      
      if (message?.includes('401') || message?.includes('Unauthorized')) {
        errorMessage = 'Email o contraseña incorrectos. Por favor verificá tus credenciales.';
      } else if (message?.includes('403')) {
        errorMessage = 'Tu cuenta está desactivada. Contactá a soporte.';
      } else if (message?.includes('500')) {
        errorMessage = 'Error del servidor. Por favor intentá de nuevo más tarde.';
      } else if (message?.includes('Network Error') || message?.includes('Failed to fetch')) {
        errorMessage = 'No se pudo conectar con el servidor. Verificá tu conexión.';
      }
      
      setLocalError(errorMessage);
    }
  }, [loginError]);

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
    if (localError) {
      setLocalError(null);
    }
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    if (localError) {
      setLocalError(null);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setLocalError(null);
    
    if (!email || !password) {
      console.warn('⚠️ [LoginPage] Email o password vacíos');
      setLocalError('Por favor completá todos los campos.');
      return;
    }
    
    try {
      const credentials: LoginCredentials = { email, password };
      await login(credentials);
      navigate('/dashboard', { replace: true });
      
    } catch (error: any) {
      if (!loginError) {
        setLocalError('Ocurrió un error al iniciar sesión. Por favor intentá de nuevo.');
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>Mi E-commerce</h1>
          <p className={styles.subtitle}>Iniciá sesión para continuar</p>
        </div>
        
        {/* ✅ Usar localError en lugar de loginError */}
        {localError && (
          <div className={styles.error} role="alert" aria-live="assertive">
            <span className={styles.errorIcon}>⚠️</span>
            <span>{localError}</span>
          </div>
        )}
        
        <form 
          onSubmit={handleSubmit}
          className={styles.form}
          noValidate
        >
          <div className={styles.field}>
            <label htmlFor="email" className={styles.label}>
              Email <span className={styles.required}>*</span>
            </label>
            <input
              id="email"
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={handleEmailChange}
              required
              disabled={isLoggingIn}
              className={styles.input}
              autoComplete="email"
              aria-invalid={!!localError}
            />
          </div>
          
          <div className={styles.field}>
            <label htmlFor="password" className={styles.label}>
              Contraseña <span className={styles.required}>*</span>
            </label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={handlePasswordChange}
              required
              disabled={isLoggingIn}
              className={styles.input}
              autoComplete="current-password"
              aria-invalid={!!localError}
            />
          </div>
          
          <Button 
            type="submit" 
            variant="primary" 
            fullWidth 
            isLoading={isLoggingIn}
            disabled={isLoggingIn || !email || !password}
          >
            {isLoggingIn ? 'Iniciando sesión...' : 'Iniciar Sesión'}
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