# -*- coding: utf-8 -*-
"""
@author: Karthik Iyer
"""
import backtest as bt
import matplotlib.pyplot as plt
plt.style.use('seaborn')

if __name__ == "__main__":  
    params = {
        'init_cptl': 10000,
        'frequency': 'hour',
        'limit': 2160, # 3 months
        'exchanges': ['Bitfinex', 'Kraken'],
        'fee': [0.0025, 0.0025], 
        'pair': ['BTC', 'USD']
        }
#    params = {
#        'init_cptl': 10000,
#        'frequency': 'hour',
#        'limit': 2160, # 3 months
#        'exchanges': ['Bitfinex', 'Kraken'],
#        'fee': [0.0025, 0.0025],
#        'pair': ['ETH', 'USD']
#        }
#    params = {
#        'init_cptl': 10000,
#        'frequency': 'hour',
#        'limit': 2160, # 3 months
#        'exchanges': ['Bitfinex', 'Kraken'],
#        'fee': [0.0025, 0.0025],
#        'pair': ['LTC', 'USD']
#        }
    trade_stats = bt.CryptoArb(params=params).backtest()
    #----------
    # Plot PnL
    #----------
    
#    plt.subplot(2, 3, 1)
#    plt.plot(trade_stats['Exchange1_pnl'])
#    plt.title('Bitifinex PnL')
#    plt.xlabel('Trade number')
#    plt.ylabel('USD')
#    plt.grid()
#    
#    plt.subplot(2, 3, 2)
#    plt.plot(trade_stats['Exchange2_pnl'])
#    plt.title('Kraken PnL')
#    plt.xlabel('Trade number')
#    plt.ylabel('USD')
#    plt.grid()
#    
#    
#    plt.subplot(2, 3, 3)
#    plt.plot(trade_stats['Exchange2_pnl'] + trade_stats['Exchange1_pnl'])
#    plt.title('Total PnL')
#    plt.xlabel('Trade number')
#    plt.ylabel('USD')
#    plt.grid()
#    
#    --------------------
    # Plot equity curves
    #---------------------
    
    plt.subplot(2, 3, 1)
    plt.plot(trade_stats['Account1_cash'])
    plt.title('Cash in Bitfinex account')
    plt.xlabel('Trade number')
    plt.ylabel('USD')
    plt.grid()
    
    plt.subplot(2, 3, 2)
    plt.plot(trade_stats['Account2_cash'])
    plt.title('Cash in Kraken account')
    plt.xlabel('Trade number')
    plt.ylabel('USD')
    plt.grid()
    
    plt.subplot(2, 3, 3)
    plt.plot(trade_stats['Account1_cash'] + trade_stats['Account2_cash'])
    plt.title('Equity curve')
    plt.xlabel('Trade number')
    plt.ylabel('USD')
    plt.grid()
    
    plt.tight_layout()
    