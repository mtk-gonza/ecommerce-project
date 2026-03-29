# --- BUILD STAGE ---
FROM node:20-alpine AS build

WORKDIR /ecommerce-react

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# --- SERVE STAGE ---
FROM nginx:stable-alpine

RUN apk add --no-cache bash

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /ecommerce-react/dist /usr/share/nginx/html

# Copiamos SOLO el template (no el config.js de desarrollo)
COPY public/config.template.js /usr/share/nginx/html/config.template.js

EXPOSE 80

CMD ["/bin/sh", "-c", "envsubst '$API_URL' < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js && nginx -g 'daemon off;'"]