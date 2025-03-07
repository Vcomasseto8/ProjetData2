EUR/BRL Exchange Rate Forecasting with Machine Learning 🏦📈

This project simulates a real-world business scenario where financial data is collected, preprocessed, analyzed, and used for forecasting using Machine Learning models.

Exchange rate forecasting is crucial for:
✔️ Businesses engaged in international trade.
✔️ Investors managing foreign assets.
✔️ Individuals planning financial transactions across borders.

The ability to predict exchange rate fluctuations can help in hedging risks, optimizing currency conversion strategies, and making informed investment decisions.

📌 Pipeline Overview
This project follows a structured ML pipeline:
✅ Data Retrieval from financial APIs.
✅ Feature Engineering for financial time series.
✅ Exploratory Data Analysis (EDA) with visualizations.
✅ Multiple Machine Learning models for forecasting.
✅ Performance evaluation & model selection.

📂 Project Structure
/ProjetData2
│── data/                      # Stores raw & processed data
│   ├── eda/                   # Exploratory Data Analysis outputs
│   ├── forecast/              # Forecasts & model comparisons
│   ├── preprocess/            # Preprocessed datasets
│   ├── raw/                   # Original raw data CSVs
│
│── src/                       # Core scripts for data pipeline
│   ├── load_data.py           # Fetches financial & macroeconomic data
│   ├── preprocess.py          # Data cleaning & feature engineering
│   ├── eda.py                 # Exploratory Data Analysis (EDA)
│   ├── forecast.py            # Machine Learning models for forecasting
│
│── main.py                    # Executes the full pipeline
│── predict.py                  # FastAPI API for exchange rate prediction
│── requirements.txt            # List of dependencies
│── Dockerfile                  # Docker configuration for containerization
│── aplip.py                      # Web app to see exchange rates
│── docker-compose.yml          # Compose file for container orchestration
│── .env                        # API keys for data fetching (ignored in Git)
│── render.yaml                 # Web Service
│── README.md                   # Project documentation


🔧 Installation & Setup
💻 Requirements
Python 3.8+
Pip
(Optional) Docker

📥 Setup Instructions
# Clone the repository
git clone https://github.com/Vcomasseto8/ProjetData2.git
cd ProjetData2
# Install dependencies
pip install -r requirements.txt
# Set up API keys in a .env file
echo "ALPHA_VANTAGE_API_KEY=your_api_key" > .env
echo "FRED_API_KEY=your_api_key" >> .env

▶ How to Run the Project
Run the full pipeline:
python main.py

Run individual steps:
# Step 1: Fetch financial & macroeconomic data
python src/load_data.py
# Step 2: Preprocess the data
python src/preprocess.py
# Step 3: Perform Exploratory Data Analysis
python src/eda.py
# Step 4: Train ML models & generate forecasts
python src/forecast.py

🌍 Running the API (FastAPI + Docker)
Run API Without Docker
uvicorn predict:app --host 0.0.0.0 --port 8000
Check API at 👉 http://localhost:8000/docs
