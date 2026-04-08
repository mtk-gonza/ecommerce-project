import { Routes, Route, Navigate } from 'react-router-dom';
import { Header } from '@/components/layout/Header';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { HomePage } from '@/pages/HomePage';
import { LoginPage } from '@/pages/LoginPage';
import { RegisterPage } from '@/pages/RegisterPage';
import { DashboardPage } from '@/pages/DashboardPage';

export function App() {
  return (
    <div className="app">
      <Header />
      <main>
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
          
          <Route path="/products" element={
            <ProtectedRoute roles={['customer', 'admin']}>
              <div>Productos (por implementar)</div>
            </ProtectedRoute>
          } />
          
          <Route path="/profile" element={
            <ProtectedRoute roles={['customer', 'admin']}>
              <div>Perfil de Usuario (por implementar)</div>
            </ProtectedRoute>
          } />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}