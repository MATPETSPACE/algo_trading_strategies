# Back testing a trading strategy

The goal of this project is to back test a quantitative trading strategy. We use the R package  *quantstrat* for back testing. We work with a widely used indicator, Relative Strength Index, or [RSI.](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/RSI) The relative strength index (RSI) is most commonly used to indicate temporary overbought or oversold conditions in a market. A disadvantage of the RSI is that sudden, sharp price movements results in rapid change in the indicators and, thus, it is prone to giving false signals. 

The strategy works as follows: When the RSI value signals overselling, one enters the market. A typical setting for this signal is 30\%. When the RSI signals overbuying, eg 70\%, this is a signal to exit the market. RSI is one of the more popular *momentum* indicators. If a trader wants to use a momentum-based strategy, she takes a long position in a stock or asset that has been trending up. If the stock is trending down, she takes a short position. Instead of the traditional philosophy of trading – buy low, sell high – momentum investing seeks to sell low and buy lower, or buy high and sell higher. When the RSI is above 70 (or some other appropriately set limit), it means the market is overbought and likely due for a correction. When the RSI is below 30 (or some other appropriately set limit), the market is getting oversold and might be due for a rally. 

In this project, we set up the strategy, run it, re-run it after optimizing the signal parameters and perform a walk forward analysis (a validation technique). We compare the efficiency of the strategy by looking at various performance measures.


Acknowledgements
----------------------

I woud like to thank Daniel Hanson for teaching me the fundamentals of electronic trading and how to test various trading strategies using  *quantstrat*. This is a project that I undertook to understand how to programmatically back test a given trading strategy.

Sources
---------
[Quantstrat](https://www.rdocumentation.org/packages/quantstrat/versions/0.8.2)<br>
[Explaining RSI](https://www.thebalance.com/trading-commodities-with-rsi-and-momentum-indicators-809349)<br>
[Back Testing strategies in R](https://timtrice.github.io/backtesting-strategies/) (This is an excellent exposition for beginners!)
