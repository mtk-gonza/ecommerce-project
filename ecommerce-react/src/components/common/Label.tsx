import type { LabelHTMLAttributes, ReactNode } from 'react';
import styles from '@/styles/common/Label.module.css';

export interface LabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean;
  optional?: boolean;
  children: ReactNode;
}

export function Label({
  required,
  optional,
  className = '',
  children,
  ...props
}: LabelProps) {
  return (
    <label className={`${styles.label} ${className}`} {...props}>
      {children}
      {required && <span className={styles.required}>*</span>}
      {optional && <span className={styles.optional}>(opcional)</span>}
    </label>
  );
}