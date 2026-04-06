import { useState, type FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/common/Button';
import type { RegisterData } from '@/types/user';
import styles from './../styles/pages/RegisterPage.module.css';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      // TODO: Integrar con useAuth().register() cuando lo implementes
      const RegisterData = { name, email, password };
      console.log('Registro:', RegisterData);
      
      // Simular delay de API
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Redirigir a login después de registrar
      navigate('/login', { 
        state: { message: '¡Registro exitoso! Ahora podés iniciar sesión.' }
      });
    } catch (err) {
      setError('Ocurrió un error. Por favor intentá de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>Crear Cuenta</h1>
          <p className={styles.subtitle}>Registrate para empezar a comprar</p>
        </div>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="name" className={styles.label}>Nombre</label>
            <input
              id="name"
              type="text"
              placeholder="Tu nombre"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              disabled={isLoading}
              className={styles.input}
              autoComplete="name"
            />
          </div>
          
          <div className={styles.field}>
            <label htmlFor="email" className={styles.label}>Email</label>
            <input
              id="email"
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
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
              minLength={6}
              disabled={isLoading}
              className={styles.input}
              autoComplete="new-password"
            />
          </div>
          
          <Button 
            type="submit" 
            variant="primary" 
            fullWidth 
            isLoading={isLoading}
          >
            Registrarse
          </Button>
        </form>
        
        <div className={styles.footer}>
          <p>
            ¿Ya tenés cuenta?{' '}
            <Link to="/login" className={styles.link}>
              Iniciá sesión acá
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}