from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load forecast data
forecast_df = pd.read_csv("data/forecast/best_model_forecast.csv")
forecast_df["date"] = pd.to_datetime(forecast_df["date"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exchange Rate Prediction API"}

@app.get("/predict/{date}")
def get_prediction(date: str):
    selected_date = pd.to_datetime(date)
    if selected_date in forecast_df["date"].values:
        predicted_value = forecast_df.loc[forecast_df["date"] == selected_date, "forecast"].values[0]
        return {"date": date, "predicted_exchange_rate": predicted_value}
    return {"error": "No prediction available for this date"}
