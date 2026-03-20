FROM node:20-slim
WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install lucide-vue-next vue @tailwindcss/postcss tailwindcss postcss autoprefixer vue-router@4

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]