# Karthik Iyer

# Back testing RSI in quantstrat
----------------


rm(list = ls())
library(quantmod)
library(quantstrat)
library(TTR)
library(lattice)
library(gridExtra) 

#Initial set up and variables initialization

Sys.setenv(TZ = "UTC")
currency("USD")
initDate <- "2004-09-30"
startDate <- "2004-10-01"
endDate <- "2017-05-26"
initEq <- 0
adjustment <- TRUE
.nShs <- 1000
#stopLoss <- 0.02 #~2% from experimentation and MAE plot, for question 2

symbols <- "VNQ"
stock(symbols, currency = "USD", multiplier = 1)
options("getSymbols.yahoo.warning" = FALSE)
getSymbols(Symbols=symbols,
           src = "yahoo",
           index.class = "POSIXct",
           from = startDate, 
           to = endDate, 
           adjust = adjustment)
strat.st <- "rsi"
portfolio.st <- "rsi"
account.st <- "rsi"
.n <- 14 
.maType <-"SMA"

#.rsiOb <-75 #These values are what we get after optimizing. Used in part d) & e)
#.rsiOs <-40 #These values are what we get after optimizing. Used in part d) & e)

#.rsiOb <-50 #These values are the "comparison" pair. Used in part d)
#.rsiOs <-40 #These values are the "comparison" pair. Used in part d)

.rsiOb <- 60  #For part a) and b)
.rsiOs <- 40  #For part a) and b)

#.rsiObrange<-seq(50,75,by=5) #for part c) and f)
#.rsiOsrange<-seq(20,40,by=5) #for part c) and f)

#.rsiObrange<-seq(35,75,by=5) #for part c) after looking at first heat map
#.rsiOsrange<-seq(30,40,by=5) #for part c) after looking at first heat map


#Remove previously created portfolio and account objects
rm.strat(portfolio.st)
rm.strat(account.st)

#Now we initialize our portfolio, account and orders. 
#We will also store our strategy to save for later.

initPortf(name = portfolio.st,
          symbols = symbols,
          initDate = initDate)

initAcct(name = account.st,
         portfolios = portfolio.st,
         initDate = initDate,
         initEq = initEq)

initOrders(portfolio = portfolio.st,
           symbols = symbols,
           initDate = initDate)

strategy(strat.st, store = TRUE)

#----------------------------
#3 Steps for Strategy set up
#----------------------------

#STEP 1: Add INDICATORS
add.indicator(strategy = strat.st,
              name = "RSI",
              arguments = list(price = quote(Cl(mktdata)), 
                               n = .n,
                               maType=.maType),
              label = "rsi_indicator")

#STEP 2: ADD SIGNALS
add.signal(strategy = strat.st,
           name = "sigThreshold",
           arguments = list(column = "rsi_indicator",
                          relationship = "lte",
                          threshold = .rsiOs,
                          cross = TRUE),
           label = "rsisignal.lte.rsiOs")

add.signal(strategy = strat.st,
           name = "sigThreshold",
           arguments = list(column = "rsi_indicator",
                          relationship = "gt",
                          threshold = .rsiOb,
                          cross = TRUE),
           label = "rsisignal.gt.rsiOb")


#STEP 3: ADD RULES

#ENTRY RULE
add.rule(strategy = strat.st,
         name = "ruleSignal",
         arguments = list(sigcol = "rsisignal.lte.rsiOs",
                          sigval = TRUE,
                          orderqty = .nShs,
                          ordertype = "market",
                          orderside = "long", 
                          TxnFees = 0, 
                          replace = FALSE),
         type = "enter",
         path.dep = TRUE,
         label = "EnterLONG")

#EXIT RULE 

#This closes out all long positions (orderside, orderqty). 
#This order will replace (replace) any open orders.
add.rule(strat.st, 
         name = "ruleSignal", 
         arguments = list(sigcol = "rsisignal.gt.rsiOb", 
                          sigval = TRUE, 
                          orderqty = "all", 
                          ordertype = "market", 
                          orderside = "long", 
                          TxnFees = 0, 
                          replace = TRUE), 
         type = "exit", 
         path.dep = TRUE,
         label = "ExitLONG")

#STOP LOSS RULE

# Now, set up a "child" rule that will trigger the stop-loss.
#add.rule(strategy = strat.st, 
#name ='ruleSignal',
#arguments = list(sigcol="rsisignal.lte.rsiOs", 
#sigval = TRUE, 
#replace = FALSE,
#orderside ='long', 
#ordertype ='stoplimit', 
#tmult = TRUE, 
#threshold = quote(stopLoss),
#orderqty = 'all'),
#type ='chain', 
#parent = 'EnterLONG', 
#label = 'StopLossLong', 
#enabled = FALSE)



#For part c) and f)

add.distribution(strat.st,
                 paramset.label = "OPT_RSI",
                 component.type = "signal",
                 component.label = "rsisignal.lte.rsiOs",
                 variable = list(threshold = .rsiOsrange),
                 label = "Oversold_range")

add.distribution(strat.st,
                 paramset.label = "OPT_RSI",
                 component.type = "signal",
                 component.label = "rsisignal.gt.rsiOb",
                 variable = list(threshold = .rsiObrange),
                 label = "Overbought_range")

# Switch stop-loss rule on/off by activating this 
# enable.rule(.) command (see rule setting above).
# It is associated with the rule label "StopLossLong".

#enable.rule(strategy = strat.st, 
#type = "chain",
#label = 'StopLossLong')

#---------------------
#RUN THE STRATEGY
#----------------------

results <- applyStrategy(strat.st, portfolios = portfolio.st)

#For part (c))
results <- apply.paramset(strategy.st = strat.st,
                          paramset.label = "OPT_RSI",
                          portfolio.st = portfolio.st,
                          account.st = account.st,
                          nsamples = 0)

updatePortf(Portfolio = portfolio.st)
updateAcct(name = account.st)
updateEndEq(Account = account.st)

#chart.Posn(Portfolio = portfolio.st, 
#symbol = symbols, 
#TA="add_RSI(n =.n, maType = .maType, wilder = F)")

chart.ME(Portfolio = portfolio.st, 
         Symbol = symbols, 
         type = 'MAE', 
         scale = 'percent')

tstats <- tradeStats(Portfolios = portfolio.st)
tstats[c("Net.Trading.PL",  "Max.Drawdown","Profit.To.Max.Draw","Ann.Sharpe")]

z <- tapply(X = results$tradeStats$Profit.To.Max.Draw,
            INDEX = list(results$tradeStats$Oversold_range, results$tradeStats$Overbought_range),
            FUN=mean)

x <- as.numeric(rownames(z))
y <- as.numeric(colnames(z))

filled.contour(x = x, y = y, z = z, color = heat.colors,
               xlab = "Oversold_range values", ylab = "OVerbought_range values")
myTitle <- paste0("Profit/MaxDrawdown: ", symbols)
title(myTitle)
#-----------------------------------------------------------
#Part (e)

#bbsimRep <- mcsim(Portfolio = portfolio.st, 
                   #Account = account.st, 
                   #n = 1000,
                   #replacement = TRUE,
                   #use = 'txns')

#quantile(bbsimRep, normalize = F)
#summary(bbsimRep,normalize = F)
#plot(bbsimRep, normalize = F) 
#hist(bbsimRep, normalize = FALSE)
#--------------------------------------------------------------

#Part (f)

# One can change nsamples to a number less than the total 
# number of possible combinations among the distributions to 
# speed it up while testing code. nsamples = 0  will run through all 
# the combinations:

results <- walk.forward(strategy.st = strat.st,
                        paramset.label ='OPT_RSI',
                        portfolio.st = "rsi",
                        account.st = "rsi",
                        period ='years',
                        k.training = 4,
                        k.testing = 1,
                        nsamples = 0,
                        #nsamples=5,
                        audit.prefix = 'wfa',
                        anchored = FALSE,
                        verbose = TRUE
#)
#tstats <- t(tradeStats(Portfolios = portfolio.st))
#tstats[c("Net.Trading.PL",  "Max.Drawdown","Profit.To.Max.Draw","Ann.Sharpe")]
#chart.forward("wfa.results.RData")
