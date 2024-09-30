📊 Univariate Time Series Analysis and Forecasting

🚀 Project Overview
 •	This project focuses on univariate time series analysis using historical precipitation data. The main goal is to forecast future rainfall using advanced time series models.

Objectives:
 •	🛠️ Analyze precipitation patterns over time.
 •	📈 Forecast future precipitation values using the SARIMA model.

📦 Imports:
 •	pandas for data manipulation.
 •	matplotlib.pyplot for data visualization.
 •	statsmodels libraries for time series decomposition, stationarity testing (ADF test), autocorrelation (ACF) and partial autocorrelation 
   (PACF) plots, and modeling with SARIMAX.
 •	warnings to suppress unnecessary warnings.

📁 Dataset:
 •	Source: Rainfall Dataset.
 •	Key Attributes: Date, Precipitation, Temperature, Humidity, etc.

📥 Data Loading and Initial Exploration:
 •	The script reads the rainfall data from a CSV file (Rainfall_data.csv).
 •	It uses df.describe() to display basic statistics (mean, standard deviation, etc.) for each column.
 •	df.info()  provides an overview of the dataset, including data types and null values.

🧹 Data Preprocessing
 •	A new Date column is created by combining Year, Month, and Day.
 •	Feature Engineering: Extracted Year, Month, and Weekday from the date column for analysis.
 •	Renames the Day column to Weekdays and drops unnecessary columns.

🔍 Exploratory Data Analysis (EDA)
 •	Visualization: • Scatter plots are created to visualize the relationship between Specific Humidity, Relative Humidity, Temperature, and 
                 Precipitation.
                 • Bar plots visualize how precipitation changes over time (yearly, monthly, and weekly).
 •	Decomposition: • Sets the Date column as the index for easier time series operations.
                 • Decomposes the precipitation time series into trend, seasonal, and residual components using seasonal_decompose.
                 • Plots the decomposed components to analyze the data.

🤖 Modeling and Prediction
 •	Stationarity Testing: •	Performs the Augmented Dickey-Fuller (ADF) test to check the stationarity of the Precipitation series.
 •	ACF & PACF Analysis:  •	ACF and PACF plots are generated to examine the autocorrelation of the time series. 
                        •	Both autocorrelation and partial autocorrelation functions (ACF and PACF) are used to identify the order of ARIMA 
                          models.
                        • The ACF helps in identifying the moving average (MA) part, while the PACF helps in identifying the autoregressive 
                          (AR) part.
                        •	Applies differencing to make the series stationary if needed, and performs the ADF test again.
 •	SARIMA Model: •	A Seasonal ARIMA (SARIMA) model is built with specified order and seasonal order parameters. 
                •	Fits the model to the precipitation data and generates a summary of the model's performance.

📊 Results and Discussion
 •	SARIMA Forecast: • The model is used to forecast future values (e.g., for the next 12 steps).
                   • Plots the actual data alongside the SARIMA predictions to visualize the model's forecast accuracy.
 •	Model Performance: • The forecasted values closely followed the trend and seasonal patterns of the actual data.

🔮 Future Work
 •	Model Improvement: Explore more complex models (e.g., Prophet, deep learning) for better accuracy.
 •	Real-Time Forecasting: Integrate real-time data streams for continuous forecasting and timely decision-making.
