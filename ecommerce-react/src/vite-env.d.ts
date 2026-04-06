// ✅ CSS Modules - Permite importar *.module.css con tipos
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

// ✅ Assets - Imágenes y otros archivos estáticos
declare module '*.svg' {
  const content: string;
  export default content;
}

declare module '*.png' {
  const content: string;
  export default content;
}

declare module '*.jpg' {
  const content: string;
  export default content;
}

declare module '*.jpeg' {
  const content: string;
  export default content;
}

declare module '*.gif' {
  const content: string;
  export default content;
}

declare module '*.webp' {
  const content: string;
  export default content;
}

// ✅ Variables de entorno tipadas para import.meta.env
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_MERCADOPAGO_PUBLIC_KEY: string;
  // Agregar más según necesites
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}