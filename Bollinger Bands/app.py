# importing all the libraries used to run the code
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Do not show warning at the terminal while running this code
pd.options.mode.chained_assignment = None

#Defining the initial parameters to download the asset info from YFinance
dict_parameters = {}
dict_parameters['ticker'] = "^BVSP"
dict_parameters['start_date'] = "2015-01-01"
dict_parameters['end_date'] = datetime.today().strftime('%Y-%m-%d')

dict_parameters['rolling_mean_period'] = 10
dict_parameters['deviations'] = 2

dict_parameters['target'] = 5

def df_gen(ticker, start_date, end_date, rolling_mean_period, deviations, target):

    df = yf.download(ticker, start = start_date, end = end_date)

    df['deviation'] = df['Adj Close'].rolling(rolling_mean_period).std()
    df['RM'] = df['Adj Close'].rolling(rolling_mean_period).mean()
    df['Sup_Band'] = df['RM'] + (df['deviation'] * deviations)
    df['Inf_Band'] = df['RM'] - (df['deviation'] * deviations)

    df.dropna(axis = 0)

    # Building all targets
    df.loc[:, 'Return'] = df['Adj Close'].pct_change(target)
    df.loc[:, 'Target'] = df['Return'].shift(-target)

    df = df.dropna(axis = 0)

    #Creating the trade rules, whenever the Adj Close ends up Higher or Lower a band, a decision is taken
    # 1 = Buy/Long, -1 = Sell/Short. This is made to follow the trend
    df.loc[:, 'Rule'] = np.where(df.loc[:, 'Adj Close'] > df.loc[:, 'Sup_Band'], 1, 0)
    df.loc[:, 'Rule'] = np.where(df.loc[:, 'Adj Close'] < df.loc[:, 'Inf_Band'], -1, df.loc[:,'Rule'])

    df.loc[:, 'Trade'] = df.loc[:, 'Target'] * df.loc[:, 'Rule']

    df.loc[:, 'Return_Trade_BB'] = df['Trade'].cumsum()

    return df

def bollinger_graph_generator(df, ticker):
    # Plot stock price with rolling mean and both bands 
    df[['Adj Close', 'RM', 'Sup_Band', 'Inf_Band']].plot(grid=True, figsize=(20,15), linewidth = 1, fontsize=15, color=["darkblue", 'orange', 'green', 'red'])
    plt.xlabel("Date", fontsize = 15)
    plt.ylabel("Price", fontsize = 15)
    plt.title(f'{ticker} - FinQuant', fontsize=25)
    plt.legend()
    plt.show()

def performance_graph_generator(df):
    df['Return_Trade_BB'].plot(grid=True, figsize=(20,15), linewidth = 1, fontsize=15, color=["darkblue"])
    plt.xlabel("Data", fontsize = 15)
    plt.ylabel("Return %", fontsize = 15)
    plt.title("RETURN TRADE %", fontsize=25)
    plt.legend()
    plt.show()

def change_settings(dict_parameters):
    print(f'Current Settings: ticker: {dict_parameters['ticker']} \n',  
        f'start_date: {dict_parameters['start_date']} \n',
        f'end_date: {dict_parameters['end_date']}\n',
        f'rolling_mean_period: {dict_parameters['rolling_mean_period']}\n',
        f'deviations: {dict_parameters['deviations']}\n'
        f'target: {dict_parameters['target']}\n'
    )
    selected_change = input("Which parameter will be setted?")
    new_value = input("Type new value: ")
    try:
        new_value = int(new_value)
        dict_parameters[selected_change] = new_value
        print(type(dict_parameters[selected_change]))
    except:
        dict_parameters[selected_change] = new_value
    
    return dict_parameters

while True:
    print('Menu - Choose Option\n'
          '1 - Change Settings\n'
          '2 - Bollinger Graph\n'
          '3 - Performance Graph\n'
          '4 - Quit')
    
    option = int(input('Selected Option: '))

    if option == 1:
        dict_parameters = change_settings(dict_parameters)
        continue
        
    if option == 4:
        break
        
    df = df_gen(dict_parameters['ticker'],
                dict_parameters['start_date'],
                dict_parameters['end_date'],
                dict_parameters['rolling_mean_period'],
                dict_parameters['deviations'],
                dict_parameters['target'])

    if option == 2:    
        bollinger_graph_generator(df, dict_parameters['ticker'])
    elif option == 3:
        performance_graph_generator(df)
    else:
        print('No valid option selected!')


