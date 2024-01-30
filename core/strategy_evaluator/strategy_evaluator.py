import os

import numpy as np
import pandas as pd
from core.analyzer.QAnalyzer import Analyzer
from prettytable import PrettyTable
from matplotlib import pyplot as plt
import core.config as cfg
from core.QStats import QStats
from core.QPlot import QPlot

def strategy_evaluator(folder, report=False, ):

    portfolio_df = pd.DataFrame(columns=['date', 'pnl'])
    portfolio_df.set_index('date', inplace=True)

    summary = [['filepath', 'strategy', 'status', 'sharpe_ratio_ann']]
    if report:
        plt.figure(figsize=(12, 6))
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            sname = filename[0:filename.index('_')]
            status, sr, df = check_single_strategy(f, strategy_name=sname)
            summary.append([f, sname, status, sr])

            _tmp_df = pd.DataFrame()
            _tmp_df = df
            _tmp_df['date'] = _tmp_df.index

            portfolio_df = pd.concat([portfolio_df, _tmp_df], axis=0, sort=False)

            if report:
                plt.plot(df['cumpnl'].fillna(method='ffill'), label=sname, linewidth=2, alpha=0.5)
                plt.plot(df['drawdown'].fillna(method='ffill'), linewidth=1, color='r', alpha=0.5)


    tab = PrettyTable(summary[0])
    tab.title = "SUMMARY"
    tab.align = 'r'
    tab.sortby = 'sharpe_ratio_ann'
    tab.reversesort = True
    tab.add_rows(summary[1:])
    print(tab)

    # TOTAL PORTFOLIO
    portfolio_df = portfolio_df.groupby('date').sum()
    portfolio_df.drop('cumpnl', axis=1)
    # replaces zeros with NaN so you get the write count of trades
    portfolio_df.replace(0, np.NaN, inplace=True)
    status, sr, df = check_single_strategy(filepath=None, strategy_name="Portfolio", dataframe=portfolio_df)
    if report:
        plt.plot(df['cumpnl'].fillna(method='ffill'), label='Portfolio', linewidth=2, color='b', alpha=1)
        plt.plot(df['drawdown'].fillna(method='ffill'), label='Portfolio DD', linewidth=2, color='r', alpha=1)
        plt.title('Equities')
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.show()

    qstats = QStats(portfolio_df)
    qstats.get_stats_report()
    qplot = QPlot()
    qplot.plot_equity(qstats.get_equity_data(), 'Portfolio Equity')
    qplot.plot_yields_by_years(qstats.get_yields_by_year(), 'Portfolio by Years')
    #qplot.plot_yields_by_months(qstats.get_yields_by_months(), "Portfolio by Months")

    #check_correlation_matrix(folder, strategy_name=sname)

    pass


def check_correlation_matrix(folder, strategy_name):

    dfp = {
        "Array_1": [30, 70, 100],
        "Array_2": [65.1, 49.50, 30.7, 90.4]
    }

    data = pd.DataFrame(dfp)

    print(data.corr())

    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            df = pd.read_csv(f, header=None, parse_dates=True, index_col=0, names=["date", "pnl"])




    return

def check_single_strategy(filepath, strategy_name='strategy', _chart=False, dataframe=None):
    """ CHECK STRATEGY"""
    if filepath is not None:
        df = pd.read_csv(filepath, header=None, parse_dates=True, index_col=0)
        df.columns=['pnl']
    else:
        df = dataframe

    a = Analyzer(df)
    #a.get_stats_report()
    status, tab, sr = a.validate(title=strategy_name)

    print("------ EVALUATION SETTINGS ------")
    print("Long  Term periods:", cfg.STRATEGY_EVALUATOR_LONG_TERM)
    print("Short Term periods:", cfg.STRATEGY_EVALUATOR_SHORT_TERM)

    print(tab)
    if _chart:
        a.plot_equity(title=strategy_name)

    return status, sr, df
