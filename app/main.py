# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from sqlalchemy import create_engine
import os
import requests
import json

app = FastAPI()

# Настройка подключения к базе данных
DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
engine = create_engine(DATABASE_URL)

# Функция для очистки данных
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Пример очистки данных: удаление пропущенных значений
    df = df.dropna()
    # Пример преобразования типов: преобразуем столбец 'lead_time' в целочисленный
    df['lead_time'] = df['lead_time'].astype(int)
    # Добавьте сюда другие шаги по очистке и обработке данных, если нужно
    return df

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Чтение CSV файла в DataFrame
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {e}")
    
    # Очистка данных
    df_clean = clean_data(df)

    # Преобразование DataFrame в JSON
    json_data = df_clean.to_json(orient='records')

    # Отправка данных на Go-сервис для обработки
    response = requests.post("http://go_service:8080/process", data=json_data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error processing data with Go service")

    # Сохранение данных в базу данных
    try:
        df_clean.to_sql('data_table', con=engine, if_exists='append', index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data to database: {e}")

    return {"status": "success", "filename": file.filename}
