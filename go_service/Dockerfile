# go_service/Dockerfile

FROM golang:1.23.1

WORKDIR /app

# Копируем go.mod
COPY go.mod ./

# Загружаем зависимости
RUN go mod download

# Копируем исходный код
COPY . ./

# Собираем приложение
RUN go build -o main .

EXPOSE 8080

CMD ["./main"]
