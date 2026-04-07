import type { HTMLAttributes, ReactNode } from 'react';
import styles from '@/styles/common/Container.module.css';

export type ContainerVariant = 'default' | 'fluid' | 'narrow';

type ContainerAsType = 'div' | 'section' | 'main' | 'article' | 'aside' | 'nav' | 'header' | 'footer';

export interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
  variant?: ContainerVariant;
  as?: ContainerAsType;
  children: ReactNode;
}

export function Container({
  variant = 'default',
  as: Component = 'div',
  className = '',
  children,
  ...props
}: ContainerProps) {
  const containerClasses = [
    styles.container,
    styles[variant],
    className,
  ].filter(Boolean).join(' ');

  return (
    <Component 
      className={containerClasses} 
      {...props}
    >
      {children}
    </Component>
  );
}