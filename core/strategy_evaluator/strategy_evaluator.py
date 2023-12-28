import os
import pandas as pd
from core.analyzer.QAnalyzer import Analyzer
from prettytable import PrettyTable
from matplotlib import pyplot as plt

def strategy_evaluator(folder, report=False, ):
    summary = [['filepath', 'strategy', 'status', 'sharpe_ratio_ann']]
    if report:
        plt.figure(figsize=(12, 6))
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            sname = filename[0:filename.index('_')]
            status, sr , df = check_single_strategy(f, strategy_name=sname)
            summary.append([f, sname, status, sr])
            if status == True and report:
                plt.plot(df['cumpnl'], label=sname, linewidth=1)
                plt.plot(df['drawdown'], linewidth=1, color='r')


    tab = PrettyTable(summary[0])
    tab.title = "SUMMARY"
    tab.align = 'r'
    tab.sortby = 'sharpe_ratio_ann'
    tab.reversesort = True
    tab.add_rows(summary[1:])
    print(tab)

    if report:
        plt.title('Equities')
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.show()

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

def check_single_strategy(filepath, strategy_name='strategy', _chart=False):
    """ CHECK STRATEGY"""
    df = pd.read_csv(filepath, header=None, parse_dates=True, index_col=0)
    df.columns=['pnl']

    a = Analyzer(df)
    #a.get_stats_report()
    status, tab, sr = a.validate(title=strategy_name)

    print(tab)
    if _chart:
        a.plot_equity(title=strategy_name)

    return status, sr, df
