import os
import pandas as pd
from fastapi import FastAPI
from src.load_data import DataLoader
from src.preprocess import DataPreprocessor
from src.forecast import Forecasting
from src.eda import ExploratoryDataAnalysis

# Define directories
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Exchange Rate Forecasting API is running"}

@app.get("/run-pipeline")
def run_pipeline():
    """Triggers the data pipeline (load, preprocess, EDA, forecast) via API request."""
    
    print("\n=== Step 1: Loading Data ===")
    loader = DataLoader()
    loader.run()

    print("\n=== Step 2: Preprocessing Data ===")
    preprocessor = DataPreprocessor()
    preprocessor.run()

    print("\n=== Step 3: Exploratory Data Analysis ===")
    eda = ExploratoryDataAnalysis()
    eda.run()

    print("\n=== Step 4: Forecasting ===")
    forecaster = Forecasting()
    forecaster.best_model_forecast()

    forecast_file = os.path.join(DATA_DIR, "forecast", "best_model_forecast.csv")

    if os.path.exists(forecast_file):
        forecast_df = pd.read_csv(forecast_file, parse_dates=["date"])

        # Last actual value available (last row where 'actual' is not NaN)
        last_actual_value = forecast_df.dropna(subset=["actual"]).iloc[-1]

        # Select only future forecasts (where 'actual' is NaN)
        future_forecasts = forecast_df[forecast_df["actual"].isna()]

        print("\n=== Exchange Rate Predictions for the Next Days ===")
        print(f"Last Actual Exchange Rate: {last_actual_value['date'].date()} → {last_actual_value['actual']:.4f}\n")

        # Display all future forecasts
        print(future_forecasts[['date', 'forecast']].to_string(index=False))

        return {
            "message": "Pipeline executed successfully!",
            "last_actual": {
                "date": str(last_actual_value["date"].date()),
                "value": last_actual_value["actual"]
            },
            "predictions": future_forecasts[["date", "forecast"]].to_dict(orient="records")
        }
    else:
        return {"message": "Pipeline executed, but no forecast file was found."}

# Keep the original functionality when run as a script
if __name__ == "__main__":
    main()

