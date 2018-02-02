## Arbitrage in cryptocurrency markets
The goal of this project is to back-test a simple long-short trading strategy on cryptocurrencies. 

### Idea
Cryptocurrency markets are relatively new and still inefficient. There are dozens of cryptocurrency exchanges around the world and 
often there is a (relatively significant) price (bid-ask) difference from one exchange to another. The purpose of this project is 
to capitalize on this price inefficiency between 2 exchanges and develop a market-neutral strategy.

Here is the basic strategy. 

1.	Look at the last-traded price of a cryptocurrency at two different exchanges. 

2.	If there is a significant spread in the prices, then buy (go long) the undervalued exchange and short sell the over-valued exchange.                                                                                                                                                           

3.	When the spread closes, exit the market by selling the previously undervalued exchange and buying back the previously 
overvalued exchange. 

Let us define a few terms and consider a toy example to understand the logic of the strategy. 

Let us call one of the exchanges as *exchange1* and the other as *exchange2* and keep their order fixed throughout. 
(It does not matter which of the two exchanges we choose as *exchange1*; but the choice of the two exchanges matters. 
We will come back to the choice of exchanges later.)
Consider a cryptocurrency, call it *cry* that is offered at both the exchanges. *Assume that both the exchanges allow short-selling*. 
Suppose the last traded price of *cry* at *exchange1* is significantly lower than at *exchange2*. 
(Significantly is admittedly a subjective term. For our purposes, let us assume that there is at least a 1% price difference so 
that on closing the trade and paying transaction fees (which are much lower than 1%), we are left with some profit.) We then 
*simultaneously* buy some amount of coins at *exchange1* and *short sell* equal amount of coins at *exchange2*. 
We call this as *longing the spread*.

Now suppose at a later time, the last traded price of *cry* at *exchange1* is more than 
that at *exchange2*, then sell the previously *exchange1* bought coins and buy back *exchange2* coins, closing the 
*longing of spread* and exiting the market.

The exact opposite logic applies if currently, last traded price of *cry* at *exchange1* is significantly higher than at *exchange2*. 
In that case, we will enter the market by *shorting the spread* (buy some amount of coins at *exchange2* and simultaneously 
short sell equal amount of coins at *exchange1*.) At a later date, we will exit the market by closing the *shorting of spread.* 

### Toy example. 

Suppose, the last-traded price of *cry* at *exchange1* is currently $600 and that at *exchange2* is $610. 
There is more than 1% price difference and we get a signal to *long the spread* and enter the market. 
(Let us assume that we only deal with 1 coin at the moment. If we are dealing with many coins, that would make 
no difference to the strategy mathematically.  However, trading many coins will potentially cause *slippage* and can eat 
in to the profits. It is thus important to choose order sizes and exchanges where in slippage possibilities is minimized.

There are 3 mutually exhaustive and exclusive possibilities that would give us an exit signal. 

1.	The (last traded) price of *cry* increases at *exchange1* to USD 630 and that at *exchange2* decreases to  USD 605. 
In this case, we would make (assuming no transaction fees) a profit of  USD 30 on the long and  USD 5 on the short with an 
overall profit of  USD 35. 

2.	The price of *cry* increases at *exchange1* to  USD 630 and that at *exchange2* increases to  USD 620. 
Again, assuming there are no transaction fees, we would make a profit of  USD 20 on the long and a loss of  USD 10 on 
the short with an overall profit of  USD 10. 

3.	The price of *cry* decreases at *exchange1* to  USD 590 and that at *exchange2* decreases to  USD 580. 
Again, assuming there are no transaction fees, we would make a profit of  USD 30 on the short and a loss of  USD 10 on the 
long with an overall profit of  USD 20.

Thus, if we are long the spread, we get an exit signal only if one the following three situations arise. 
Price at *exchange1* increases and price at *exchange2* decreases, price at both the exchanges increases or 
price at both the exchanges decreases. Note that the fourth possibility where in the price at *exchange1* decreases 
and the price at *exchange2* also decreases will only widen the spread and not trigger an exit signal. 
Thus, in all 3 possible cases, we end up with a theoretical profit. 

Similar logic applies if we enter the market by *shorting the spread.*

### Advantages

Note that we don’t sell but actually short sell cry on the short exchange. This offers two important advantages:

•	The strategy is always market-neutral: *cry’s* market's moves (up or down) don't impact the strategy returns. 
This removes a big risk from the strategy. The *cry* market could suddenly lose a lot of its value and this won't make
any difference in the strategy returns.

•	The strategy doesn't need to transfer funds (USD or *cry*) between the exchanges. 
The buy/sell and sell/buy trading activities are done in parallel on two different exchanges, independently. 
Advantage: no need to deal with transfer latency issues.

### Pitfalls

A few possibilities can make a winning trade in to a losing one. 

•	There is not enough liquidity. 

*Possible solution:* Choose exchanges with large number of users and currencies which are heavily traded so that there 
is always someone on the other side to your position. 
For our purpose, we choose *Bitfinex* and *Kraken* as our exchanges. 
Both of these exchanges allow short selling. 

•	Fees and commission eating in to profits. 

*Possible solution:* Have more restrictive entry and exit points resulting in fewer trades. 
In our case, we demand at least 1% price difference so that after fees and commission, we are still profitable. 
Note that the fee gets taken twice for each trade because it happens for each exchange. 

•	Orders not getting filled at the desired price. 

*Possible solution:* Have a small capital and deal with only small-ish orders. 
Slippage can thus be potentially avoided. 

•	Prices not reversing direction. 

*Possible solution:* Cut your losses short and exit the market. 

### Best currencies to use?

Since this strategy gets its trade signals from volatility, perhaps newer currencies would be a good choice. Be careful with newer currencies as there might not be enough liquidity. 
Bitcoin is the most well-known and the biggest (by market capitalization) currency. It is currently much more volatile than any other currency, making it a prime candidate for arbitrage. 
Our strategy takes in to account all pitfalls and sets up more robust entry and exit signals.

## Disclaimer

I am not responsible for any loss you sustain. Be careful. This is crypto. Anything can happen.





      
