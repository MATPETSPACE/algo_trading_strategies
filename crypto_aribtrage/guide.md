## Python Scripts

*get_data.py* : Returns a *pandas* dataframe by calling an exchange's API. The dataframe comprises of OHLC prices, volume and timestamp
of a specified crypto-currency from a specified exchange. 

*back_test.py* : Backtests the strategy and returns trade statistics (after taking fees and commission in to account.)

*main.py* : Main file that calls the backtest function and plots some trade statistics. (Play around with this with different currencies 
and exchanges and compare the results!)

*mail_alert.py:* This script sends an e-mail alert every time a trading signal is received. 
