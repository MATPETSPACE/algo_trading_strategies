# -*- coding: utf-8 -*-
# pylint: disable-msg=too-many-statements
"""
@author: Karthik Iyer
"""
import numpy as np
import get_data as cr

class CryptoArb(object):
    """ Main class for backtester"""
    
    params = {
        'init_cptl': 10000,
        'frequency': 'hour', # either 'hour' or 'day'
        'limit': 300,
        'exchanges': ['Bitfinex', 'Kraken'],
        'fee': 'FEES',
        'pair': 'pair'
        }
   
    
    def __init__(self, params):
        """
        Create backtester
        params :: Backtester's settings:
            * init_cptl :: int; Base capital, default 10K
            * limit :: int; Number of historical data to collect, default 300
            * frequency :: str; Data frequency, default hourly
            * exchanges :: List of two exchange names used for the strategy, 
                           order does not matter
            * pair :: List of crypto-fiat pair to be traded; Order matters,
                      the first element in the list must be the cryptocurrency.
            * fee :: List of exchange (taker) fees in fraction; Same order 
                     as that for exchanges. For instance if an exchange fee is 
                     1 % of the trade, then fee=0.01. 
        """
        if params is not None:
            for key, value in self.params.items():
                if key in params:
                    self.params[key] = params[key]
        self.__exchange1_pnl = []
        self.__exchange2_pnl = []
        self.__trading_log = []
        self.__acc1 = 0.5*self.params['init_cptl'] # 50% of base capital in exch 1
        self.__acc2 = 0.5*self.params['init_cptl']
        self.__roi = []   
        self.__cash_ex1 = []
        self.__cash_ex2 = []
        
    def backtest(self):
        """
        Backtests the strategy on historical data and records trade statistics.
        Returns a dictionary containing pnl for accounts in both exchange, 
        cash in accounts on both exchanges, and a list of trading log.
        """

        # Get data
        if self.params['frequency'] == 'day':
            df_1 = cr.get_data(self.params['pair'], 
                               frequency='day', 
                               limit=self.params['limit'],
                               exchange=self.params['exchanges'][0])
            df_2 = cr.get_data(self.params['pair'], 
                               frequency='day', 
                               limit=self.params['limit'],
                               exchange=self.params['exchanges'][1])
        if self.params['frequency'] == 'hour':
            df_1 = cr.get_data(self.params['pair'], 
                               frequency='hour', 
                               limit=self.params['limit'],
                               exchange=self.params['exchanges'][0])
            df_2 = cr.get_data(self.params['pair'], 
                               frequency='hour', 
                               limit=self.params['limit'],
                               exchange=self.params['exchanges'][1])
        # Backtest strategy
        pos = None
        for ii in range(df_1.close.shape[0]):
            min_balance = min(self.__acc1, self.__acc2) # Trade on this capital
            if min_balance < 100: # Terminate strategy and exit the market.
                break
            
            df1_cp = float(df_1.close.iloc[ii])
            df2_cp = float(df_2.close.iloc[ii])
            diff = df1_cp - df2_cp
            
            if pos is None:
                if diff < -0.01*min(df1_cp, df2_cp):
                    # Open long
                    adjusted_df1_cp = df1_cp + df1_cp*self.params['fee'][0]
                    no_of_coins = round(min_balance/ adjusted_df1_cp, 3)
                    long_invst = no_of_coins*adjusted_df1_cp
                    
                    adjusted_df2_cp = df2_cp + df2_cp*self.params['fee'][1]
                    short_invst = no_of_coins*adjusted_df2_cp
                    
                    pos = 'Long'
                    msg = "Long position opened with " + \
                           str(no_of_coins) + " number of coins."
                    self.__trading_log.append(msg)
                    
                if diff >= 0.01*min(df1_cp, df2_cp):
                    # Open Short
                    adjusted_df2_cp = df2_cp + df2_cp*self.params['fee'][1]
                    no_of_coins = round(min_balance/ adjusted_df2_cp, 3)
                    long_invst = no_of_coins*adjusted_df2_cp
                    
                    adjusted_df1_cp = df1_cp + df1_cp*self.params['fee'][0]
                    short_invst = no_of_coins*adjusted_df1_cp
                    
                    pos = 'Short'
                    msg = "Short position opened with " + \
                           str(no_of_coins) + " number of coins."
                    self.__trading_log.append(msg)
                    
            if pos is not None:
                if pos == 'Long' and diff >= 0.01*min(df1_cp, df2_cp):
                    # Close long and update trade statstics
                    adjusted_df1_cp = df1_cp - df1_cp*self.params['fee'][0]
                    exchange1_profit = no_of_coins*adjusted_df1_cp - long_invst
                    self.__exchange1_pnl.append(exchange1_profit)
                    self.__acc1 += exchange1_profit
                    self.__acc1 = round(self.__acc1, 2)
                    self.__cash_ex1.append(self.__acc1)
                    
                    adjusted_df2_cp = df2_cp - df2_cp*self.params['fee'][1]
                    exchange2_profit = -no_of_coins*adjusted_df2_cp + \
                                       short_invst
                    self.__exchange2_pnl.append(exchange2_profit)
                    self.__acc2 += exchange2_profit
                    self.__acc2 = round(self.__acc2, 2)
                    self.__cash_ex2.append(self.__acc2)
                    
                    msg = 'Long position closed with net profit ' + \
                           '{}$'.format(exchange1_profit + exchange2_profit)
                    self.__trading_log.append(msg)
                    pos = None
                    
                if pos == 'Short' and diff <= -0.01*min(df1_cp, df2_cp):
                    # Close Short and update trade statistics
                    adjusted_df2_cp = df2_cp - df1_cp*self.params['fee'][1]
                    exchange2_profit = no_of_coins*adjusted_df2_cp - long_invst
                    self.__exchange2_pnl.append(exchange2_profit)
                    self.__acc2 += exchange2_profit
                    self.__acc2 = round(self.__acc2, 2)
                    self.__cash_ex2.append(self.__acc2)
                    
                    adjusted_df1_cp = df1_cp - df1_cp*self.params['fee'][0]
                    exchange1_profit = -no_of_coins*adjusted_df1_cp + \
                                       short_invst
                    self.__exchange1_pnl.append(exchange1_profit)
                    self.__acc1 += exchange1_profit
                    self.__acc1 = round(self.__acc1, 2)
                    self.__cash_ex1.append(self.__acc1)
                    
                    msg = 'Short position closed with net profit ' + \
                            '{}$ '.format(exchange1_profit + exchange2_profit)
                    self.__trading_log.append(msg)
                    pos = None
            
        self.__exchange1_pnl = np.array(self.__exchange1_pnl)
        self.__exchange2_pnl = np.array(self.__exchange2_pnl)
        self.__cash_ex1 = np.array(self.__cash_ex1)
        self.__cash_ex2 = np.array(self.__cash_ex2)
        
        return {'Exchange1_pnl': self.__exchange1_pnl, 
                'Exchange2_pnl': self.__exchange2_pnl,
                'Account1_cash': self.__cash_ex1,
                'Account2_cash': self.__cash_ex2,
                'Trading log': self.__trading_log
               }
