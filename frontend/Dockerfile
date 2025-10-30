FROM node:18-alpine

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install

# Копирование кода
COPY . .

# Экспозиция порта
EXPOSE 3000

# Запуск приложения
CMD ["npm", "start"]