export const env = {
  get API_URL(): string {
    return (
      window.APP_CONFIG?.API_URL || 'http://localhost:3050'
    );
  },

  get API_V1_PREFIX(): string {
    return (
      window.APP_CONFIG?.API_V1_PREFIX || '/api/v1'
    );
  },
  
  get MERCADOPAGO_PUBLIC_KEY(): string {
    return (
      window.APP_CONFIG?.MERCADOPAGO_PUBLIC_KEY || 'TEST-4cdb5ed3-c72e-42ce-ad1c-babb27f7fb8c' 
    );
  },
  
  get APP_VERSION(): string {
    return (
      window.APP_CONFIG?.APP_VERSION || '1.0.0'
    );
  },
  
  get ENVIRONMENT(): string {
    return (
      window.APP_CONFIG?.ENVIRONMENT || 'development'
    );
  },
  
  get IS_PROD(): boolean {
    return this.ENVIRONMENT === 'production';
  },
  
  get IS_DEV(): boolean {
    return this.ENVIRONMENT === 'development';
  },
} as const;

export type Env = typeof env;