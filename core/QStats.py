import pandas as pd
class QStats(object):

    def __init__(self, df):
        self.df = df
        self.__calc()


    def __calc(self):
        if not self.df.empty:
            self.df['cumpnl'] = self.df['pnl'].cumsum().round(2)
            self.df['highvalue'] = self.df['cumpnl'].cummax()
            self.df['drawdown'] = self.df['cumpnl'] - self.df['highvalue']
            self.df['drawdown_pct'] = (self.df['drawdown'] / self.df['highvalue']) * 100
            self.maxdd = self.df['drawdown'].min()
            self.maxdd_pct = self.df['drawdown_pct'].min()

            # STATS
            self.tot_trades = self.df['pnl'].count()
            self.tot_trades_neg = self.df['pnl'][self.df['pnl'] < 1.0 ].count()
            self.tot_trades_pos = self.df['pnl'][self.df['pnl'] > 1.0 ].count()
            self.pnl = self.df['pnl'].sum().round(2)
            self.average_trade = self.df['pnl'].mean().round(2)
            self.stddev = self.df['pnl'].std()

            self.maxloss = self.df['pnl'].min()
            self.maxwin = self.df['pnl'].max()
            self.avgLoss = self.df['pnl'][self.df['pnl'] < 0.0 ].mean()
            self.winrate = (self.tot_trades_pos/self.tot_trades)*100
            if self.tot_trades_neg > 0:
                self.profit_factor = self.tot_trades/self.tot_trades_neg
            else:
                self.profit_factor = 0.0
        else:
            self.tot_trades = 0
            self.tot_trades_neg = 0
            self.tot_trades_pos = 0
            self.pnl = 0.0
            self.average_trade = 0.0
            self.stddev = 0.0
            self.maxdd = 0.0
            self.maxdd_pct = 0.0
            self.maxloss = 0.0
            self.maxwin = 0.0
            self.avgLoss = 0.0
            self.winrate = 0.0
            self.profit_factor = 0.0


    def get_equity_data(self):
        if 'market_date' in self.df.columns:
            df_equity = self.df[['cumpnl', 'drawdown', 'market_date']].copy()
        else:
            df_equity = self.df[['cumpnl', 'drawdown', 'date']].copy()
        return df_equity

    def get_stats_report(self):
        print("--"*40)
        print("STRATEGY STATISTICS")
        print("--"*40)
        print("Total Profit       : {:.2f}".format(self.pnl))
        print("Average Trade      : {:.2f}".format(self.average_trade))
        print("--"*40)
        print("Nr Trades          : ", self.tot_trades)
        print("Nr Positive Trades : ", self.tot_trades_pos)
        print("Nr Negative Trades : ", self.tot_trades_neg)
        if self.tot_trades_neg>0:
            print("Profit Factor      : {:.2f}".format(self.tot_trades/self.tot_trades_neg))
        if self.tot_trades>0:
            print("Winning Rate       : {:.2f}".format((self.tot_trades_pos/self.tot_trades)*100), "%")
        print("--"*40)
        print("Standard Deviation : {:.2f}".format(self.stddev))
        print("Max DrawDown       : {:.2f}".format(self.maxdd)+" ({:.2f}%)".format(self.maxdd_pct))
        print("Max Loss           : {:.2f}".format(self.maxloss))
        print("Max Win            : {:.2f}".format(self.maxwin))
        print("Average Loss       : {:.2f}".format(self.avgLoss))
        print("--"*40)
        _df = self.get_yields_by_year()
        for year, pnl in _df.iterrows():
            print("Year ", year, "        : {:.2f}".format(float(pnl)))
        print("--"*40)

        pass


    def get_yields_by_year(self):
        if not self.df.empty:
            _df = self.df
            if 'market_date' in _df.columns:
                field = 'market_date'
            else:
                field = 'date'
                _df[field] = _df.index

            _df[field] = pd.to_datetime(_df[field])
            _df['year'] = _df[field].dt.year
            _df = _df[['year', 'pnl']].groupby(['year'], sort=False).sum().sort_index()
            return _df
        else:
            return pd.DataFrame()

    def get_yields_by_months(self):
        _df = self.df
        if 'market_date' in _df.columns:
            field = 'market_date'
        else:
            field = 'date'
            _df[field] = _df.index

        _df[field] = pd.to_datetime(_df[field])
        _df['yearmonth'] = _df[field].dt.strftime("%Y-%m")
        _df = _df[['yearmonth', 'pnl']].groupby(['yearmonth'], sort=False).sum().sort_index()
        return _df