import { useState, type FormEvent, type ChangeEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { getErrorMessage } from '@/api/client';
import type { RegisterData } from '@/types/user';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { Container } from '@/components/common/Container';
import { Alert } from '@/components/common/Alert';
import { Form } from '@/components/common/Form';
import { Label } from '@/components/common/Label';
import { FormSpan } from '@/components/common/FormSpan';

import styles from '@/styles/pages/RegisterPage.module.css';

export default function RegisterPage() {
  const [formData, setFormData] = useState<RegisterData>({
    email: '', password: '', name: '', phone: '',
  });
  const [localError, setLocalError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  
  const { register, isRegistering } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (localError) setLocalError(null);
    if (successMessage) setSuccessMessage(null);
  };

  const handleBlur = (e: ChangeEvent<HTMLInputElement>) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const getFieldError = (fieldName: string): string | null => {
    if (!touched[fieldName]) return null;
    const { email, password, name } = formData;
    
    switch (fieldName) {
      case 'name':
        if (!name.trim()) return 'El nombre es obligatorio';
        if (name.trim().length < 2) return 'Mínimo 2 caracteres';
        break;
      case 'email':
        if (!email.trim()) return 'El email es obligatorio';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Email inválido';
        break;
      case 'password':
        if (!password) return 'La contraseña es obligatoria';
        if (password.length < 8) return 'Mínimo 8 caracteres';
        break;
    }
    return null;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    // Validaciones básicas
    if (!formData.name.trim() || !formData.email.trim() || !formData.password) {
      setLocalError('Por favor completá los campos obligatorios');
      return;
    }
    if (!acceptedTerms) {
      setLocalError('Debes aceptar los términos y condiciones');
      return;
    }
    
    setLocalError(null);
    setSuccessMessage(null);
    
    try {
      await register(formData);
      setSuccessMessage('¡Registro exitoso! Redirigiendo al login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (error) {
      setLocalError(getErrorMessage(error));
    }
  };

  return (
    <Container variant="narrow" className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>Crear Cuenta</h1>
          <p className={styles.subtitle}>Registrate para empezar a comprar</p>
        </div>
        
        {successMessage && (
          <Alert variant="success">{successMessage}</Alert>
        )}
        
        {localError && !successMessage && (
          <Alert variant="error" dismissible onDismiss={() => setLocalError(null)}>
            {localError}
          </Alert>
        )}
        
        {/* ✅ Form component literal */}
        <Form onSubmit={handleSubmit}>
          
          {/* Nombre */}
          <div className={styles.field}>
            <Label htmlFor="name" required>Nombre</Label>
            <Input
              id="name"
              name="name"
              type="text"
              placeholder="Tu nombre completo"
              value={formData.name}
              onChange={handleChange}
              onBlur={handleBlur}
              required
              disabled={isRegistering || !!successMessage}
              error={getFieldError('name') || undefined}
              autoComplete="name"
            />
            {getFieldError('name') && (
              <FormSpan variant="error">{getFieldError('name')}</FormSpan>
            )}
          </div>
          
          {/* Email */}
          <div className={styles.field}>
            <Label htmlFor="email" required>Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="tu@email.com"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              required
              disabled={isRegistering || !!successMessage}
              error={getFieldError('email') || undefined}
              autoComplete="email"
            />
            {getFieldError('email') && (
              <FormSpan variant="error">{getFieldError('email')}</FormSpan>
            )}
          </div>
          
          {/* Contraseña */}
          <div className={styles.field}>
            <Label htmlFor="password" required>Contraseña</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="Mínimo 8 caracteres"
              value={formData.password}
              onChange={handleChange}
              onBlur={handleBlur}
              required
              minLength={8}
              disabled={isRegistering || !!successMessage}
              error={getFieldError('password') || undefined}
              autoComplete="new-password"
            />
            {getFieldError('password') && (
              <FormSpan variant="error">{getFieldError('password')}</FormSpan>
            )}
          </div>
          
          {/* Teléfono (opcional) */}
          <div className={styles.field}>
            <Label htmlFor="phone" optional>Teléfono</Label>
            <Input
              id="phone"
              name="phone"
              type="tel"
              placeholder="+54 9 11 1234-5678"
              value={formData.phone}
              onChange={handleChange}
              disabled={isRegistering || !!successMessage}
              autoComplete="tel"
            />
          </div>
          
          {/* Términos */}
          <div className={styles.terms}>
            <input
              id="terms"
              type="checkbox"
              checked={acceptedTerms}
              onChange={(e) => setAcceptedTerms(e.target.checked)}
              disabled={isRegistering || !!successMessage}
            />
            <Label htmlFor="terms" className={styles.termsLabel}>
              Acepto los{' '}
              <a href="/terms" target="_blank" rel="noopener noreferrer">
                términos y condiciones
              </a>
            </Label>
          </div>
          
          {/* Botón */}
          <Button 
            type="submit" 
            variant="primary" 
            fullWidth 
            isLoading={isRegistering}
            disabled={isRegistering || !!successMessage || !acceptedTerms}
          >
            {isRegistering ? 'Registrando...' : 'Crear Cuenta'}
          </Button>
        </Form>
        
        <div className={styles.footer}>
          <p>
            ¿Ya tenés cuenta?{' '}
            <Link to="/login" className={styles.link}>
              Iniciá sesión acá
            </Link>
          </p>
        </div>
      </div>
    </Container>
  );
}