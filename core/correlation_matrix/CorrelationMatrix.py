# =======================================================================================================================
# QStudio - correlation_matrix.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from core.Datahub import Datahub
import core.config as cfg



class CorrelationMatrix:
    """
    CORRELATION MATRIX CLASS, using pearson method.
    call the generate() method
    """

    s = Datahub()
    show_chart = True
    """
    INIT
    """

    def __init__(self, _s, show=True):
        self.s = _s
        self.show_chart = show

    def generate(self, periods=90):
        """
        GENERATE CORRELATION MATRIX based on the last N periods, by default periods=90
        """
        symbols = []

        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            r['Symbol'] = s
            symbols.append(r)
        df = pd.concat(symbols)
        df = df.reset_index()
        df = df[['Date', 'Close', 'Symbol']]

        df_pivot = df.pivot('Date', 'Symbol', 'Close').reset_index()

        corr_df = df_pivot.corr(method='pearson')
        corr_df.head().reset_index()

        plt.figure(figsize=(13, 8))
        seaborn.heatmap(corr_df, annot=True, cmap='RdYlGn')
        plt.title("Correlation Matrix (last "+str(periods)+" periods)")
        if self.show_chart:
            plt.show()
        else:
            plt.savefig(cfg.OUTPUT_REPOSITORY+"CorrelationMatrix_"+cfg.OUTPUT_FILENAME)
