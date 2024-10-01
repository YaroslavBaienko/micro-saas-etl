# app/main.py

from fastapi import FastAPI, UploadFile, File, Depends
import pandas as pd
from sqlalchemy import create_engine
import os

app = FastAPI()

# Настройка подключения к базе данных
DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
engine = create_engine(DATABASE_URL)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Чтение CSV файла
    df = pd.read_csv(file.file)
    # Обработка данных (пока пропустим этот шаг)
    # Сохранение данных в базу данных
    df.to_sql('data_table', con=engine, if_exists='append', index=False)
    return {"status": "success", "filename": file.filename}
