EUR/BRL Exchange Rate Forecasting with Machine Learning

This project simulates a real-world business scenario where financial data is collected, preprocessed, analyzed, and used for forecasting using Machine Learning models. 
Exchange rate forecasting is crucial for businesses engaged in international trade, investors managing foreign assets, and individuals planning financial transactions across borders. The ability to predict exchange rate fluctuations can help in hedging risks, optimizing currency conversion strategies, and making informed investment decisions.

The pipeline consists of:
- Data retrieval from APIs
- Feature engineering
- Exploratory Data Analysis (EDA)
- Multiple Machine Learning models for forecasting exchange rates
- Performance evaluation and model selection

📁 Project Structure:

📁 data/             # Contains raw and processed data
    📁 eda/              # Stores exploratory data analysis outputs
    📁 forecast/         # Stores model forecasts and comparison results
📜 load_data.py      # Fetches financial and macroeconomic data
📜 preprocess.py     # Cleans data and generates features for ML
📜 eda.py            # Performs exploratory data analysis
📜 forecast.py       # Runs ML models and generates forecasts
📜 main.py           # Main script executing the full pipeline
📜 requirements.txt  # Lists dependencies

🔧 Installation & Setup

Requirements

Python 3.8+

Pip

Setup Instructions

# Clone the repository
git clone https://github.com/your-repo-name.git
cd your-repo-name

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: `venv\Scripts\activate`)

# Install dependencies
pip install -r requirements.txt

# Set up API keys in a .env file
echo "ALPHA_VANTAGE_API_KEY=your_api_key" > .env

▶ How to Run the Project

Run the entire pipeline:

python main.py

Run individual steps:

# Step 1: Fetch financial & macroeconomic data
python load_data.py

# Step 2: Preprocess the data
python preprocess.py

# Step 3: Perform Exploratory Data Analysis
python eda.py

# Step 4: Run Machine Learning forecasting models
python forecast.py

📊 Features & Methodology

✅ Key Features

Automated data retrieval from APIs

Feature engineering for financial time series

Exploratory Data Analysis (EDA) with visualizations

Multiple ML models (Random Forest, XGBoost, LightGBM, etc.)

Performance comparison & model selection

Forecast generation and evaluation

📉 Machine Learning Models Used

Model

Type

Linear Regression

ML

Random Forest

ML

XGBoost

ML

LightGBM

ML

Prophet

ML

📈 Outputs & Results

📊 Model Comparison (MSE, MAE, R²) saved in data/forecast/model_comparison.csv

📉 Forecast Results stored in data/forecast/best_model_forecast.csv

📈 Visualizations saved in data/eda/

❗ Issues & Troubleshooting

If data fetching fails, check API keys in .env

If macroeconomic indicators are missing, verify load_data.py

If models perform poorly, experiment with different features in preprocess.py

🚀 Future Improvements

Improve model performance with feature selection

Add deep learning models (LSTMs, Transformers)

Deploy as a web app using Flask/FastAPI + Streamlit

🤝 Contributors & Contact

Your Name (@yourgithub) – LinkedIn

Open to contributions! Feel free to submit a pull request.