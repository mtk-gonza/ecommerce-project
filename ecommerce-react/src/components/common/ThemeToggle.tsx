// src/components/common/ThemeToggle.tsx
import { useEffect, useState } from 'react';
import styles from '@/styles/common/ThemeToggle.module.css';

export function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const isDarkMode = document.documentElement.classList.contains('dark');
    setIsDark(isDarkMode);
  }, []);

  const toggleTheme = () => {
    const newIsDark = !isDark;
    document.documentElement.classList.toggle('dark');
    setIsDark(newIsDark);
    localStorage.setItem('theme', newIsDark ? 'dark' : 'light');
  };

  return (
    <button
      onClick={toggleTheme}
      className={styles.toggle}
      aria-label={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
      type="button"
    >
      {isDark ? '🌞' : '🌙'}
    </button>
  );
}