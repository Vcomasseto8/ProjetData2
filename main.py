import os
import pandas as pd
from src.load_data import DataLoader
from src.preprocess import DataPreprocessor
from src.forecast import Forecasting
from src.eda import ExploratoryDataAnalysis 

# Define directories
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def main():
    print("\n=== Step 1: Loading Data ===")
    loader = DataLoader()
    loader.run()

    print("\n=== Step 2: Preprocessing Data ===")
    preprocessor = DataPreprocessor()
    preprocessor.run()

    print("\n=== Step 3: Exploratory Data Analysis ===")
    eda = ExploratoryDataAnalysis()
    eda.run()  # Run the EDA process

    print("\n=== Step 4: Forecasting ===")
    forecaster = Forecasting()
    forecaster.best_model_forecast()

    # Load the forecasted data and display the next day's prediction
    forecast_file = os.path.join(DATA_DIR, "forecast", "best_model_forecast.csv")
    if os.path.exists(forecast_file):
        forecast_df = pd.read_csv(forecast_file)
        next_day_forecast = forecast_df.iloc[-1]  # Last row is the most recent prediction
        print("\n=== Next Day Predicted Exchange Rate ===")
        print(next_day_forecast)

if __name__ == "__main__":
    main()
