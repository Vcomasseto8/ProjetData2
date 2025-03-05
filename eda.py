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

# Diretórios
DATA_DIR = "data"
EDA_DIR = os.path.join(DATA_DIR, "eda")
os.makedirs(EDA_DIR, exist_ok=True)

# Carregar os dados
file_path = os.path.join(DATA_DIR, "preprocessed_data.csv")
df = pd.read_csv(file_path, parse_dates=["date"], index_col="date")

# Garantir frequência diária
df = df.asfreq("D")
df.interpolate(method="time", inplace=True)

# Gerar estatísticas descritivas
summary_stats = df.describe()
summary_stats.to_csv(os.path.join(EDA_DIR, "summary_statistics.csv"))

# Analisar valores ausentes
missing_values = df.isnull().sum()
missing_values.to_csv(os.path.join(EDA_DIR, "missing_values.csv"))

# Plotar tendência da taxa de câmbio ao longo do tempo
fig = px.line(df, x=df.index, y="close", title="BRL/EUR Exchange Rate Trend")
fig.write_html(os.path.join(EDA_DIR, "exchange_rate_trend.html"))

# Análise de bandas de Bollinger
df["ma_20"] = df["close"].rolling(window=20).mean()
df["std_20"] = df["close"].rolling(window=20).std()
df["upper_band"] = df["ma_20"] + (df["std_20"] * 2)
df["lower_band"] = df["ma_20"] - (df["std_20"] * 2)

fig_bollinger = go.Figure()
fig_bollinger.add_trace(go.Scatter(x=df.index, y=df["close"], mode="lines", name="Close Price"))
fig_bollinger.add_trace(go.Scatter(x=df.index, y=df["upper_band"], mode="lines", name="Upper Band", line=dict(color="red", dash="dash")))
fig_bollinger.add_trace(go.Scatter(x=df.index, y=df["lower_band"], mode="lines", name="Lower Band", line=dict(color="green", dash="dash")))
fig_bollinger.write_html(os.path.join(EDA_DIR, "bollinger_bands.html"))

# Matriz de correlação
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Matrix")
plt.savefig(os.path.join(EDA_DIR, "correlation_matrix.png"))
plt.close()

# Análise de volatilidade ao longo do tempo
df["volatility"] = df["close"].pct_change().rolling(window=30).std()
fig_volatility = px.line(df, x=df.index, y="volatility", title="Volatility Trend (30-day Rolling)")
fig_volatility.write_html(os.path.join(EDA_DIR, "volatility_trend.html"))

# Decomposição de séries temporais
decomposition = seasonal_decompose(df["close"], model="multiplicative", period=30)
fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
decomposition.observed.plot(ax=axes[0], legend=False, title="Observed")
decomposition.trend.plot(ax=axes[1], legend=False, title="Trend")
decomposition.seasonal.plot(ax=axes[2], legend=False, title="Seasonality")
decomposition.resid.plot(ax=axes[3], legend=False, title="Residuals")
plt.tight_layout()
plt.savefig(os.path.join(EDA_DIR, "time_series_decomposition.png"))
plt.close()

# Retornos logarítmicos e sua distribuição
df["log_returns"] = np.log(df["close"] / df["close"].shift(1))
plt.figure(figsize=(10, 6))
sns.histplot(df["log_returns"].dropna(), bins=50, kde=True)
plt.title("Distribution of Log Returns")
plt.savefig(os.path.join(EDA_DIR, "returns_distribution.png"))
plt.close()

# Autocorrelação dos retornos
plt.figure(figsize=(10, 6))
plot_acf(df["log_returns"].dropna(), lags=30)
plt.title("Autocorrelation of Returns")
plt.savefig(os.path.join(EDA_DIR, "acf_returns.png"))
plt.close()

# Médias móveis (curta e longa)
fig_ma = px.line(df, x=df.index, y=["close", "ma_20"], title="Moving Averages")
fig_ma.write_html(os.path.join(EDA_DIR, "moving_averages.html"))

# Análise macroeconômica
fig_macro = px.line(df, x=df.index, y=["inflation", "gdp_growth", "trade_balance"], title="Macroeconomic Indicators Over Time")
fig_macro.write_html(os.path.join(EDA_DIR, "macro_analysis.html"))

print("EDA completed. All files saved in the 'eda' directory.")


