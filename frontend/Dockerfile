# Stage 1: build Vite app
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# Nếu bạn có biến môi trường VITE_* thì thêm tại build args/env
RUN npm run build

# Stage 2: serve bằng Nginx
FROM nginx:1.27-alpine AS serve
# Copy build sang Nginx html
COPY --from=build /app/dist /usr/share/nginx/html
# Mặc định Nginx sẽ phục vụ trên :80
EXPOSE 80
# Không sửa nginx.conf ở đây; ta dùng gateway reverse proxy riêng
