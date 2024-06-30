# importing all the libraries used to run the code
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Used to not show warning at the terminal while running this code
pd.options.mode.chained_assignment = None

#Defining the initial parameters to download the asset info from YFinance
ticker = "^BVSP"
inicio = "2015-01-01"
fim = "2021-04-12"
# datetime.today().strftime('%Y-%m-%d')

df = yf.download(ticker, start = inicio, end = fim)

#Set both the amount of days to be consiedered when calculling the rolling mean and the size of bands based on the amount of std
rolling_mean_period = 50
deviations = 2

df['deviation'] = df['Adj Close'].rolling(rolling_mean_period).std()
df['RM'] = df['Adj Close'].rolling(rolling_mean_period).mean()
df['Sup_Band'] = df['RM'] + (df['deviation'] * deviations)
df['Inf_Band'] = df['RM'] - (df['deviation'] * deviations)

# Remove NAN values from df
df.dropna(axis = 0)

#Plot stock price with rolling mean and both bands 
df[['Adj Close', 'RM', 'Sup_Band', 'Inf_Band']].plot(grid=True, figsize=(20,15), linewidth = 3, fontsize=15, color=["darkblue", 'orange', 'green', 'red'])
plt.xlabel("Date", fontsize = 15)
plt.ylabel("Price", fontsize = 15)
plt.title(f'{ticker} - FinQuant', fontsize=25)
plt.legend()
plt.show()

# Building all targets
periods = 5
df.loc[:, 'Return'] = df['Adj Close'].pct_change(periods)
df.loc[:, 'Target'] = df['Return'].shift(-periods)

df = df.dropna(axis = 0)

#Creating the trade rules, whenever the Adj Close ends up Higher or Lower a band, a decision is taken
# 1 = Buy/Long, -1 = Sell/Short. This is made to follow the trend
df.loc[:, 'Rule'] = np.where(df.loc[:, 'Adj Close'] > df.loc[:, 'Sup_Band'], 1, 0)
df.loc[:, 'Rule'] = np.where(df.loc[:, 'Adj Close'] < df.loc[:, 'Inf_Band'], -1, df.loc[:,'Rule'])

df.loc[:, 'Trade'] = df.loc[:, 'Target'] * df.loc[:, 'Rule']

df.loc[:, 'Return_Trade_BB'] = df['Trade'].cumsum()

df['Return_Trade_BB'].plot(grid=True, figsize=(20,15), linewidth = 1, fontsize=15, color=["darkblue"])
plt.xlabel("Data", fontsize = 15)
plt.ylabel("Return %", fontsize = 15)
plt.title("RETURN TRADE %", fontsize=25)
plt.legend()
plt.show()