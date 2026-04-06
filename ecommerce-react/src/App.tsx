import { Routes, Route, Navigate } from 'react-router-dom';
import { Button } from '@/components/common/Button';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import DashboardPage from '@/pages/DashboardPage';


function HomePage() {
  return (
    <div className="container" style={{ padding: '2rem', textAlign: 'center' }}>
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
    </div>
  );
}

function App() {
  return (
    <Routes>
      {/* Rutas públicas */}
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      {/* Rutas protegidas */}
      <Route path="/dashboard" element={
        <ProtectedRoute roles={['customer', 'admin']}>
          <DashboardPage />
        </ProtectedRoute>
      } />
      
      <Route path="/profile" element={
        <ProtectedRoute roles={['customer', 'admin']}>
          <div>Perfil de Usuario (por implementar)</div>
        </ProtectedRoute>
      } />
      
      <Route path="/products" element={
        <ProtectedRoute roles={['customer', 'admin']}>
          <div>Productos (por implementar)</div>
        </ProtectedRoute>
      } />
      
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;