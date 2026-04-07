import styles from '@/styles/common/Loader.module.css';

export interface LoaderProps {
  size?: 'small' | 'medium' | 'large';
  color?: 'primary' | 'white' | 'inherit';
  label?: string;
  fullScreen?: boolean;
}

export function Loader({
  size = 'medium',
  color = 'primary',
  label = 'Cargando...',
  fullScreen = false,
}: LoaderProps) {
  return (
    <div className={`${styles.wrapper} ${fullScreen ? styles.fullScreen : ''}`}>
      <div
        className={`${styles.spinner} ${styles[size]} ${styles[color]}`}
        role="status"
        aria-label={label}
      />
      {label && !fullScreen && (
        <span className="sr-only">{label}</span>
      )}
    </div>
  );
}