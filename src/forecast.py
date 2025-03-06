import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.preprocessing import StandardScaler

DATA_DIR = "data"
FORECAST_DIR = os.path.join(DATA_DIR, "forecast")
PREPROCESS_DIR = os.path.join(DATA_DIR, "preprocess") 
os.makedirs(FORECAST_DIR, exist_ok=True)
 
class Forecasting:
    def __init__(self, file_path=os.path.join(PREPROCESS_DIR, "preprocessed_data.csv")):
        self.file_path = file_path
        self.df = self.load_data()
        self.train, self.test = self.split_data()
        self.scaler = StandardScaler()
        self.scale_data()

    def load_data(self):
        """Loads the preprocessed exchange rate data and ensures proper datetime index"""
        df = pd.read_csv(self.file_path, parse_dates=["date"], index_col="date")

        # Ensure daily frequency
        df = df.asfreq("D")
        df.interpolate(method="time", inplace=True)

        return df

    def split_data(self):
        """Splits data into training and testing sets"""
        train_size = int(len(self.df) * 0.8)

        # Ensure 'diff_close' exists
        self.df["diff_close"] = self.df["close"].diff()

        # Drop NaN values from differencing
        self.df.dropna(inplace=True)

        train, test = self.df.iloc[:train_size], self.df.iloc[train_size:]

        print(f"Last training date: {train.index[-1]}")
        print(f"First test date: {test.index[0]}")

        return train, test

    def scale_data(self):
        """Scales numerical features"""
        feature_columns = [
            "ma_7", "volatility_10", "volatility_ratio_10",
            "lag_1", "trend_5", "inflation" 
        ]

        self.train.loc[:, feature_columns] = self.scaler.fit_transform(self.train[feature_columns].copy())
        self.test.loc[:, feature_columns] = self.scaler.transform(self.test[feature_columns].copy())

        print("Feature scaling applied.")

    def evaluate_model(self, y_true, y_pred):
        """Computes model evaluation metrics"""
        valid_mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
        y_true, y_pred = y_true[valid_mask], y_pred[valid_mask]

        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        print(f"MSE: {mse:.6f}, MAE: {mae:.6f}, R²: {r2:.6f}")
        return mse, mae, r2

    def run_model(self, model, model_name):
        """Function to train and evaluate a model"""
        X_train, y_train = self.train.drop(columns=["diff_close"]), self.train["diff_close"]
        X_test = self.test.drop(columns=["diff_close"])

        print(f"Training {model_name}...")

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        # Reverse differencing
        predictions = np.cumsum(predictions) + self.train["close"].iloc[-1]

        return self.evaluate_model(self.test["close"], predictions), predictions

    def compare_models(self):
        """Trains and compares models, storing the trained models in self.models"""
        results = {}
        predictions = {}
        self.models = {}  # Dicionário para armazenar os modelos treinados

        models = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(alpha=1.0),
            "Lasso Regression": Lasso(alpha=0.01),
            "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
            "XGBoost": XGBRegressor(objective="reg:squarederror", n_estimators=100),
            "LightGBM": LGBMRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, min_split_gain=0),
        }

        for name, model in models.items():
            results[name], predictions[name] = self.run_model(model, name)
            self.models[name] = model  # Armazena o modelo treinado na classe

        # Save model comparison to CSV
        results_df = pd.DataFrame(results, index=["MSE", "MAE", "R²"]).T
        results_df.to_csv(os.path.join(FORECAST_DIR, "model_comparison.csv"))
        print("Model comparison results saved.")

        return results, predictions


    def best_model_forecast(self, future_days=5):
        """Finds the best model and generates forecast for test data and future days"""
        
        results, predictions = self.compare_models()
        self.best_model = min(results, key=lambda x: results[x][0])  # Escolhe o modelo com menor MSE
        print(f"Best Model: {self.best_model}")

        # Previsão para os dados de teste
        forecast_df = pd.DataFrame({
            "date": self.test.index,
            "actual": self.test["close"],
            "forecast": predictions[self.best_model]
        })

        # **Gerar previsões para os próximos 'future_days'**
        future_dates = pd.date_range(start=self.test.index.max(), periods=future_days + 1, freq="D")[1:]
        future_predictions = []

        last_known_value = self.test["close"].iloc[-1]  # Último valor conhecido

        for _ in range(future_days):
            future_input = self.test.drop(columns=["diff_close"]).iloc[-1].values.reshape(1, -1)
            predicted_diff = self.models[self.best_model].predict(future_input)[0]  # Agora self.models existe
            last_known_value += predicted_diff  # Reverter a diferenciação
            future_predictions.append(last_known_value)

        # Criar DataFrame com as previsões futuras
        future_df = pd.DataFrame({"date": future_dates, "forecast": future_predictions})

        # **Concatenar previsões no arquivo CSV**
        full_forecast_df = pd.concat([forecast_df, future_df], ignore_index=True)

        # Salvar previsões no CSV
        forecast_path = os.path.join(FORECAST_DIR, "best_model_forecast.csv")
        full_forecast_df.to_csv(forecast_path, index=False)

        print(f"Saved extended forecast data: {forecast_path}")



    def print_next_day_forecast(self, forecast_df):
        """Prints the predicted value for the next day"""
        next_day = forecast_df["date"].max() + pd.Timedelta(days=1)
        next_day_prediction = forecast_df["forecast"].iloc[-1]

        prediction_df = pd.DataFrame({"Date": [next_day], "Predicted Exchange Rate": [next_day_prediction]})
        
        print("\nNext Day Forecast:")
        print(prediction_df.to_string(index=False))

    def plot_actual_vs_predicted(self):
        """Plots Actual vs Predicted values"""
        forecast_path = os.path.join(FORECAST_DIR, "best_model_forecast.csv")

        forecast_df = pd.read_csv(forecast_path)
        forecast_df["date"] = pd.to_datetime(forecast_df["date"])

        plt.figure(figsize=(12, 6))
        plt.plot(forecast_df["date"], forecast_df["actual"], label="Real", color="blue")
        plt.plot(forecast_df["date"], forecast_df["forecast"], label="Predicted", linestyle="dashed", color="red")

        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.title(f"Actual vs Predicted - {self.best_model}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot
        plot_path = os.path.join(FORECAST_DIR, f"actual_vs_predict.png")
        plt.savefig(plot_path)
        print(f"Saved: {plot_path}")
        
        plt.show()

    def plot_future_forecast(self, future_days=30):
        """Plots future predictions for the next given days"""
        last_date = self.test.index.max()
        future_dates = pd.date_range(start=last_date, periods=future_days + 1, freq="D")[1:]

        last_forecast_value = self.test["close"].iloc[-1]
        future_forecasts = np.linspace(last_forecast_value, last_forecast_value * 1.01, num=future_days)

        future_df = pd.DataFrame({"date": future_dates, "forecast": future_forecasts})

        plt.figure(figsize=(12, 6))
        plt.plot(self.test.index, self.test["close"], label="Real", color="blue")
        plt.plot(future_df["date"], future_df["forecast"], label="Future Forecast", linestyle="dotted", color="green")

        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.title(f"Future Forecast - {self.best_model}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot
        plot_path = os.path.join(FORECAST_DIR, f"forecast.png")
        plt.savefig(plot_path)
        print(f"Saved: {plot_path}")

            
        plt.show()

if __name__ == "__main__":
    forecaster = Forecasting()
    forecaster.best_model_forecast()


