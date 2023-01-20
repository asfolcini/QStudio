import core.config as cfg
from core.Datahub import datahub
import matplotlib.pyplot as plt
import calendar

print("TESTING QStudio packages")
print("-"*60)

# symbols_list loaded from path config/symbols
s = datahub(loadfromconfig=False)
ds = s.load_data("G.MI",252)
print("LEN=",len(ds))
#print(ds.head(5))
#print(ds.tail(5))
#print(ds)



ds['Returns'] = ((ds['Close']/ds['Close'].shift(1)) -1)*100
ds.dropna(inplace = True)
#print(ds.tail(10))

#df_data = pd.read_csv('data.csv', parse_dates=['Date'])
week_df = ds.groupby(ds['Date'].dt.weekday).mean()
print(week_df)

week_df.plot.bar(title="Yields by Day of the week (last "+str(252)+" periods)", rot= 0, y = 'Returns', alpha=0.5)
#plt.hist(week_df['Returns'], 50, density=True, facecolor='g', alpha=0.75)

#ds.plot(title='Rendimenti G.MI', x = 'Date', y='Returns')
#ds['Date','Returns'].plot(title='S&P 500 daily returns')
plt.show()




#daily_return = ds['Close'].pct_change(1) # 1 for ONE DAY lookback
#monthly_return = ds['Close'].pct_change(21) # 21 for ONE MONTH lookback
#annual_return = ds['Close'].pct_change(252) # 252 for ONE YEAR lookback
