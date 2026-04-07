export interface AppConfig {
  API_URL: string;
  API_V1_PREFIX: string;
  MERCADOPAGO_PUBLIC_KEY?: string;
  APP_VERSION?: string;
  ENVIRONMENT?: 'development' | 'staging' | 'production';
  [key: string]: string | undefined;
}

declare global {
  interface Window {
    APP_CONFIG?: AppConfig;
  }
}

export {};