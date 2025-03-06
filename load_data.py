import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

# Validate API keys
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Alpha Vantage API Key not found. Set ALPHA_VANTAGE_API_KEY in .env")

if not FRED_API_KEY:
    raise ValueError("FRED API Key not found. Set FRED_API_KEY in .env")

# Define directories
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Define file paths
EXCHANGE_FILE = os.path.join(DATA_DIR, "exchange_rates.csv")
MACRO_FILE = os.path.join(DATA_DIR, "macro_data.csv")

# Define API URLs
EXCHANGE_RATE_URL = "https://www.alphavantage.co/query"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

# Define date range (last 5 years)
END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=5 * 365)


class DataLoader:
    def __init__(self):
        self.exchange_data = None
        self.macro_data = None

    def fetch_exchange_rate(self, from_currency="EUR", to_currency="BRL"):
        """Fetches historical exchange rate data from Alpha Vantage"""
        print("Fetching exchange rate data...")

        params = {
            "function": "FX_DAILY",
            "from_symbol": from_currency,
            "to_symbol": to_currency,
            "apikey": ALPHA_VANTAGE_API_KEY,
            "outputsize": "full"
        }

        response = requests.get(EXCHANGE_RATE_URL, params=params)
        data = response.json()

        if "Time Series FX (Daily)" not in data:
            raise ValueError(f"Error fetching exchange rate data: {data}")

        df = pd.DataFrame.from_dict(data["Time Series FX (Daily)"], orient="index")
        df.index = pd.to_datetime(df.index)  # Convert index to datetime
        df = df.sort_index()

        # Rename columns and convert types
        df.columns = ["open", "high", "low", "close"]
        df = df.astype(float)

        # Filter last 5 years
        df = df[df.index >= START_DATE]

        # Save to CSV
        df.to_csv(EXCHANGE_FILE)
        print(f"Exchange rate data saved: {EXCHANGE_FILE}")
        self.exchange_data = df

    def fetch_macro_data(self):
        """Fetches inflation and interest rate from FRED API"""
        print("Fetching macroeconomic indicators...")

        indicators = {
            "inflation": "BRACPIALLMINMEI",  # BRL Inflation Rate
            "interest_rate": "IRSTCI01BRM156N",  # SELIC Rates
    
        }

        macro_df = pd.DataFrame()

        for indicator, series_id in indicators.items():
            print(f"Fetching {indicator} data...")
            params = {
                "series_id": series_id,
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "observation_start": START_DATE.strftime("%Y-%m-%d")
            }

            response = requests.get(FRED_URL, params=params)
            data = response.json()

            if "observations" not in data:
                print(f"Warning: No data for {indicator}")
                continue

            temp_df = pd.DataFrame(data["observations"])

            # Convert date column to datetime
            temp_df["date"] = pd.to_datetime(temp_df["date"])
            temp_df.set_index("date", inplace=True)

            # Keep only the necessary column (value) and rename it
            temp_df = temp_df[["value"]].rename(columns={"value": indicator})

            # Convert to numeric (handling errors)
            temp_df[indicator] = pd.to_numeric(temp_df[indicator], errors="coerce")

            # Merge with the main macroeconomic DataFrame
            if macro_df.empty:
                macro_df = temp_df
            else:
                macro_df = macro_df.join(temp_df, how="outer")

        # Filter last 5 years
        macro_df = macro_df[macro_df.index >= START_DATE]

        # Save to CSV
        macro_df.to_csv(MACRO_FILE)
        print(f"Macroeconomic data saved: {MACRO_FILE}")
        self.macro_data = macro_df

    def run(self):
        """Runs data fetching process."""
        self.fetch_exchange_rate()
        self.fetch_macro_data()


if __name__ == "__main__":
    loader = DataLoader()
    loader.run()
