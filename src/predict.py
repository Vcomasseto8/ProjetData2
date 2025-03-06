import os
import pandas as pd
from fastapi import FastAPI
from forecast import Forecasting

# Inicializa o FastAPI
app = FastAPI()

# Carrega o modelo e gera previsões
forecaster = Forecasting()
forecaster.best_model_forecast()

# Carrega os dados de previsão salvos
FORECAST_FILE = os.path.join("data", "forecast", "best_model_forecast.csv")
forecast_df = pd.read_csv(FORECAST_FILE, parse_dates=["date"])

@app.get("/")
def home():
    return {"message": "BRL/EUR Exchange Rate Prediction API is running!"}

@app.get("/predict/{date}")
def predict(date: str):
    """Retorna a previsão do câmbio para uma data específica"""
    date = pd.to_datetime(date)

    if date in forecast_df["date"].values:
        predicted_value = forecast_df.loc[forecast_df["date"] == date, "forecast"].values[0]
        return {"date": date.strftime("%Y-%m-%d"), "predicted_exchange_rate": predicted_value}
    else:
        return {"error": "Prediction for this date is not available. Try a date closer to the forecast range."}
