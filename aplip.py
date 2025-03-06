import pandas as pd
import streamlit as st

forecast_df = pd.read_csv("data/forecast/best_model_forecast.csv")
forecast_df["date"] = pd.to_datetime(forecast_df["date"])  

st.title("BRL/EUR Exchange Rate Prediction")

st.subheader("Latest Exchange Rate Prediction")
st.write(forecast_df.tail(7))

# Select a future date
selected_date = st.date_input("Select a date in the next 5 days", forecast_df["date"].max())

selected_date = pd.to_datetime(selected_date)

if selected_date in forecast_df["date"].values:
    predicted_value = forecast_df.loc[forecast_df["date"] == selected_date, "forecast"].values[0]
    st.subheader(f"Predicted Exchange Rate for {selected_date.date()}: {predicted_value}")
else:
    st.warning("No prediction available for this date.")

