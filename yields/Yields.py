# =======================================================================================================================
# QStudio - Yields.py class
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import datetime

import matplotlib.pyplot as plt
from core.Datahub import datahub
import core.config as cfg
import numpy as np
import calendar

class Yields:
    """
    YIELDS CLASS.
    call the generate() method
    """
    overlay = False
    s = datahub()
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
