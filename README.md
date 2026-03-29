# Proyecto ECOMMERCE

## PASO 1  
Clonar repositorio:
```bash
git clone https://github.com/mtk-gonza/ecommerce-project.git
```

## PASO 2  
Renombrar y colocar las variables de entorno:
```bash
cp .env.example .env
nano .env
```

## PASO 3  
Crear las imágenes de Docker:
```bash
docker compose build
```

## PASO 4  
En Portainer, copiar el siguiente contenido. 
Agregar las variables de entorno que están en el archivo `.env`, o bien adjuntar directamente el archivo.
```yaml
services:
  ecommerce-fastapi:
    image: ecommerce-project-ecommerce-fastapi:latest
    container_name: ecommerce-fastapi
    environment:
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=${DB_NAME}
      - CORS_ALLOW_ORIGINS=${CORS_ALLOW_ORIGINS}
      - DEBUG=${DEBUG}
    ports:
      - ${API_PORT}:3050
    restart: always

  ecommerce-react:
    image: ecommerce-project-ecommerce-react:latest
    container_name: ecommerce-react
    environment:
      - API_URL=${API_URL}
    ports:
      - ${WEB_PORT}:80
    depends_on:
      - ecommerce-fastapi
    restart: always
```

### Opción alternativa para crear el stack

En el directorio raíz se encuentra el archivo `stack-compose.yml`. Podés copiar el contenido y crear el stack directamente:

```bash
cat stack-compose.yml
```