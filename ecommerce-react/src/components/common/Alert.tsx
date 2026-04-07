import type { HTMLAttributes, ReactNode } from 'react';
import styles from '@/styles/common/Alert.module.css';

export type AlertVariant = 'info' | 'success' | 'warning' | 'error';

export interface AlertProps extends Omit<HTMLAttributes<HTMLDivElement>, 'title'> {
  variant?: AlertVariant;
  title?: string;
  children: ReactNode;
  dismissible?: boolean;
  onDismiss?: () => void;
  icon?: ReactNode;
}

export function Alert({
  variant = 'info',
  title,
  children,
  dismissible = false,
  onDismiss,
  icon,
  className = '',
  ...props
}: AlertProps) {
  return (
    <div 
      className={`${styles.alert} ${styles[variant]} ${className}`} 
      role="alert"
      {...props}
    >
      <div className={styles.content}>
        {icon && <span className={styles.icon}>{icon}</span>}
        <div className={styles.text}>
          {title && <strong className={styles.title}>{title}</strong>}
          <span className={styles.message}>{children}</span>
        </div>
      </div>
      
      {dismissible && (
        <button
          className={styles.dismiss}
          onClick={onDismiss}
          aria-label="Cerrar"
          type="button"
        >
          ×
        </button>
      )}
    </div>
  );
}