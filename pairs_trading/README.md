## Pairs selection and trading

In this project, we look at the popular *pairs trading* strategy. The key idea behind pairs trading is to capitalize on market imbalances between two (or more) related assets with the expectation of making money when the inequality is corrected in the future. There are a couple of dimensions to this project that we looked at. The first is *pair selection*, where in we filter out possible candidate from a universe of stocks based on a clustering technique. We then use a statistical test to further filter out believable candidate pairs for the trading strategy. Next, we use Kalman filter to estimate the (hidden) dynamic hedge ratio between the pair of assets and use that to explicitly set in entry and exit rules. We compare this strategy with a simple buy and hold strategy (of one of the assets or some other benchmark asset). We also do a simple stress test to look at the robustness of the *logic* of the pairs trading strategy. 

**Python scripts**

*pairs_trading.py*; A python script that initializes the necessary variables and runs a back test.

*pairs_selection_pca_and_kmeans.ipynb*; An IPython notebook that walks through the pair selection process. This borrows very heavily from Jonathan Larkin’s [notebook](https://www.quantopian.com/posts/pairs-trading-with-machine-learning) on pair selection. I would like to thank Giovanni Sinapi for helping me with this part. 

Note to the reader
-----------------
Run *pairs_trading.py* within [Quantopian's](https://www.quantopian.com) IDE to generate interactive plots, back test result statistics and tear sheet. 

**Output files**

Project Report: *Report.pdf*; A write up with summary and explanation of the methods used. 

Presentation: *presentation.pdf*; A walk through of the key ideas in the report. 
