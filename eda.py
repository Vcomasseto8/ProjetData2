import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
import plotly.express as px
import plotly.graph_objects as go

# Define directories
DATA_DIR = "data"
EDA_DIR = os.path.join(DATA_DIR, "eda")
os.makedirs(EDA_DIR, exist_ok=True)

class ExploratoryDataAnalysis:
    def __init__(self, file_path=os.path.join(DATA_DIR, "preprocessed_data.csv")):
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self):
        """Loads preprocessed data and handles missing values."""
        print("Loading preprocessed data for EDA...")
        df = pd.read_csv(self.file_path, parse_dates=["date"], index_col="date")
        df = df.asfreq("D")
        df.interpolate(method="time", inplace=True)  # Fill missing values
        return df

    def save_summary_statistics(self):
        """Saves summary statistics and missing values."""
        print("Saving summary statistics and missing values report...")
        summary_stats = self.df.describe()
        summary_stats.to_csv(os.path.join(EDA_DIR, "summary_statistics.csv"))

        missing_values = self.df.isnull().sum()
        missing_values.to_csv(os.path.join(EDA_DIR, "missing_values.csv"))

    def plot_exchange_rate_trend(self):
        """Plots and saves exchange rate trend."""
        print("Generating exchange rate trend visualization...")
        fig = px.line(self.df, x=self.df.index, y="close", title="BRL/EUR Exchange Rate Trend")
        fig.write_html(os.path.join(EDA_DIR, "exchange_rate_trend.html"))

    def plot_bollinger_bands(self):
        """Computes and plots Bollinger Bands."""
        print("Generating Bollinger Bands visualization...")
        self.df["ma_20"] = self.df["close"].rolling(window=20).mean()
        self.df["std_20"] = self.df["close"].rolling(window=20).std()
        self.df["upper_band"] = self.df["ma_20"] + (self.df["std_20"] * 2)
        self.df["lower_band"] = self.df["ma_20"] - (self.df["std_20"] * 2)

        fig_bollinger = go.Figure()
        fig_bollinger.add_trace(go.Scatter(x=self.df.index, y=self.df["close"], mode="lines", name="Close Price"))
        fig_bollinger.add_trace(go.Scatter(x=self.df.index, y=self.df["upper_band"], mode="lines", name="Upper Band", line=dict(color="red", dash="dash")))
        fig_bollinger.add_trace(go.Scatter(x=self.df.index, y=self.df["lower_band"], mode="lines", name="Lower Band", line=dict(color="green", dash="dash")))
        fig_bollinger.write_html(os.path.join(EDA_DIR, "bollinger_bands.html"))

    def plot_correlation_matrix(self):
        """Plots and saves correlation matrix."""
        print("Generating feature correlation matrix...")
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.df.corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
        plt.title("Feature Correlation Matrix")
        plt.savefig(os.path.join(EDA_DIR, "correlation_matrix.png"))
        plt.close()

    def plot_volatility_trend(self):
        """Computes and plots volatility trend."""
        print("Generating volatility trend visualization...")
        self.df["volatility"] = self.df["close"].pct_change().rolling(window=30).std()
        fig_volatility = px.line(self.df, x=self.df.index, y="volatility", title="Volatility Trend (30-day Rolling)")
        fig_volatility.write_html(os.path.join(EDA_DIR, "volatility_trend.html"))

    def plot_time_series_decomposition(self):
        """Performs and saves time series decomposition."""
        print("Performing time series decomposition...")
        decomposition = seasonal_decompose(self.df["close"], model="multiplicative", period=30)
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        decomposition.observed.plot(ax=axes[0], legend=False, title="Observed")
        decomposition.trend.plot(ax=axes[1], legend=False, title="Trend")
        decomposition.seasonal.plot(ax=axes[2], legend=False, title="Seasonality")
        decomposition.resid.plot(ax=axes[3], legend=False, title="Residuals")
        plt.tight_layout()
        plt.savefig(os.path.join(EDA_DIR, "time_series_decomposition.png"))
        plt.close()

    def plot_log_returns_distribution(self):
        """Computes and plots log returns distribution."""
        print("Generating log returns distribution plot...")
        self.df["log_returns"] = np.log(self.df["close"] / self.df["close"].shift(1))
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df["log_returns"].dropna(), bins=50, kde=True)
        plt.title("Distribution of Log Returns")
        plt.savefig(os.path.join(EDA_DIR, "returns_distribution.png"))
        plt.close()

    def plot_acf_returns(self):
        """Plots and saves autocorrelation function of returns."""
        print("Generating autocorrelation plot of returns...")
        plt.figure(figsize=(10, 6))
        plot_acf(self.df["log_returns"].dropna(), lags=30)
        plt.title("Autocorrelation of Returns")
        plt.savefig(os.path.join(EDA_DIR, "acf_returns.png"))
        plt.close()

    def plot_moving_averages(self):
        """Plots and saves moving averages."""
        print("Generating moving averages plot...")
        fig_ma = px.line(self.df, x=self.df.index, y=["close", "ma_20"], title="Moving Averages")
        fig_ma.write_html(os.path.join(EDA_DIR, "moving_averages.html"))

    def plot_macro_analysis(self):
        """Plots and saves macroeconomic indicators over time."""
        print("Generating macroeconomic indicators visualization...")
        fig_macro = px.line(self.df, x=self.df.index, y=["inflation", "gdp_growth", "trade_balance"], title="Macroeconomic Indicators Over Time")
        fig_macro.write_html(os.path.join(EDA_DIR, "macro_analysis.html"))

    def run(self):
        """Runs all EDA steps sequentially."""
        print("\n=== Starting Exploratory Data Analysis (EDA) ===")
        self.save_summary_statistics()
        self.plot_exchange_rate_trend()
        self.plot_bollinger_bands()
        self.plot_correlation_matrix()
        self.plot_volatility_trend()
        self.plot_time_series_decomposition()
        self.plot_log_returns_distribution()
        self.plot_acf_returns()
        self.plot_moving_averages()
        self.plot_macro_analysis()
        print("✅ EDA completed. All visualizations saved in 'eda' directory.")

# Run EDA if executed directly
if __name__ == "__main__":
    eda = ExploratoryDataAnalysis()
    eda.run()
