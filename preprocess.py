import os
import pandas as pd
import numpy as np

# Define data directory
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

class DataPreprocessor:
    def __init__(self, file_path=os.path.join(DATA_DIR, "exchange_rates.csv"), 
                 macro_path=os.path.join(DATA_DIR, "macro_data.csv"),
                 output_path=os.path.join(DATA_DIR, "preprocessed_data.csv")):
        self.file_path = file_path
        self.macro_path = macro_path
        self.output_path = output_path

    def load_data(self):
        """Loads exchange rate data, ensuring 'date' column exists and is properly formatted."""
        df = pd.read_csv(self.file_path)

        # Check if 'date' exists as a column
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
        else:
            # If no 'date' column, assume the first column is the index
            df.index = pd.to_datetime(df.iloc[:, 0])  # Convert first column to datetime
            df.drop(df.columns[0], axis=1, inplace=True)  # Remove duplicate first column

        df = df.sort_index()
        df.dropna(inplace=True)  # Ensure no NaN values remain

        return df


    def add_features(self, df):
        """Adds predictive features for forecasting."""

        # First-order differencing
        df["diff_close"] = df["close"].diff()

        # Rolling Median (Better than simple moving average)
        df["rolling_median_10"] = df["close"].rolling(window=10).median()

        # Moving Averages
        df["ma_3"] = df["close"].rolling(window=3).mean()
        df["ma_7"] = df["close"].rolling(window=7).mean()
        df["ma_30"] = df["close"].rolling(window=30).mean()

        # Momentum (Price change over 10 days)
        df["momentum_10"] = df["close"].diff(10)

        # Volatility Features
        df["volatility_10"] = df["diff_close"].rolling(window=10).std()
        df["volatility_30"] = df["diff_close"].rolling(window=30).std()

        # Volatility Ratio (New Feature)
        df["volatility_ratio_10"] = df["volatility_10"] / df["close"]

        # Lagged Features
        df["lag_1"] = df["close"].shift(1)
        df["lag_3"] = df["close"].shift(3)
        df["lag_7"] = df["close"].shift(7)

        # Trend Indicator (New Feature)
        df["trend_5"] = df["close"].rolling(window=5).mean() - df["close"].rolling(window=10).mean()

        # Seasonality Features
        df["day_of_week"] = df.index.dayofweek
        df["month"] = df.index.month

        # Drop NaN values caused by rolling operations
        df.dropna(inplace=True)

        return df

    def add_macro_data(self, df):
        """Merges macroeconomic indicators, handling missing values."""
        if not os.path.exists(self.macro_path):
            print(f"WARNING: Macro data file {self.macro_path} not found. Skipping merge.")
            return df

        macro_df = pd.read_csv(self.macro_path, parse_dates=["date"])
        macro_df.set_index("date", inplace=True)

        # Merge with exchange rate data
        df = df.join(macro_df, how="left")

        # Fill missing macro values using forward-fill and back-fill
        for col in macro_df.columns:
            df[col].fillna(method="ffill", inplace=True)
            df[col].fillna(method="bfill", inplace=True)

        return df

    def save_preprocessed_data(self, df):
        """Ensures the date column is saved correctly and removes interest_rate before saving."""
        
        # Drop 'interest_rate' if it exists
        if "interest_rate" in df.columns:
            print("Dropping 'interest_rate' column due to excessive missing values...")
            df.drop(columns=["interest_rate"], inplace=True)

        # Reset index to ensure 'date' is saved as a column
        df.reset_index(inplace=True)

        # Rename the index column to 'date'
        if df.columns[0] != "date":  
            df.rename(columns={df.columns[0]: "date"}, inplace=True)
            
        # Save to CSV without adding an extra index column
        df.to_csv(self.output_path, index=False)

        print(f" Preprocessed data saved to {self.output_path}")

    def run(self):
        """Runs the full preprocessing pipeline."""
        print(" Loading exchange rate data...")
        df = self.load_data()
        
        print(" Adding new features...")
        df = self.add_features(df)

        print(" Adding macroeconomic data (Inflation, Interest Rate, GDP Growth, Trade Balance)...")
        df = self.add_macro_data(df)
        
        print(" Saving final preprocessed dataset...")
        self.save_preprocessed_data(df)

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    preprocessor.run()
