# =======================================================================================================================
# QStudio - Yields.py class
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import math
import matplotlib.pyplot as plt
import pandas as pd

from core.Datahub import Datahub
import core.config as cfg
import numpy as np

class Yields:
    """
    YIELDS CLASS.
    call the generate() method
    """
    overlay = False
    s = Datahub()
    show_chart = True
    """
    INIT
    """

    def __init__(self, _s, show=True, overlay=False):
        self.s = _s
        self.show_chart = show
        self.overlay = overlay

    def generate(self, periods=90):
        """
        GENERATE YIELD CHART based on the last N periods, by default periods=90
        """

        fsize = figsize=(16,4)
        if len(self.s.get_symbols()) == 1 or self.overlay:
            figure, axis = plt.subplots(figsize=fsize)
        else:
            figure, axis = plt.subplots(len(self.s.get_symbols()), sharex=True, figsize=fsize)

        i = 0
        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            r['Symbol'] = s
            r['Returns'] = ((r['Close']/r['Close'].shift(1)) -1)*100
            r.dropna(inplace = True)
            ss = len(self.s.get_symbols())
            volatility = r['Returns'].std()
            print(str(s) + " volatility("+str(periods)+")="+str(volatility))
            if ss == 1 or self.overlay:
                axis.grid(True, linestyle='-.')
                axis.set_title('Yields')
                if ss == 1:
                    colorformat = np.where(r['Returns']>=0, 'g','r')
                    axis.bar(r['Date'], r['Returns'], label=str(s), color=colorformat)
                else:
                    axis.plot(r['Date'], r['Returns'], label=str(s), linestyle='-')
                axis.legend(loc="upper left")
            else:
                axis[i].grid(True, linestyle='-.')
                axis[i].set_title(str(s))
                colorformat = np.where(r['Returns']>=0, 'g','r')
                axis[i].bar(r['Date'], r['Returns'], color=colorformat)
            i = i + 1

        figure.tight_layout()
        if self.show_chart:
            plt.show()
        else:
            plt.savefig(cfg.OUTPUT_REPOSITORY+"Yields_"+cfg.OUTPUT_FILENAME)


    def get_volatility(self, periods=999999999):
        """
        COMPUTE VOLATILITY
        """
        print("VOLATILITY REPORT (Periods =", str(periods), ")")
        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            r['Symbol'] = s
            r['Returns'] = ((r['Close']/r['Close'].shift(1)) -1)*100
            r.dropna(inplace = True)
            daily = r['Returns'].std()
            monthly = math.sqrt(21) * r['Returns'].std()
            annually = math.sqrt(252) * r['Returns'].std()
            print(str(s)+' Daily = {:.2f}%'.format(daily), ' Monthly = {:.2f}%'.format(monthly), ' Annually = {:.2f}%'.format(annually))

    def get_yields(self,_symbol):
        r = self.s.load_data(_symbol)
        r['Symbol'] = _symbol
        r['Returns'] = ((r['Close']/r['Close'].shift(1)) -1)*100
        r.dropna(inplace = True)
        return r

    def generate_week(self, periods=90):
        """
          GENERATE YIELD CHART GROUP BY WEEK DAYS based on the last N periods, by default periods=90
          """
        fsize = figsize=(6,4)
        if len(self.s.get_symbols()) == 1 or self.overlay:
            figure, axis = plt.subplots(figsize=fsize)
        else:
            figure, axis = plt.subplots(len(self.s.get_symbols()), sharex=True, figsize=fsize)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        i = 0
        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            r['Symbol'] = s
            r['Returns'] = ((r['Close']/r['Close'].shift(1)) -1)*100
            r['day'] = r['Date'].dt.weekday
            week_df = r[['day', 'Returns']].groupby(['day'], sort=False).mean().sort_index()
            week_df['x'] = week_df.index
            for d in week_df['x']:
                week_df['x'][d] = days[d]
            r.dropna(inplace = True)
            ss = len(self.s.get_symbols())
            if ss == 1:
                axis.grid(True, linestyle='-.')
                axis.set_title('Weekdays yields '+str(s)+"(last "+str(periods)+" periods)")
                colorformat = np.where(week_df['Returns']>=0, 'g','r')
                axis.bar(week_df['x'], week_df['Returns'], color=colorformat)
            else:
                axis[i].grid(True, linestyle='-.')
                axis[i].set_title(str(s))
                colorformat = np.where(r['Returns']>=0, 'g','r')
                axis[i].bar(week_df['x'], week_df['Returns'], color=colorformat)
            i = i + 1

        figure.tight_layout()
        if self.show_chart:
            plt.show()
        else:
            plt.savefig(cfg.OUTPUT_REPOSITORY+"Yields_"+cfg.OUTPUT_FILENAME)

    def generate_month(self, periods=9999):
        """
          GENERATE YIELD CHART GROUP BY MONTH based on the last N periods, by default periods=90
          """
        fsize = figsize=(6,4)
        if len(self.s.get_symbols()) == 1 or self.overlay:
            figure, axis = plt.subplots(figsize=fsize)
        else:
            figure, axis = plt.subplots(len(self.s.get_symbols()), sharex=True, figsize=fsize)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        i = 0
        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            r['Symbol'] = s
            r['Returns'] = ((r['Close']/r['Close'].shift(1)) -1)*100
            r['month'] = pd.DatetimeIndex(r['Date']).month
            month_df = r[['month', 'Returns']].groupby(['month'], sort=False).mean().sort_index()
            month_df['x'] = month_df.index
            for m in month_df['x']:
                month_df['x'][m] = months[m-1]
            r.dropna(inplace = True)

            ss = len(self.s.get_symbols())
            if ss == 1:
                axis.grid(True, linestyle='-.')
                axis.set_title('Monthly yields '+str(s)+"(last "+str(periods)+" periods)")
                colorformat = np.where(month_df['Returns']>=0, 'g','r')
                axis.bar(month_df['x'], month_df['Returns'], color=colorformat)
            else:
                axis[i].grid(True, linestyle='-.')
                axis[i].set_title(str(s))
                colorformat = np.where(month_df['Returns']>=0, 'g','r')
                axis[i].bar(month_df['x'], month_df['Returns'], color=colorformat)
            i = i + 1

        figure.tight_layout()
        if self.show_chart:
            plt.show()
        else:
            plt.savefig(cfg.OUTPUT_REPOSITORY+"Yields_"+cfg.OUTPUT_FILENAME)

    def autocorrelation(self):

        for s in self.s.get_symbols():
            df = self.get_yields(s)

            from statsmodels.tsa.stattools import adfuller
            # Check for stationarity of the time-series data
            # We will look for p-value. In case, p-value is less than 0.05, the time series
            # data can said to have stationarity
            df_stationarityTest = adfuller(df['Returns'], autolag='AIC')
            if (df_stationarityTest[1]<0.05):
               test_pass = "PASSED"
            else:
               test_pass = "FAILED"
            print("P-value: ", df_stationarityTest[1], " is < 0.05 ? ==> STATIONARITY TEST ", test_pass)

            # Next step is to find the order of AR model to be trained
            # for this, we will plot partial autocorrelation plot to assess
            # the direct effect of past data on future data
            from statsmodels.graphics.tsaplots import plot_pacf
            pacf = plot_pacf(df['Returns'], lags=21, method='ywm')
            plt.title('Autocorrelation '+s+' (last 21 periods)')
            if not self.show_chart:
                plt.savefig(cfg.OUTPUT_REPOSITORY+"Autocorrelation_"+s.replace(".", "")+"_"+cfg.OUTPUT_FILENAME)

        if self.show_chart:
            plt.show()

        return