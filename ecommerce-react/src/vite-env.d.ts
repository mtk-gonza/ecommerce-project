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