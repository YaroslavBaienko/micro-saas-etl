from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd
import os
import requests

app = FastAPI()

# Настройка подключения к базе данных
DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@" \
               f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
engine = create_engine(DATABASE_URL)

# Функция для очистки данных
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df['lead_time'] = df['lead_time'].astype(int)
    # Добавьте дополнительные шаги очистки, если необходимо
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
    try:
        response = requests.post("http://go_service:8080/process", data=json_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error processing data with Go service: {e}")
    
    # Сохранение данных в базу данных
    try:
        df_clean.to_sql('data_table', con=engine, if_exists='append', index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data to database: {e}")
    
    return {"status": "success", "filename": file.filename}

# Эндпоинт: Общее количество бронирований
@app.get("/analytics/total_bookings")
def get_total_bookings():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) as total FROM data_table"))
            total = result.scalar()
        return {"total_bookings": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

# Эндпоинт: Количество отмененных бронирований
@app.get("/analytics/canceled_bookings")
def get_canceled_bookings():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) as total FROM data_table WHERE is_canceled = 1"))
            total = result.scalar()
        return {"canceled_bookings": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

# Эндпоинт: Среднее время ожидания перед бронированием
@app.get("/analytics/average_lead_time")
def get_average_lead_time():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT AVG(lead_time) as average_lead_time FROM data_table"))
            average_lead_time = result.scalar()
        return {"average_lead_time": average_lead_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

# Эндпоинт: Топ-5 стран по количеству бронирований
@app.get("/analytics/top_countries")
def get_top_countries():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT country, COUNT(*) as total
                FROM data_table
                GROUP BY country
                ORDER BY total DESC
                LIMIT 5
            """))
            keys = result.keys()
            countries = [dict(zip(keys, row)) for row in result]
        return {"top_countries": countries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

# Эндпоинт: Средняя стоимость бронирования по типу отеля
@app.get("/analytics/average_adr_by_hotel")
def get_average_adr_by_hotel():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT hotel, AVG(adr) as average_adr
                FROM data_table
                GROUP BY hotel
            """))
            keys = result.keys()
            adr_by_hotel = [dict(zip(keys, row)) for row in result]
        return {"average_adr_by_hotel": adr_by_hotel}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

# Эндпоинт: Процент отмененных бронирований
@app.get("/analytics/cancellation_rate")
def get_cancellation_rate():
    try:
        with engine.connect() as connection:
            total_result = connection.execute(text("SELECT COUNT(*) as total FROM data_table"))
            total = total_result.scalar()
            canceled_result = connection.execute(text("SELECT COUNT(*) as total FROM data_table WHERE is_canceled = 1"))
            canceled = canceled_result.scalar()
            cancellation_rate = (canceled / total) * 100 if total > 0 else 0
        return {"cancellation_rate": cancellation_rate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
