import { Container } from '@/components/common/Container';
import { Button } from '@/components/common/Button';

export function HomePage() {
  return (
    <Container>
      <h1>🚀 Mi E-commerce</h1>
      <p>Bienvenido a la tienda</p>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
        <Button variant="primary" onClick={() => window.location.href = '/login'}>
          Iniciar Sesión
        </Button>
        <Button variant="secondary" onClick={() => window.location.href = '/register'}>
          Registrarse
        </Button>
      </div>
    </Container>
  );
}