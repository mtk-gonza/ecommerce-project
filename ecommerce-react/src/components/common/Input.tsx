import { forwardRef } from 'react';
import type { InputHTMLAttributes } from 'react';
import styles from '@/styles/common/Input.module.css';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  label?: string;
  helperText?: string;
  fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      error,
      label,
      helperText,
      fullWidth = false,
      className = '',
      id,
      disabled,
      ...props
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    return (
      <div className={`${styles.wrapper} ${fullWidth ? styles.fullWidth : ''}`}>
        {label && (
          <label htmlFor={inputId} className={styles.label}>
            {label}
            {props.required && <span className={styles.required}>*</span>}
          </label>
        )}
        
        <input
          ref={ref}
          id={inputId}
          className={`${styles.input} ${error ? styles.error : ''} ${className}`}
          disabled={disabled}
          aria-invalid={!!error}
          aria-describedby={helperText ? helperId : undefined}
          data-error-id={error ? errorId : undefined}
          {...props}
        />
      </div>
    );
  }
);

Input.displayName = 'Input';