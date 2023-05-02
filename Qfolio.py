import pandas as pd
import numpy as np
import pyfolio as pf
from matplotlib import pyplot as plt


## STRATEGY 1

Strategy_1_returns = pd.read_csv('./portfolio/StrategyA1_SR0.5_SKW1.csv', header=None, parse_dates=True, index_col=0)
Strategy_1_returns.columns=['Return']


#Strategy_1_returns.plot(title = 'Daily return - Strategy 1', figsize=(12, 6))

#cum_datalist1=[1+x for x in Strategy_1_returns['Return']]
#cum_datalist1=pd.DataFrame(cum_datalist1, index=Strategy_1_returns.index)
#cum_datalist1.cumprod().plot(title = 'Cumulative Daily return - Strategy 1', figsize=(12, 6))


## STRATEGY 2

Strategy_2_returns = pd.read_csv('./portfolio/StrategyA3_SR1_SKW1.csv', header=None, parse_dates=True, index_col=0)
Strategy_2_returns.columns=['Return']


#Strategy_2_returns.plot(title = 'Daily return - Strategy 2', figsize=(12, 6))

#cum_datalist2=[1+x for x in Strategy_2_returns['Return']]
#cum_datalist2=pd.DataFrame(cum_datalist2, index=Strategy_2_returns.index)
#cum_datalist2.cumprod().plot(title = 'Cumulative Daily return - Strategy 2', figsize=(12, 6))

# STRATEGY 3

Strategy_3_returns = pd.read_csv('./portfolio/StrategyB2_SR1_SKW-1.csv', header=None, parse_dates=True, index_col=0)
Strategy_3_returns.columns=['Return']



#à ALL STRATEGIES COMBINED

Strategies_A_B = pd.concat([Strategy_1_returns, Strategy_2_returns, Strategy_3_returns], axis=1, ignore_index=False)
Strategies_A_B.columns=['Strat 1', 'Strat 2', 'Strat 3']
Strategies_A_B.cumsum().plot(title = 'Daily returns', figsize=(12, 6))
#plt.show()

print(Strategies_A_B.describe())
print(Strategies_A_B.kurtosis())
print(Strategies_A_B.skew())
#Strategies_A_B.plot(kind="hist", bins=50, subplots=True, figsize=(16,10))
#plt.show()

print("Strategies Correlation (Full History)")
corr = Strategies_A_B.corr()
print(corr)

print("Strategies Correlation (last 3 months)")
corr = Strategies_A_B[-63:].corr()
print(corr)


#Strategies_A_B['Strat 1'].rolling(252).corr(Strategies_A_B['Strat 2']).plot(title='Strat 1 vs Strat 2')
#plt.show()


#pf.tears.create_returns_tear_sheet(pd.Series(Strategies_A_B['Strat 1']))
#f = pf.tears.create_returns_tear_sheet(pd.Series(Strategies_A_B['Strat 1']), return_fig=True)
#f.savefig('./output/pyfolio_returns_tear_sheet.png')

portfolio_total_return = np.sum([0.2, 0.2, 0.2] * Strategies_A_B, axis=1)
f = pf.tears.create_returns_tear_sheet(pd.Series(portfolio_total_return), return_fig=True)
f.savefig('./output/portfolio_3strat_equal.pdf')
print(portfolio_total_return.describe())