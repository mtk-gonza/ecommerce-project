ecommerce-react/
├── public/
│   └── favicon.ico
│
├── src/
│   ├── 📁 api/                   # Llamadas a API (por dominio)
│   │   ├── client.ts             # Axios instance + interceptors
│   │   ├── auth.ts               # /auth/login, /auth/register, /auth/me
│   │   ├── products.ts           # /products, /products/:slug
│   │   ├── cart.ts               # /cart/*
│   │   └── orders.ts             # /orders/*
│   │
│   ├── 📁 components/            # Componentes UI reutilizables
│   │   ├── 📁 common/            # Button, Input, Loader, Modal, Alert
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.module.css
│   │   │   │   └── index.ts
│   │   │   ├── Input/
│   │   │   └── Loader/
│   │   │
│   │   └── 📁 layout/            # Header, Footer, Container, ProtectedRoute
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── ProtectedRoute.tsx
│   │
│   ├── 📁 config/                # Configuración de la app
│   │   ├── env.ts                # Variables de entorno tipadas
│   │   └── queryClient.ts        # React Query config
│   │
│   ├── 📁 hooks/                 # Custom hooks globales
│   │   ├── useAuth.ts            # Login, register, logout
│   │   ├── useCart.ts            # Carrito (Zustand wrapper)
│   │   └── useProducts.ts        # Productos (React Query wrapper)
│   │
│   ├── 📁 pages/                 # Páginas = Rutas
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── ProductsPage.tsx
│   │   ├── ProductDetailPage.tsx
│   │   ├── CartPage.tsx
│   │   ├── CheckoutPage.tsx
│   │   ├── OrderSuccessPage.tsx
│   │   ├── ProfilePage.tsx
│   │   └── OrdersPage.tsx
│   │
│   ├── 📁 store/                 # Estado global (Zustand)
│   │   ├── authStore.ts
│   │   ├── cartStore.ts
│   │   └── index.ts
│   │
│   ├── 📁 styles/                # CSS global (sin Tailwind)
│   │   ├── variables.css
│   │   ├── reset.css
│   │   ├── globals.css
│   │   └── mixins.css
│   │
│   ├── 📁 types/                 # Tipos TypeScript (mapean backend)
│   │   ├── user.ts
│   │   ├── product.ts
│   │   ├── cart.ts
│   │   ├── order.ts
│   │   └── index.ts
│   │
│   ├── 📁 utils/                 # Funciones puras reutilizables
│   │   ├── formatCurrency.ts
│   │   ├── formatDate.ts
│   │   ├── validators.ts
│   │   └── constants.ts
│   │
│   ├── App.tsx                   # Routing principal
│   ├── main.tsx                  # Entry point
│   └── index.css                 # Importa styles/globals.css
│
├── .env
├── .env.example
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md