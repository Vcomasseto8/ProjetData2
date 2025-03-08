# 🏦📈 EUR/BRL Exchange Rate Forecasting with Machine Learning

## **Overview**

This project simulates a real-world business scenario where financial data is collected, preprocessed, analyzed, and used for forecasting using Machine Learning models. Exchange rate forecasting is crucial for businesses engaged in international trade, investors managing foreign assets, and individuals planning financial transactions across borders. The ability to predict exchange rate fluctuations can help in hedging risks, optimizing currency conversion strategies, and making informed investment decisions.

**Why is exchange rate forecasting important?**
- **Businesses** engaged in international trade.  
- **Investors** managing foreign assets.  
- **Individuals** planning financial transactions across borders.  

The ability to predict exchange rate fluctuations helps in **hedging risks, optimizing currency conversion strategies, and making informed investment decisions**.

---

## **Pipeline Overview**

This project follows a structured **Machine Learning pipeline**:

- **Data Retrieval** from financial APIs.  
- **Feature Engineering** for financial time series.  
- **Exploratory Data Analysis (EDA)** with visualizations.  
- **Multiple Machine Learning models** for forecasting.  
- **Performance evaluation & model selection.**  
- **Deployment of an API for real-time predictions.**  

---

## 📂 Project Structure
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


---

## Installation & Setup

### **Requirements**
- Python **3.8+**
- Pip
- (Optional) **Docker** for containerized execution.

### **Setup Instructions**

#### **Clone the repository**
git clone https://github.com/Vcomasseto8/ProjetData2.git
cd ProjetData2

**Install dependencies**
pip install -r requirements.txt

**Set up API keys in a .env file**
echo "ALPHA_VANTAGE_API_KEY=your_api_key" > .env
echo "FRED_API_KEY=your_api_key" >> .env

▶ How to Run the Project
**Run the full pipeline**
python main.py

**Run individual steps**
# Step 1: Fetch financial & macroeconomic data
python src/load_data.py

# Step 2: Preprocess the data
python src/preprocess.py

# Step 3: Perform Exploratory Data Analysis
python src/eda.py

# Step 4: Train ML models and generate forecasts
python src/forecast.py

**Run the API (FastAPI)**
uvicorn api:app --host 0.0.0.0 --port 8000

**Run the Web App (Streamlit)**
streamlit run api/aplip.py

**Features & Methodology**
**Key Features**
- Automated Data Retrieval from APIs (Alpha Vantage, FRED).
- Feature Engineering for financial time series forecasting.
- Exploratory Data Analysis (EDA) to understand key patterns.
- Multiple Machine Learning Models:
    - Linear Regression
    - Ridge Regression
    - Lasso Regression
    - Random Forest
    - XGBoost
    - LightGBM
- Performance Evaluation: MSE, MAE, R².
- API Deployment via FastAPI on Render.

**Running with Docker**
**Build the Docker Image**
docker build -t vcomasseto/projetdata:latest .

**Run the Container**
docker run -p 8000:8000 vcomasseto/projetdata:latest

**Push the Image to Docker Hub**
docker tag vcomasseto/projetdata:latest vcomasseto/projetdata:latest
docker push vcomasseto/projetdata:latest

**Pull and Run the Container (External Users)**
docker pull vcomasseto/projetdata:latest
docker run -p 8000:8000 vcomasseto/projetdata:latest

**How to Use the API**
Make a Request to Get Predictions
curl https://projetdata2.onrender.com/predict/2025-03-10

**Example Response:**
{
    "date": "2025-03-10",
    "predicted_exchange_rate": 6.356
}

**Next Steps & Future Improvements**
While this project delivers a strong foundation, several enhancements can improve forecasting accuracy and model robustness:

- Implement GARCH Models
The team did not explore GARCH (Generalized Autoregressive Conditional Heteroskedasticity), which models volatility over time. Integrating GARCH will allow better representation of time-varying variance.
- Cross-Validation for Model Training
Currently, we use a simple 80/20 Train-Test split.
K-Fold Cross-Validation should be implemented to improve generalization.
- Hyperparameter Tuning
Apply GridSearchCV or Bayesian Optimization to optimize model parameters.
- Deep Learning Models
Explore LSTMs or Transformers to capture long-term dependencies in exchange rate movements.
- Improve API & Deployment

**Contributors & Contact**

Vitoria Comasseto (@Vcomasseto8) – www.linkedin.com/in/vitoria-comasseto 
Carolina Alexandra Urtubia (@totaurt) - www.linkedin.com/in/curtubia/ 
Henriqu Viola Carvalho (@hqviolake) - www.linkedin.com/in/hviolac/ 
Martin Interlurralde Spiniello - www.linkedin.com/in/mart%C3%ADn-iturralde-spiniello-12084b239/




