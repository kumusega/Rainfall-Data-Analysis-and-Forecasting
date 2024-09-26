import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

df = pd.read_csv("Rainfall_data.csv")

"""To see count, mean, standard deviation, and minimum and maximum values in each columns"""
print(df.describe())

"""To see content of each column and data types present in it along with the number of null values present"""
print(df.info())

"""converting datetime formate(combine year,month,day into single column)"""

df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])


"""Extract year, month and weekdays from the Date index"""

df['Year']  = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df['Weekdays'] = df["Date"].dt.dayofweek

""" Replace column "Day" with column "Weekdays" """

df["Day"] = df["Weekdays"]


"""Drop the Year, Month, and Day columns"""

df.drop(columns=["Weekdays"],inplace=True)


"""Rename the "Day" column to "Weekdays" """

df.rename(columns={"Day": "Weekdays"}, inplace=True)


"""Calculate mean precipitation for each day of the week"""

mean_precipitation = df.groupby("Weekdays")["Precipitation"].mean()


"""To visualize relationships between Specific Humidity, Relative Humidity, Temperature and target variable(Precipitation)"""

plt.style.use("dark_background")
plt.figure()
plt.scatter(df['Specific Humidity'], df['Precipitation'], color="lime")
plt.title('Scatter plot of Specific Humidity vs Precipitation')
plt.xlabel('Specific Humidity')
plt.ylabel('Precipitation')
plt.show()

plt.figure()
plt.scatter(df['Relative Humidity'], df['Precipitation'], color="cyan")
plt.title('Scatter plot of Relative Humidity vs Precipitation')
plt.xlabel('Relative Humidity')
plt.ylabel('Precipitation')
plt.show()

plt.figure()
plt.scatter(df['Temperature'], df['Precipitation'], color="fuchsia")
plt.title('Scatter plot of Temperature vs Precipitation')
plt.xlabel('Temperature')
plt.ylabel('Precipitation')
plt.show()

"""To visualize how precipitation changes over time"""

plt.figure(figsize=(12,6))
plt.bar(df["Year"],df["Precipitation"],label="yearly precipitation", color="deepskyblue")
plt.title("yearly precipitation over time")
plt.xlabel("Year")
plt.ylabel("Precipitation")
plt.legend()
plt.show()

plt.figure(figsize=(12,6))
plt.bar(df["Month"],df["Precipitation"],label="monthly precipitation", color="gold")
plt.title("monthly precipitation over time")
plt.xlabel("Month")
plt.ylabel("Precipitation")
plt.legend()
plt.show()

plt.figure(figsize=(12,6))
plt.bar(mean_precipitation.index, mean_precipitation.values, label="weekly precipitation", color="tomato")
plt.title("precipitation over each day of week")
plt.xlabel("day of week")
plt.ylabel("mean precipitation")
plt.xticks(ticks=range(7),labels=["monday","tuesday","wednesday","thrusday","friday","saturday","sunday"])
plt.legend()
plt.show()

"""By setting the "‘Date’" column as the index(for easily perform time series operations on your DataFrame)."""

time_series = df.set_index("Date",inplace=True)
print(df)

"""To get insights of the data"""
decomposition = seasonal_decompose(df["Precipitation"], model="additive")
trend = decomposition.trend
seasonal = decomposition.seasonal
residue = decomposition.resid
print(trend)
print(seasonal)
print(residue)

"""Plot the time series of precipitation to identify trends, seasonality and residue"""

plt.figure(figsize=(12,8))
plt.subplot(411)
plt.plot(df["Precipitation"], label="actual precipitation data", color="green")
plt.legend()

plt.subplot(412)
plt.plot(trend, label="trend data", color="red")
plt.legend()

plt.subplot(413)
plt.plot(seasonal, label="seasonal data", color="blue")
plt.legend()

plt.subplot(414)
plt.plot(residue, label="residue data", color="orange")
plt.legend()
plt.show()

"""ADF Test for stationarity(before reject the null hypothesis) before diffrencing"""

target_var = df["Precipitation"]

ADF_test = adfuller(target_var)
print('ADF Statistic (Differenced):', ADF_test[0])
print('p-value (Differenced):', ADF_test[1])

plt.figure(figsize=(12,5))
plt.subplot(121)
plot_acf(target_var, lags=30, ax=plt.gca(), color="yellow")
plt.subplot(122)
plot_pacf(target_var, lags=30, ax=plt.gca(),color="coral")
plt.show()

"""Differencing the series to make it stationary"""
series_diff = target_var.diff().dropna()
print(series_diff)

sm.graphics.tsa.plot_acf(series_diff, lags=20,color="red")
plt.show()

"""ADF Test for stationarity(after reject the null hypothesis) with its ACF and PACF plot(seasonal)PDQS"""
"""ADF Test for stationarity (after differencing)"""

target_var = df["Precipitation"]

"""Seasonal differencing"""
series_diff = target_var.diff(12).dropna()
print(series_diff)

ADF_test_seasonal = adfuller(series_diff)
print('ADF Statistic (Seasonally Differenced):', ADF_test_seasonal[0])
print('p-value (Seasonally Differenced)):', ADF_test_seasonal[1])

plt.figure(figsize=(12,5))
plt.subplot(121)
plot_acf(series_diff, lags=30, ax=plt.gca(), color="deeppink")
plt.subplot(122)
plot_pacf(series_diff, lags=30, ax=plt.gca(),color="magenta")
plt.show()

"""Fit a SARIMA model"""

"""Example order and seasonal order values"""

p, d, q = 1, 1, 1

"""For monthly data with a yearly seasonality"""

P, D, Q, S = 1,1,1,12

model = sm.tsa.SARIMAX(target_var, order=(p,d,q), seasonal_order=(P,D,Q,S))
arima_output = model.fit()

print(arima_output.summary())

"""Make predictions"""

forecast = arima_output.get_forecast(steps=12)
forecast_mean = forecast.predicted_mean

"""Plot the actual data and the forecast"""

plt.figure(figsize=(12, 6))
plt.plot(target_var, label='actual data', color="blue")
plt.plot(forecast_mean, label='SARIMA prediction', color="yellow")
plt.legend()
plt.show()