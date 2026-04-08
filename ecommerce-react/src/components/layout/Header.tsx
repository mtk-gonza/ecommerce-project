// src/components/layout/Header.tsx
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { ThemeToggle } from '@/components/common/ThemeToggle';
import styles from '@/styles/layout/Header.module.css';

export function Header() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
    setIsMobileMenuOpen(false);
  };

  const navLinks = [
    { href: '/', label: 'Inicio' },
    { href: '/products', label: 'Productos' },
  ];

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        {/* Logo */}
        <Link to="/" className={styles.logo}>
          <span className={styles.logoIcon}>🛒</span>
          <span className={styles.logoText}>Mi E-commerce</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className={styles.desktopNav}>
          {navLinks.map((link) => (
            <Link key={link.href} to={link.href} className={styles.navLink}>
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Desktop Actions */}
        <div className={styles.desktopActions}>
          <ThemeToggle />
          
          {isAuthenticated ? (
            <div className={styles.userMenu}>
              <span className={styles.userName}>{user?.name}</span>
              <button onClick={handleLogout} className={styles.logoutButton} type="button">
                Cerrar Sesión
              </button>
            </div>
          ) : (
            <div className={styles.authButtons}>
              <Link to="/login" className={styles.loginButton}>Iniciar Sesión</Link>
              <Link to="/register" className={styles.registerButton}>Registrarse</Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          className={styles.mobileMenuButton}
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label={isMobileMenuOpen ? 'Cerrar menú' : 'Abrir menú'}
          type="button"
        >
          <span className={styles.hamburger}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className={styles.mobileMenu}>
          <nav className={styles.mobileNav}>
            {navLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className={styles.mobileNavLink}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </nav>
          
          <div className={styles.mobileActions}>
            <ThemeToggle />
            
            {isAuthenticated ? (
              <>
                <div className={styles.mobileUserName}>{user?.name}</div>
                <button onClick={handleLogout} className={styles.mobileLogoutButton} type="button">
                  Cerrar Sesión
                </button>
              </>
            ) : (
              <div className={styles.mobileAuthButtons}>
                <Link to="/login" className={styles.mobileLoginButton} onClick={() => setIsMobileMenuOpen(false)}>
                  Iniciar Sesión
                </Link>
                <Link to="/register" className={styles.mobileRegisterButton} onClick={() => setIsMobileMenuOpen(false)}>
                  Registrarse
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}