import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from datetime import datetime

# Inicializa a aplicação FastAPI
app = FastAPI()

# Caminho para o arquivo de previsões
FORECAST_FILE = os.path.join("data", "forecast", "best_model_forecast.csv")

# Verifica se o arquivo existe antes de carregar
if not os.path.exists(FORECAST_FILE):
    raise FileNotFoundError(f"Forecast file not found: {FORECAST_FILE}")

# Carrega as previsões
forecast_df = pd.read_csv(FORECAST_FILE, parse_dates=["date"])

@app.get("/")
def home():
    return {"message": "BRL/EUR Exchange Rate Prediction API is running!"}

@app.get("/predict/{date}")
def predict(date: str):
    """
    Retorna a previsão do câmbio para uma data específica.
    Exemplo de uso: /predict/2025-03-10
    """
    try:
        # Converte a string de data para formato datetime
        date_obj = pd.to_datetime(date)

        # Procura a data na previsão
        if date_obj in forecast_df["date"].values:
            predicted_value = forecast_df.loc[forecast_df["date"] == date_obj, "forecast"].values[0]
            return {
                "date": date_obj.strftime("%Y-%m-%d"),
                "predicted_exchange_rate": predicted_value
            }
        else:
            raise HTTPException(status_code=404, detail="Prediction for this date is not available. Try a closer date.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")
