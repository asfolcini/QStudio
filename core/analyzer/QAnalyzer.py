import pandas as pd
from matplotlib import pyplot as plt
from prettytable import PrettyTable
import core.config as cfg

class Analyzer(object):

    def __init__(self, df):
        self.df = df
        self.__calc()

    def __calc(self):
        self.df['cumpnl'] = self.df['pnl'].cumsum().round(2)

        self.df['highvalue'] = self.df['cumpnl'].cummax()
        self.df['drawdown'] = self.df['cumpnl'] - self.df['highvalue']

        # STATS
        self.tot_trades = self.df['pnl'].dropna().count()
        self.tot_trades_neg = self.df['pnl'][self.df['pnl'] < 1.0 ].dropna().count()
        self.tot_trades_pos = self.df['pnl'][self.df['pnl'] > 1.0 ].dropna().count()
        self.pnl = self.df['pnl'].round(2).sum()
        self.average_trade = self.df['pnl'].round(2).mean()
        self.stddev = self.df['pnl'].round(2).std()
        self.maxdd = self.df['drawdown'].round(2).min()

        self.df['drawdown_pct'] = (self.df['drawdown'] / self.df['highvalue']) * 100
        self.maxdd_pct = self.df['drawdown_pct'].round(2).min()

        self.maxloss = self.df['pnl'].round(2).min()
        self.maxwin = self.df['pnl'].round(2).max()
        self.avgLoss = self.df['pnl'][self.df['pnl'] < 0.0 ].round(2).mean()
        pass

    def get_yields_by_year(self):
        _df = self.df
        _df['year'] = _df.index.year
        _df = _df[['year', 'pnl']].groupby(['year'], sort=False).sum().sort_index()
        return _df

    def get_stats_report(self):
        if self.tot_trades_neg > 0:
            self.profit_factor = self.tot_trades/self.tot_trades_neg
        if self.pnl.std() > 0:
            self.sharpe_ratio = self.pnl.mean()/self.pnl.std()
        print("--"*40)
        print("STRATEGY STATISTICS")
        print("--"*40)
        print("Total Profit       : {:.2f}".format(self.pnl))
        print("Average Trade      : {:.2f}".format(self.average_trade))
        print("Sharpe Ratio       : {:.2f}".format(self.sharpe_ratio))
        print("--"*40)
        print("Nr Trades          : ", self.tot_trades)
        print("Nr Positive Trades : ", self.tot_trades_pos)
        print("Nr Negative Trades : ", self.tot_trades_neg)
        print("Profit Factor      : {:.2f}".format(self.profit_factor))
        print("Winning Rate       : {:.2f}".format((self.tot_trades_pos/self.tot_trades)*100), "%")
        print("--"*40)
        print("Standard Deviation : {:.2f}".format(self.stddev))
        print("Max DrawDown       : {:.2f}".format(self.maxdd))
        print("Max Loss           : {:.2f}".format(self.maxloss))
        print("Max Win            : {:.2f}".format(self.maxwin))
        print("Average Loss       : {:.2f}".format(self.avgLoss))
        print("--"*40)
        _df = self.get_yields_by_year()
        for year, pnl in _df.iterrows():
            print("Year ",year,"        : {:.2f}".format(float(pnl)))
        print("--"*40)
        pass

    def plot_equity(self, title=None):
        self.df.dropna().plot(y=['cumpnl','drawdown'], kind='line', color=['green', 'red'], title='Equity '+str(title), figsize=(12,6))
        plt.axvspan(self.long_term_df.index[0], self.long_term_df.index[-1], color='grey', alpha=0.3)
        plt.axvspan(self.short_term_df.index[0], self.short_term_df.index[-1], color='green', alpha=0.3)

        plt.grid()
        plt.show()
        pass

    def validate(self, long_term_periods=cfg.STRATEGY_EVALUATOR_LONG_TERM, short_term_periods=cfg.STRATEGY_EVALUATOR_SHORT_TERM, title='STRATEGY'):
        """ Default long_term is 18months,
            default short_term is 3months
            returns status boolean
        """
        self.long_term_df = self.df.iloc[-long_term_periods:]
        self.short_term_df = self.df.iloc[-short_term_periods:]

        self.pnl_long_term = self.long_term_df['pnl'].sum()
        self.pnl_short_term = self.short_term_df['pnl'].sum()

        # PROFIT FACTOR
        self.short_term_tot_trades = self.short_term_df['pnl'].dropna().count()
        self.short_term_tot_trades_neg = self.short_term_df['pnl'][self.short_term_df['pnl'] < 1.0 ].dropna().count()
        self.short_term_pf = (self.short_term_tot_trades/self.short_term_tot_trades_neg).round(2)
        self.short_term_sr = (self.short_term_df['pnl'].mean()/self.short_term_df['pnl'].std())
        self.long_term_sr = (self.long_term_df['pnl'].mean()/self.long_term_df['pnl'].std())

        status = False
        if (self.pnl_long_term > 0) and (self.pnl_short_term > 0):
            status = True

        table = [['', 'Full Term', 'Long Term', 'Short Term'],
                 ['PnL', self.pnl.round(2), self.pnl_long_term.round(2), self.pnl_short_term.round(2)],
                 ['Drawdown', self.maxdd, self.long_term_df['drawdown'].round(2).min(), self.short_term_df['drawdown'].round(2).min()],
                 ['DD %', self.maxdd_pct, self.long_term_df['drawdown_pct'].round(2).min(), self.short_term_df['drawdown_pct'].round(2).min()],
                 ['Avg Trade', self.average_trade.round(2), self.long_term_df['pnl'].mean().round(2), self.short_term_df['pnl'].mean().round(2)],
                 ]
        tab = PrettyTable(table[0])
        tab.title = str(title)+str(" [status:"+str("ACTIVE" if status else "STOPPED")+"]")
        tab.align = 'r'
        tab.add_rows(table[1:])

        # return annualized sharpe ratio
        return status, tab, ((252**0.5) * self.long_term_sr).round(2)