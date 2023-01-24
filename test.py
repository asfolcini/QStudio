import core.config as cfg
from core.Datahub import datahub
import matplotlib.pyplot as plt
import pandas as pd
from yields.Yields import Yields
from statsmodels.tsa.ar_model import AutoReg

print("TESTING QStudio packages")
print("-"*60)

s = datahub(loadfromconfig=True)
s.set_symbols("RACE.MI")
ys = Yields(s, False, overlay=False)
df = ys.get_yields("RACE.MI")

from statsmodels.tsa.stattools import adfuller
# Check for stationarity of the time-series data
# We will look for p-value. In case, p-value is less than 0.05, the time series
# data can said to have stationarity
df_stationarityTest = adfuller(df['Returns'], autolag='AIC')
print(df_stationarityTest)
if (df_stationarityTest[1]<0.05):
    test_pass = "PASSED"
else:
    test_pass = "FAILED"
print("P-value: ", df_stationarityTest[1], " is < 0.05 ? ==> STATIONARITY TEST ", test_pass)

# Next step is to find the order of AR model to be trained
# for this, we will plot partial autocorrelation plot to assess
# the direct effect of past data on future data
#
from statsmodels.graphics.tsaplots import plot_pacf
pacf = plot_pacf(df['Returns'], lags=21, method='ywm')

plt.show()

# Create training and test data
#
#train_data = df['Returns'][:len(df)-100]
#test_data = df['Returns'][len(df)-100:]
#
# Instantiate and fit the AR model with training data
#
#ar_model = AutoReg(train_data, lags=5).fit()
#
# Print Summary
#
#print(ar_model.summary())