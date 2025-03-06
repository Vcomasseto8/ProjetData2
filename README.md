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
    📁 preprocess/       # Stores preprocess csv
    📁 raw/              # Stores raws csvs
📁 src/ 
    📜 load_data.py      # Fetches financial and macroeconomic data
    📜 preprocess.py     # Cleans data and generates features for ML
    📜 eda.py            # Performs exploratory data analysis
    📜 forecast.py       # Runs ML models and generates forecasts
📜 main.py           # Main script executing the full pipeline
📜 requirements.txt  # Lists dependencies
⚙.env                # Stores the API's keys

🔧 Installation & Setup

Requirements

Python 3.8+

Pip

Setup Instructions

# Clone the repository
git clone (https://github.com/Vcomasseto8/ProjetData2)

# Install dependencies
pip install -r requirements.txt

# Set up API keys in a .env file
echo "ALPHA_VANTAGE_API_KEY=your_api_key" > .env
echo "FRED_API_KEY" = your_api_key" > .env

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

Multiple ML models (Linear Regression, LinearRegression, Ridge Regression, 
                    Lasso Regression, Random Forest, XGBoost LightGBM)

Performance comparison & model selection

Forecast generation and evaluation

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

🤝 Contributors & Contact

Vitoria Comasseto (@Vcomasseto8) – www.linkedin.com/in/vitoria-comasseto
Carolina Alexandra Urtubia (@totaurt) - www.linkedin.com/in/curtubia/
Henriqu Viola Carvalho (@hqviolake) - www.linkedin.com/in/hviolac/
Martin Interlurralde Spiniello (@) - www.linkedin.com/in/mart%C3%ADn-iturralde-spiniello-12084b239/


Open to contributions! Feel free to submit a pull request.