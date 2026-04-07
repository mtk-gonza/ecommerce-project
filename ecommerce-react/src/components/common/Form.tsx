import type { FormHTMLAttributes, ReactNode } from 'react';
import styles from '@/styles/common/Form.module.css';

export interface FormProps extends FormHTMLAttributes<HTMLFormElement> {
  error?: string;
  children: ReactNode;
}

export function Form({
  error,
  className = '',
  children,
  ...props
}: FormProps) {
  return (
    <form
      className={`${styles.form} ${error ? styles.formError : ''} ${className}`}
      {...props}
    >
      {children}
    </form>
  );
}