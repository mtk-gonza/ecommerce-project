import { useState, type FormEvent, useEffect, type ChangeEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { getErrorMessage } from '@/api/client';
import type { LoginCredentials } from '@/types/user';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { Alert } from '@/components/common/Alert';
import styles from '@/styles/pages/LoginPage.module.css';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  
  const { login, isLoggingIn, loginError } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (loginError) {
      const message = getErrorMessage(loginError);
      let errorMessage = 'Ocurrió un error al iniciar sesión.';
      
      if (message?.includes('401') || message?.includes('Unauthorized')) {
        errorMessage = 'Email o contraseña incorrectos.';
      } else if (message?.includes('Network Error')) {
        errorMessage = 'No se pudo conectar con el servidor.';
      }
      
      setLocalError(errorMessage);
    }
  }, [loginError]);

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
    if (localError) setLocalError(null);
  };

  const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    if (localError) setLocalError(null);
  };

  const handleBlur = (e: ChangeEvent<HTMLInputElement>) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    
    if (!email.trim() || !password) {
      setLocalError('Por favor completá todos los campos.');
      return;
    }
    
    try {
      const credentials : LoginCredentials = { email, password }
      await login(credentials);
      navigate('/dashboard', { replace: true });
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>Mi E-commerce</h1>
          <p className={styles.subtitle}>Iniciá sesión para continuar</p>
        </div>
        
        {localError && (
          <Alert variant="error" dismissible onDismiss={() => setLocalError(null)}>
            {localError}
          </Alert>
        )}
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="email" className={styles.label}>Email *</label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={handleEmailChange}
              onBlur={handleBlur}
              required
              disabled={isLoggingIn}
              autoComplete="email"
            />
          </div>
          
          <div className={styles.field}>
            <label htmlFor="password" className={styles.label}>Contraseña *</label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={handlePasswordChange}
              onBlur={handleBlur}
              required
              disabled={isLoggingIn}
              autoComplete="current-password"
            />
          </div>
          
          <Button 
            type="submit" 
            variant="primary" 
            fullWidth 
            isLoading={isLoggingIn}
            disabled={isLoggingIn || !email.trim() || !password}
          >
            {isLoggingIn ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </Button>
        </form>
        
        <div className={styles.footer}>
          <p>
            ¿No tenés cuenta?{' '}
            <Link to="/register" className={styles.link}>Registrate acá</Link>
          </p>
        </div>
      </div>
    </div>
  );
}