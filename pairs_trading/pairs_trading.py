# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
@author: Karthik Iyer
"""
import numpy as np
import pytz
from zipline.api import order_target, get_datetime, symbol, set_benchmark

def initialize(context):
    '''Before the start of the algorithm, zipline calls the initialize() function
       and passes in a context variable. context is a persistent namespace to 
       store variables we need to access from one algorithm iteration to the 
       next.''' 
    #context.xt = symbol('AEP')
    #context.yt = symbol('ED')
    #set_benchmark(symbol('ED'))
    
    #context.yt = symbol('OGS') # 'historical beta' = -0.06
    #context.xt = symbol('NWE') # 'historical' beta = 0.02
    #set_benchmark(symbol('NWE'))
    
    #context.xt = symbol('DRE') 
    #context.yt = symbol('AIV') 
    #set_benchmark(symbol('AIV'))
    
    context.xt = symbol('PTLA')
    context.yt = symbol('KITE')
    #set_benchmark(symbol('KITE'))
    set_benchmark(symbol('PTLA')) # default benchmark is SPY
    
    context.delta = 1e-4 # Hardcoded
    context.wt = context.delta / (1 - context.delta) * np.eye(2)
    context.vt = 1e-3 # Hardcoded

    context.theta = np.zeros(2)
    context.Ct = np.zeros((2, 2))
    context.Rt = None
    
    context.pos = None
    context.day = None
    
    #set_slippage(slippage.FixedSlippage(spread=0))
    #set_commission(commission.PerShare(cost=0.001))
    
def handle_data(context, data):    
    '''After the algorithm has been initialized, zipline calls the 
    handle_data() function once for each event. At every call, it passes the 
    same context variable and an event-frame called data containing the 
    current trading bar with open, high, low, and close (OHLC) prices as 
    well as volume for each stock in the universe'''
    
    multiple = 0.5 # Hrdcoded multiple of standard deviation.
    
    # Exectue a trade immediately after 10 am after updating the
    # Kalman filter. I'm not certain of the reason but a guess would be that
    # statistical arbitrage algorithms perform better with 
    # increasing volatility and, in general, volatility is higher around market 
    # open and market close. 
    
    exchange_time = get_datetime().astimezone(pytz.timezone('US/Eastern'))
    if exchange_time.hour == 10 and exchange_time.minute <= 10:
        # Only execute this once per day.
        if context.day is not None and context.day == exchange_time.day:
            return
        context.day = exchange_time.day
        
        # Create the observation matrix of the latest prices of xt and the 
        # intercept value (1.0) as well as the scalar value of the latest price 
        # from xt.
        Ft = np.asarray([data.current(context.xt, 'price'), 1.0]).reshape((1, 2))
        y = data.current(context.yt, 'price') 

        # The prior value of the states \theta_t is distributed as a 
        # multivariate Gaussian with mean m_{t-1} and covariance matrix R_t
        if context.Rt is not None:
            context.Rt = context.Ct + context.wt
        else:
            context.Rt = np.zeros((2, 2))
        
        # Calculate the Kalman Filter update
        # ----------------------------------
         
        # Calculate prediction of new observatio  as well as forecast error 
        # of that prediction.
        yhat = Ft.dot(context.theta)
        et = y - yhat 
        
        # Q_t is the variance of the prediction of observations and hence 
        # \sqrt{Q_t} is the standard deviation of the predictions.
        Qt = Ft.dot(context.Rt).dot(Ft.T) + context.vt 
        sqrt_Qt = np.sqrt(Qt)
        
        # The posterior value of the states \theta_t is distributed as a 
        # multivariate Gaussian with mean m_t and variance-covariance C_t
        At = context.Rt.dot(Ft.T) / Qt # A_t
        context.theta = context.theta + At.flatten()*et 
        context.Ct = context.Rt - At*Ft.dot(context.Rt) # Rt is symmetric
        
        # Place trades
        if context.pos is not None:
            if context.pos == 'long' and et > -multiple*sqrt_Qt:
                # Close long
                order_target(context.xt, 0)
                order_target(context.yt, 0)
                context.pos = None
            elif context.pos == 'short' and et < multiple*sqrt_Qt:
                # Close short
                order_target(context.xt, 0)
                order_target(context.yt, 0)
                context.pos = None
            
        if context.pos is None:
            if et < -multiple*sqrt_Qt:
                # Open long
                order_target(context.yt, 1000)
                order_target(context.xt, -1000 * context.theta[0])
                context.pos = 'long'
            elif et > multiple*sqrt_Qt:
                # Open short
                order_target(context.yt, -1000)
                order_target(context.xt, 1000 * context.theta[0])
                context.pos = 'short'
#------------------------------------------------------------------------------
'''1) symbol('symbol1')
   -----------------

    Convenience method that accepts a string literal to look up a security by 
    its symbol. A dynamic variable cannot be passed as a parameter. Within the 
    Quantopian IDE, an inline search box appears showing you matches on 
    security id, symbol, and company name.

    Parameters
    'symbol1': The string symbol of a security.

    Returns
    A security object.

    2) initialize(context)
    ------------------

    Called once at the very beginning of a backtest. Our algorithm can use 
    this method to set up any bookkeeping that we'd like. The context object 
    will be passed to all the other methods in our algorithm.

    Parameters
    context: An initialized and empty Python dictionary. The dictionary has 
    been augmented so that properties can be accessed using dot notation as 
    well as the traditional bracket notation.

    Returns
    None
    
    3) handle_data(context, data)
    --------------------------

    Called every minute.

    Parameters
    context: Same context object in initialize, stores any state you've 
    defined, and stores portfolio object.

    data: An object that provides methods to get price and volume data, check 
    whether a security exists, and check the last time a security traded.

    Returns
    None
    
    4) order_target(asset, amount, style=OrderType)
    -----------------------------------------------
    
    Places an order to adjust a position to a target number of shares. If there 
    is no existing position in the asset, an order is placed for the full 
    target number. If there is a position in the asset, an order is placed for 
    the difference between the target number of shares or contracts and the 
    number currently held. Placing a negative target order will result in a 
    short position equal to the negative number specified.

    Example
    If the current portfolio has 5 shares of AAPL and the target is 20 shares, 
    order_target(symbol('AAPL'), 20) orders 15 more shares of AAPL.

    Parameters
    asset: An Equity object or a Future object.

    amount: The integer amount of target shares or contracts. Positive means 
    buy, negative means sell.

    OrderType: (optional) Specifies the order style and the default is a market
    order. The available order styles are:

        style=MarketOrder(exchange)
        style=StopOrder(stop_price, exchange)
        style=LimitOrder(limit_price, exchange)
        style=StopLimitOrder(limit_price=price1, stop_price=price2, exchange)
        Click here to view an example for exchange routing.

    Returns
    An order id, or None if there is no difference between the target position 
    and current position.

    5) Slippage must be defined in the initialize method. It has no effect 
    if defined elsewhere in the algorithm. If we do not specify a slippage 
    method, slippage defaults to 
    VolumeShareSlippage(volume_limit=0.025, price_impact=0.1) 
    (we can take up to 2.5% of a minute's trade volume).
    
    6) To set the cost of our trades, use the set_commission method and pass 
    in PerShare or PerTrade. Like the slippage model, set_commission must be 
    used in the initialize method and has no effect if used elsewhere in the 
    algorithm. If we don't specify a commission, our backtest defaults to 
    $0.001 per share with a $1 minimum cost per trade.
    
    7) Stress Test
    --------------
    As a check for the robustness of the logic behind the trading strategy,
    do the exact opposite of what the strategy tells you to do. The 
    resultant performace must be worse. In our case, that means
    changing all the < signs to > and vice versa.
'''