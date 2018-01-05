# -*- coding: utf-8 -*-
"""
@author: Karthik Iyer
"""
import time
import pandas as pd
import requests

def get_data(pair, frequency, limit, exchange):
        """
        Retrieves historical data from cryptocompare as a pandas dataframe with
        open, low, high, close prices and volume. Look at 
        https://www.cryptocompare.com/api/#introduction
        for information on how to get data from the API.
        
        Input parameters
        -----------------
            pair: List of crypto-fiat pair to be traded; Order matters,
                  the first element in the list must be the cryptocurrency.
                  Eg: ['LTC', 'USD'], ['BTC', EUR'] etc
            frequency: str; Data frequency.
            limit: int; Number of historical data points to collect.
            exchange: str; Name of the exchange from which data is obtained. 
                      Eg: 'Kraken', 'Coinbase', 'Bitfinex' etc
        Returns
        -------
            A pandas dataframe with open, high, low, close prices and trade
            volume.
        """
        params = {
            'fsym': pair[0],
            'tsym': pair[1],
            'limit': limit,
            'e' : exchange,
            }
        url = ''
        while url == '':
            try:
                url = requests.get('https://min-api.cryptocompare.com/data' + 
                                   '/histo' + frequency,
                                   params=params)
            except requests.exceptions.ConnectionError:
                print "Connection refused by the server"
                print "Sleeping for 5 seconds"
                time.sleep(5)
                continue
        data = url.json()['Data']
        df = pd.DataFrame(data)
        df.time = pd.to_datetime(df.time, unit='s')
        df.rename(columns={'time': 'date'}, inplace=True)
        df = df.set_index(['date'])
        return df[:-1] # Return only completed hour/ day data