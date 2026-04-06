import { Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/common/Button';
import styles from './../styles/pages/DashboardPage.module.css';

export default function DashboardPage() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>¡Bienvenido, {user?.name || 'Usuario'}! 🎉</h1>
          <p className={styles.subtitle}>
            Has iniciado sesión correctamente
          </p>
        </div>
        
        <div className={styles.info}>
          <div className={styles.infoItem}>
            <span className={styles.infoLabel}>Email:</span>
            <span className={styles.infoValue}>{user?.email}</span>
          </div>
          <div className={styles.infoItem}>
            <span className={styles.infoLabel}>Rol:</span>
            <span className={styles.infoValue}>
              {user?.role === 'admin' ? '👑 Administrador' : '👤 Cliente'}
            </span>
          </div>
        </div>
        
        <div className={styles.actions}>
          <Link to="/products">
            <Button variant="primary" fullWidth>
              🛒 Ver Productos
            </Button>
          </Link>
          
          <Link to="/profile">
            <Button variant="secondary" fullWidth>
              👤 Mi Perfil
            </Button>
          </Link>
          
          <Button variant="ghost" fullWidth onClick={handleLogout}>
            🚪 Cerrar Sesión
          </Button>
        </div>
      </div>
    </div>
  );
}