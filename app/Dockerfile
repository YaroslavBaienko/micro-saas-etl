# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Устанавливаем переменные окружения для базы данных
ENV MYSQL_USER=etl_user
ENV MYSQL_PASSWORD=etl_password
ENV MYSQL_DATABASE=etl_database
ENV MYSQL_HOST=db

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
