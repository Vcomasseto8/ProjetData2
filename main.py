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

        # Load the forecasted data and display the next days' predictions
    forecast_file = os.path.join(DATA_DIR, "forecast", "best_model_forecast.csv")

    if os.path.exists(forecast_file):
        forecast_df = pd.read_csv(forecast_file, parse_dates=["date"])

        # Último valor real disponível (última linha onde 'actual' não é NaN)
        last_actual_value = forecast_df.dropna(subset=["actual"]).iloc[-1]

        # Selecionar apenas as previsões futuras (onde 'actual' é NaN)
        future_forecasts = forecast_df[forecast_df["actual"].isna()]

        print("\n=== Exchange Rate Predictions for the Next Days ===")
        print(f"Last Actual Exchange Rate: {last_actual_value['date'].date()} → {last_actual_value['actual']:.4f}\n")
        
        # Exibir todas as previsões futuras
        print(future_forecasts[['date', 'forecast']].to_string(index=False))


if __name__ == "__main__":
    main()
