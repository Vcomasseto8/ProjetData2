from fastapi import FastAPI, HTTPException
import os
import pandas as pd

app = FastAPI()

FORECAST_FILE = os.path.join("data", "forecast", "best_model_forecast.csv")

@app.get("/")
def home():
    return {"message": "BRL/EUR Exchange Rate Prediction API is running!"}

@app.get("/predict/{date}")
def predict(date: str):
    """Returns exchange rate prediction for a given date."""
    try:
        date_obj = pd.to_datetime(date)

        if not os.path.exists(FORECAST_FILE):
            raise HTTPException(status_code=500, detail="Forecast file not found on the server.")

        forecast_df = pd.read_csv(FORECAST_FILE, parse_dates=["date"])
        forecast_df["date"] = pd.to_datetime(forecast_df["date"])

        if date_obj in forecast_df["date"].values:
            predicted_value = forecast_df.loc[forecast_df["date"] == date_obj, "forecast"].values[0]
            return {"date": date_obj.strftime("%Y-%m-%d"), "predicted_exchange_rate": predicted_value}
        else:
            raise HTTPException(status_code=404, detail="Prediction for this date is not available.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")
