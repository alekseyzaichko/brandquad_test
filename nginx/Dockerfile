# Stage 1 - build frontend app
FROM node:10-alpine as build-deps

WORKDIR /app/

COPY frontend/package.json .
RUN npm i

COPY frontend /app/
RUN npm run build

# Stage 2 - nginx & frontend dist
FROM nginx:alpine

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-deps /app/dist/ /dist/

CMD ["nginx", "-g", "daemon off;"]
