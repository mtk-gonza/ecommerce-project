// ✅ Validación en runtime (opcional pero recomendado)
const getEnv = (key: string, defaultValue?: string): string => {
  const value = import.meta.env[key];
  if (value === undefined && defaultValue === undefined) {
    console.warn(`⚠️ Variable de entorno ${key} no definida`);
  }
  return value ?? defaultValue ?? '';
};

export const env = {
  // API Backend
  API_URL: getEnv('VITE_API_URL', 'http://localhost:3050/api/v1'),
  
  // MercadoPago
  MERCADOPAGO_PUBLIC_KEY: getEnv('VITE_MERCADOPAGO_PUBLIC_KEY', ''),
  
  // App
  APP_NAME: 'Mi E-commerce',
  APP_VERSION: '1.0.0',
  
  // Flags
  IS_DEV: import.meta.env.DEV,
  IS_PROD: import.meta.env.PROD,
} as const;

// ✅ Tipo exportado para usar en otros archivos
export type Env = typeof env;