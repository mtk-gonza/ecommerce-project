import type { HTMLAttributes, ReactNode } from 'react';
import styles from '@/styles/common/FormSpan.module.css';

export interface FormSpanProps extends HTMLAttributes<HTMLSpanElement> {
  children: ReactNode;
  variant?: 'helper' | 'error';
  id?: string;
}

export function FormSpan({
  children,
  variant = 'helper',
  id,
  className = '',
  ...props
}: FormSpanProps) {
  if (!children) return null;
  
  const classes = `${styles.span} ${styles[variant]} ${className}`;
  
  return (
    <span 
      id={id} 
      className={classes} 
      role={variant === 'error' ? 'alert' : undefined}
      {...props}
    >
      {children}
    </span>
  );
}