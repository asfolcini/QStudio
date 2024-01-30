# =======================================================================================================================
# QStudio - qstudio.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import datetime
import sys
import core.config as cfg
from core.Datahub import Datahub
import os
from core.correlation_matrix.CorrelationMatrix import CorrelationMatrix
from core.yields.Yields import Yields
from core.charts.Charts import Charts
from core.random_equity import random_equity as random_eq
from core.strategy_evaluator import strategy_evaluator as cs
from core.hurst.hurst_exponent import Hurst_Exponent as Hurst_Exponent
import names
import webbrowser
from core.strategy.Hack_Strategy import Hack_Strategy
from core.strategy.Miner_Strategy import strategy_execute
import pandas
from core.QBacktester import ExecutionMode


def datahub_update_all():
    """
    DATAHUB_UPDATE_ALL: update all the specified symbols in configuration config file
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.update_data()


def datahub_update(_symbols):
    """
    DATAHUB_UPDATE: update specified symbols, can be passed as a string separated by comma
    """
    header()
    s = Datahub(loadfromconfig=False)
    s.set_symbols(_symbols)
    s.update_data()


def datahub_show():
    """
    DATAHUB_SHOW: show content by listing the REPO folder
    """
    header()
    print("DATAHUB Repository")
    for file in os.listdir(cfg.DATA_REPOSITORY):
        print(" - " + str(file))


def config_symbols():
    """
    CONFIG_SYMBOLS: show configured synmbols in config symbol file
    """
    header()
    print("CONFIGURED Symbols in " + cfg.DATA_REPOSITORY)
    for x in Datahub(loadfromconfig=True).get_symbols():
        print(" - " + str(x))


def config_show():
    """
    CONFIG_SHOW
    """
    header()
    print("Configuration Settings")
    print("VERBOSE              : " + str(cfg.VERBOSE))
    print("DATAHUB REPOSITORY   : " + str(cfg.DATA_REPOSITORY))
    print("SYMBOLS FILE CONFIG  : " + str(cfg.SYMBOLS_FILEPATH))
    print("OUTPUT REPOSITORY    : " + str(cfg.OUTPUT_REPOSITORY))


def correlation_matrix_show(show=True, periods=21):
    """
    CORRELATION_MATRIX_SHOW: show correlation matrix for the configured symbols
    """
    header()
    s = Datahub(loadfromconfig=True)
    cm = CorrelationMatrix(s, show)
    cm.generate(periods)


def correlation_matrix_symbols(_symbols, show=True, periods=21):
    """
    CORRELATION_MATRIX_SYMBOLS: show correlation matrix for the given symbols
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    cm = CorrelationMatrix(s, show)
    cm.generate(periods)


def yields(_symbols, show=True, periods=252, overlay=False):
    """
    YIELDS
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=overlay)
    ys.generate(periods)


def yields_weekly(_symbols, show=True, periods=252, overlay=False):
    """
    YIELDS WEEKLY
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=overlay)
    ys.generate_week(periods)


def yields_monthly(_symbols, show=True, periods=9999, overlay=False):
    """
    YIELDS WEEKLY
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=overlay)
    ys.generate_month(periods)


def volatility(_symbols, periods=999999999):
    """
    VOLATILITY
    """
    header()
    s = Datahub(loadfromconfig=True)
    if _symbols is not None:
        s.set_symbols(_symbols)
    ys = Yields(s, False, overlay=False)
    ys.get_volatility(periods)


def autocorrelation(_symbols, show=True):
    """
    :param _symbols:
    :param show:
    :return:
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=False)
    ys.autocorrelation()


def chart(_symbols, show=True, _periods=9999, candles=False):
    """

    :param _symbols:
    :param show:
    :param _periods:
    :param candles:
    :return:
    """
    header()
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    c = Charts(s, show, overlay=False)
    if candles:
        c.generate(_periods)
    else:
        c.generate_line(_periods)


def random_equity(folder=cfg.EQUITY_OUTPUT, nr=1):
    header()
    today = datetime.date.today()
    # generate random equities
    for i in range(nr):
        rand_name = names.get_first_name(gender='female')
        print("Generating random equity: "+str(rand_name))
        random_eq.generate_random_equity(datetime.date(year=2010, month=3, day=1),
                                         datetime.date(year=today.year, month=today.month, day=today.day),
                                         filepath=str(os.path.join(folder, ''))+str(rand_name)+"_eq.csv")
    return


def random_equity_delete(folder=cfg.EQUITY_OUTPUT):
    header()
    print("Cleaning folder "+str(folder))
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            os.remove(f)
            print(" . deleting file "+str(f))
    return


def check_strategy_help():
    header()
    print("Redirect to "+cfg.CHECK_STRATEGY_HELP_URL)
    webbrowser.open(cfg.CHECK_STRATEGY_HELP_URL)
    return


def check_strategy(folder=cfg.EQUITY_OUTPUT, report=False):
    header()
    print("Check Strategy in folder "+str(folder))
    cs.strategy_evaluator(folder, report)
    return


def check_single_strategy(equity_filepath=cfg.EQUITY_OUTPUT, report=False):
    header()
    print("Check single Strategy with equity file: "+str(equity_filepath))
    cs.check_single_strategy(equity_filepath, equity_filepath, report)
    return


def open_onlinedoc():
    header()
    print("Redirect to "+cfg.ONLINE_DOCS_URL)
    webbrowser.open(cfg.ONLINE_DOCS_URL)
    return


def detect_market_behavior(_symbols):
    header()
    s = Datahub(loadfromconfig=True)
    if _symbols != None:
        s.set_symbols(_symbols)
    he = Hurst_Exponent(s)
    # he.set_margin_percentage(0.1)
    he.calc()
    return


def hack_opt(_symbols, _qty, _mean_reverting=True, _trend_filter=False, _entry_pattern=0):
    """
    :param _symbols:
    :param _qty:
    :param _mean_reverting:
    :param _trend_filter:
    :param _entry_pattern:
    :return:
    """
    header()
    print(" HACKING THE MARKET FOR FUN AND PROFIT")
    s = Datahub(loadfromconfig=True)
    if _symbols != None:
        s.set_symbols(_symbols)

    for s in s.get_symbols():
        x = Hack_Strategy("Hacking the Market for Fun and Profit", s)
        x.set_quantity(_qty)
        x.backtest_period("2000-01-20 00:00:00")
        x.set_verbose(False)
        x.set_trend_follower(not _mean_reverting)
        x.set_trend_filter(_trend_filter)
        x.set_entry_pattern(_entry_pattern)
        x.run()
        x.report_statistics()
        x.plot_equity()
        x.plot_yields_by_years()
        x.show_historical_positions(20)

    return


def hack(_symbols, _qty=100, _mean_reverting=None):
    header()
    print(" HACKING THE MARKET FOR FUN AND PROFIT")
    s = Datahub(loadfromconfig=True)
    if _symbols != None:
        s.set_symbols(_symbols)

    _data = []
    for s in s.get_symbols():
        # for each symbol in symbols...
        for trend_filter in (True, False):
            for entry_pattern in range(0, 10):
                if _mean_reverting == None:
                    for mean_reverting in (True, False):
                        if mean_reverting:
                            mtype = "Mean-Reverting"
                        else:
                            mtype = "Trend-Following"
                        x = Hack_Strategy("Hacking the Market for Fun and Profit", s)
                        x.set_quantity(_qty)
                        x.backtest_period("2000-01-20 00:00:00")
                        x.set_verbose(False)
                        x.set_trend_follower(not mean_reverting)
                        x.set_trend_filter(trend_filter)
                        x.set_entry_pattern(entry_pattern)
                        x.run()
                        _data.append([x.symbol, mtype, entry_pattern, trend_filter, x.pnl, x.average_trade, x.tot_trades, x.maxdd])
                else:
                    if _mean_reverting:
                        mtype = "Mean-Reverting"
                    else:
                        mtype = "Trend-Following"
                    x = Hack_Strategy("Hacking the Market for Fun and Profit", s)
                    x.set_quantity(_qty)
                    x.backtest_period("2000-01-20 00:00:00")
                    x.set_verbose(False)
                    x.set_trend_follower(not _mean_reverting)
                    x.set_trend_filter(trend_filter)
                    x.set_entry_pattern(entry_pattern)
                    x.run()
                    _data.append([x.symbol, mtype, entry_pattern, trend_filter, x.pnl, x.average_trade, x.tot_trades, x.maxdd])

    opt = pandas.DataFrame(_data, columns=['Symbol', 'Strategy Type', 'Entry Pattern', 'Trend Filter', 'pnl', 'avgtrade', '#Trades', 'maxdd'])
    opt = opt.sort_values(['avgtrade', 'pnl', '#Trades'], ascending=False)
    print("--"*40)
    print(" R E S U L T S")
    print(opt.head(30))
    return


def main():
    """
    MAIN
    """
    args = sys.argv[1:]

    """
    ONLINE DOCUMENTATION
    """
    if len(args) == 1 and args[0] == '--documentation':
        open_onlinedoc()
        return

    """
    DATA HUB
    """
    if len(args) == 2 and args[0] == '--datahub':
        if args[1] == '--show':
            datahub_show()
            return
    if len(args) == 2 and args[0] == '--datahub':
        if args[1] == '--update-all':
            datahub_update_all()
            return
    if len(args) == 3 and args[0] == '--datahub':
        if args[1] == '--update' and args[2] != '':
            datahub_update(args[2])
            return

    """
    CONFIGURATION
    """
    if len(args) == 2 and args[0] == '--config':
        if args[1] == '--show':
            config_show()
            return
    if len(args) == 2 and args[0] == '--config':
        if args[1] == '--symbols':
            config_symbols()
            return

    """
    CORRELATION MATRIX
    """
    if len(args) == 1 and args[0] == '--correlation_matrix':
        correlation_matrix_show(True)
        return
    if len(args) == 2 and args[0] == '--correlation_matrix':
        if args[1] == '--save':
            correlation_matrix_show(False)
            return
    if len(args) == 3 and args[0] == '--correlation_matrix':
        if args[1] == '--periods' and args[2] != '':
            correlation_matrix_show(True, int(args[2]))
            return
    if len(args) == 4 and args[0] == '--correlation_matrix':
        if args[1] == '--periods' and args[2] != '' and args[3] == '--save':
            correlation_matrix_show(False, int(args[2]))
            return
    if len(args) == 3 and args[0] == '--correlation_matrix':
        if args[1] == '--symbols' and args[2] != '':
            correlation_matrix_symbols(args[2], True)
            return
    if len(args) == 4 and args[0] == '--correlation_matrix' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            correlation_matrix_symbols(args[2], False)
            return
    if len(args) == 5 and args[0] == '--correlation_matrix' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            correlation_matrix_symbols(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--correlation_matrix' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            correlation_matrix_symbols(args[2], False, int(args[4]))
            return

    """
    YIELDS
    """
    if len(args) == 3 and args[0] == '--yields':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], True)
            return
    if len(args) == 4 and args[0] == '--yields' and args[3] == '--overlay':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], True, overlay=True)
            return
    if len(args) == 4 and args[0] == '--yields' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], False)
            return
    if len(args) == 5 and args[0] == '--yields' and args[3] == '--save' and args[4] == '--overlay':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], False, overlay=True)
            return
    if len(args) == 5 and args[0] == '--yields' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--yields' and args[3] == '--periods' and args[5] == '--overlay':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], True, int(args[4]), overlay=True)
            return
    if len(args) == 6 and args[0] == '--yields' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], False, int(args[4]))
            return
    if len(args) == 7 and args[0] == '--yields' and args[3] == '--periods' and args[5] == '--save' and args[6] == '--overlay':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], False, int(args[4]), overlay=True)
            return
    """
    YIELDS_WEEKLY
    """
    if len(args) == 3 and args[0] == '--yields_weekly':
        if args[1] == '--symbols' and args[2] != '':
            yields_weekly(args[2], True)
            return
    if len(args) == 4 and args[0] == '--yields_weekly' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            yields_weekly(args[2], False)
            return
    if len(args) == 5 and args[0] == '--yields_weekly' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields_weekly(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--yields_weekly' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields_weekly(args[2], False, int(args[4]))
            return
    """
    YIELDS_MONTHLY
    """
    if len(args) == 3 and args[0] == '--yields_monthly':
        if args[1] == '--symbols' and args[2] != '':
            yields_monthly(args[2], True)
            return
    if len(args) == 4 and args[0] == '--yields_monthly' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            yields_monthly(args[2], False)
            return
    if len(args) == 5 and args[0] == '--yields_monthly' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields_monthly(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--yields_monthly' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields_monthly(args[2], False, int(args[4]))
            return

    """
       VOLATILITY
    """
    if len(args) == 1 and args[0] == '--volatility':
        volatility(None)
        return
    if len(args) == 3 and args[0] == '--volatility':
        if args[1] == '--periods' and args[2] != '':
            volatility(None, int(args[2]))
            return
    if len(args) == 3 and args[0] == '--volatility':
        if args[1] == '--symbols' and args[2] != '':
            volatility(args[2])
            return
    if len(args) == 5 and args[0] == '--volatility':
        if args[1] == '--symbols' and args[2] != '' and args[3] == '--periods' and args[4] != '':
            volatility(args[2], int(args[4]))
            return

    """
       AUTOCORRELATION
    """
    if len(args) == 3 and args[0] == '--autocorrelation':
        if args[1] == '--symbols' and args[2] != '':
            autocorrelation(args[2], True)
            return
    if len(args) == 4 and args[0] == '--autocorrelation' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            autocorrelation(args[2], False)
            return

    """
       CHART
    """
    if len(args) == 3 and args[0] == '--chart_candles':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], candles=True)
            return
    if len(args) == 4 and args[0] == '--chart_candles' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], show=False, candles=True)
            return
    if len(args) == 5 and args[0] == '--chart_candles' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], show=True, _periods=int(args[4]), candles=True)
            return
    if len(args) == 6 and args[0] == '--chart_candles' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], show=False, _periods=int(args[4]), candles=True)
            return

    if len(args) == 3 and args[0] == '--chart':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], candles=False)
            return
    if len(args) == 4 and args[0] == '--chart' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], show=False, candles=False)
            return
    if len(args) == 5 and args[0] == '--chart' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], show=True, _periods=int(args[4]), candles=False)
            return
    if len(args) == 6 and args[0] == '--chart' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            chart(args[2], show=False, _periods=int(args[4]), candles=False)
            return

    """
    RANDOM EQUITIES
    """
    if len(args) == 4 and args[0] == '--random_equity':
        if args[1] == '--folder' and args[2] != '' and args[3] != '':
            random_equity(args[2], int(args[3]))
            return
    if len(args) == 4 and args[0] == '--random_equity':
        if args[1] == '--clean' and args[2] == '--folder' and args[3] != '':
            random_equity_delete(args[3])
            return

    """
    STRATEGY EVALUATOR
    """
    if len(args) == 2 and args[0] == '--strategy_evaluator':
        if args[1] == '--help':
            check_strategy_help()
            return
    if len(args) == 3 and args[0] == '--strategy_evaluator':
        if args[1] == '--folder' and args[2] != '':
            check_strategy(args[2], report=False)
            return
    if len(args) == 4 and args[0] == '--strategy_evaluator':
        if args[1] == '--folder' and args[2] != '' and args[3] == '--report':
            check_strategy(args[2], report=True)
            return

    """
        CHECK SINGLE STRATEGY EVALUATOR
        """
    if len(args) == 3 and args[0] == '--single_strategy_evaluator':
        if args[1] == '--file' and args[2] != '':
            check_single_strategy(args[2], report=False)
            return
    if len(args) == 4 and args[0] == '--single_strategy_evaluator':
        if args[1] == '--file' and args[2] != '' and args[3] == '--report':
            check_single_strategy(args[2], report=True)
            return

    """
    DETECT_MARKET_BEHAVIOR
    """
    if len(args) == 1 and args[0] == '--detect_market_behavior':
        detect_market_behavior(None)
        return
    if len(args) == 3 and args[0] == '--detect_market_behavior':
        if args[1] == '--symbols' and args[2] != '':
            detect_market_behavior(args[2])
            return

    """
    HACK
    """
    if len(args) == 4 and args[0] == '--hack':
        if args[1] == '--symbols' and args[2] != '':
            hack(args[2], int(args[3]), None)
            return
    if len(args) == 5 and args[0] == '--hack':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            if args[4] == '--mean-reverting':
                mr = True
            else:
                mr = False
            hack(args[2], int(args[3]), _mean_reverting=mr)
            return
    if len(args) == 7 and args[0] == '--hack':
        if args[1] == '--symbols' and args[2] != '':
            if args[4] == '--mean-reverting':
                mr = True
            else:
                mr = False
            if args[5] == '--sma-filter-on':
                tf = True
            else:
                tf = False
            hack_opt(args[2], int(args[3]), mr, tf, args[6])
            return

    """
    STOCKMINER
    """
    if len(args) == 2 and args[0] == '--stock-miner':
        if args[1] != '':
            strategy_execute(args[1], ExecutionMode.BACKTEST)
            return
    if len(args) == 3 and args[0] == '--stock-miner':
        if args[1] != '' and args[2] == '--signal':
            strategy_execute(args[1], ExecutionMode.SIGNAL)
            return
        if args[1] != '' and args[2] == '--backtest':
            strategy_execute(args[1], ExecutionMode.BACKTEST)
            return
        if args[1] != '' and args[2] == '--optimize':
            strategy_execute(args[1], ExecutionMode.OPTIMIZE)
            return

    usage()


def usage():
    """
    USAGE
    """
    header()
    print("USAGE:")
    # CONFIG
    print(" CONFIGURATION")
    print(" --config --show               : show actual configurationn " + cfg.SYMBOLS_FILEPATH)
    print(" --config --symbols            : show configured symbols in " + cfg.SYMBOLS_FILEPATH)
    print(" CORRELATION MATRIX ")

    # CORRELATION MATRIX
    print(" --correlation_matrix                                    : show correlation matrix for configured symbols")
    print(" --correlation_matrix --save                             : save correlation matrix chart for configured symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --correlation_matrix --periods [periods]                : show correlation matrix for configured symbols and given periods")
    print(" --correlation_matrix --periods [periods] --save         : save correlation matrix for configured symbols and given periods in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --correlation_matrix --symbols [symbols]                : show correlation matrix for given symbols")
    print(" --correlation_matrix --symbols [symbols] --save         : save correlation matrix chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --correlation_matrix --symbols [symbols] --periods [periods]        : show correlation matrix chart for given symbols for the given periods")
    print(" --correlation_matrix --symbols [symbols] --periods [periods] --save : save correlation matrix chart for given symbols for the given periods")

    # YIELDS
    print(" YIELDS")
    print(" --yields --symbols [symbols]                                        : show yields for the given symbols")
    print(" --yields --symbols [symbols] --overlay                              : show yields for the given symbols")
    print(" --yields --symbols [symbols] --save                                 : save yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields --symbols [symbols] --save --overlay                       : save yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields --symbols [symbols] --periods [periods]                    : show yields chart for given symbols for the given periods")
    print(" --yields --symbols [symbols] --periods [periods] --overlay          : show yields chart for given symbols for the given periods")
    print(" --yields --symbols [symbols] --periods [periods] --save --overlay   : save yields chart for given symbols for the given periods")

    # YIELDS WEEKLY
    print(" YIELDS WEEKLY")
    print(" --yields_weekly --symbols [symbols]                             : show weekly yields for the given symbols")
    print(" --yields_weekly --symbols [symbols] --save                      : save weekly yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields_weekly --symbols [symbols] --periods [periods]         : show weekly yields chart for given symbols for the given periods")
    print(" --yields_weekly --symbols [symbols] --periods [periods] --save  : save weekly yields chart for given symbols for the given periods")

    # YIELDS MONTHLY
    print(" YIELDS MONTHLY")
    print(" --yields_monthly --symbols [symbols]                             : show monthly yields for the given symbols")
    print(" --yields_monthly --symbols [symbols] --save                      : save monthly yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields_monthly --symbols [symbols] --periods [periods]         : show monthly yields chart for given symbols for the given periods")
    print(" --yields_monthly --symbols [symbols] --periods [periods] --save  : save monthly yields chart for given symbols for the given periods")

    # VOLATILITY WEEKLY
    print(" VOLATILITY")
    print(" --volatility                                         : calc volatility for configured symbols with max periods")
    print(" --volatility --periods [periods]                     : calc volatility for configured symbols with given periods")
    print(" --volatility --symbols [symbols]                     : calc volatility for given symbols")
    print(" --volatility --symbols [symbols] --periods [periods] : calc volatility for given symbols and periods")

    # AUTOCORRELATION
    print(" AUTOCORRELATION")
    print(" --autocorrelation --symbols [symbols]         : show autocorrelation AR(x) of last 21 periods")
    print(" --autocorrelation --symbols [symbols] --save  : save autocorrelation AR(x) of last 21 periods")

    # DATA HUB
    print(" DATAHUB ")
    print(" --datahub --show              : show DATAHUB repository in " + cfg.DATA_REPOSITORY)
    print(" --datahub --update-all        : update the whole datahub from yfinance")
    print(" --datahub --update [symbols]  : update the given symbols separated by comma")
    print("   example: --datahub update AAPL,G,MS,XOM")

    # CHART
    print(" CHARTS ")
    print(" --chart --symbols [symbols]                             : show candlestick chart of given symbols")
    print(" --chart --symbols [symbols] --save                      : save candlestick chart of given symbols")
    print(" --chart --symbols [symbols] --periods [periods]         : show candlestick chart of given symbols, for given periods")
    print(" --chart --symbols [symbols] --periods [periods] --save  : save candlestick chart of given symbols, for given periods")

    print(" --chart_candles --symbols [symbols]                             : show candlestick chart of given symbols")
    print(" --chart_candles --symbols [symbols] --save                      : save candlestick chart of given symbols")
    print(" --chart_candles --symbols [symbols] --periods [periods]         : show candlestick chart of given symbols, for given periods")
    print(" --chart_candles --symbols [symbols] --periods [periods] --save  : save candlestick chart of given symbols, for given periods")

    # RANDOM EQUITY
    print(" RANDOM EQUITIES")
    print(" --random_equity --folder [folder] [Nr]      : generate a number of random equities in the given folder")
    print(" --random_equity --clean --folder [folder]   : clean the given folder")

    # CHECK STRATEGIES
    print(" STRATEGY EVALUATOR")
    print(" --strategy_evaluator --help                          : show how to use the strategy_evaluator")
    print(" --strategy_evaluator --folder [folder]               : run the strategy_evaluator, no charts")
    print(" --strategy_evaluator --folder [folder] --report      : run the strategy_evaluator and produce a report")
    print(" --single_strategy_evaluator --file [folder]          : run the strategy_evaluator, no charts")
    print(" --single_strategy_evaluator --file [folder] --report : run the strategy_evaluator and produce a report")

    # HURST EXPONENT
    print(" DETECT MARKET BEHAVIOR")
    print(" --detect_market_behavior                                : detect market behavior for all configured symbols")
    print(" --detect_market_behavior --symbols [symbols]            : detect market behavior for given symbols")

    # HACKING THE MARKET FOR FUN AND PROFIT
    print(" HACKING THE MARKET FOR FUN AND PROFIT")
    print(" --hack --symbols [symbols] [qty]                                        : hack scan for given symbols and specified quantity")
    print(" --hack --symbols [symbols] [qty] [--mean-reverting | --trend-following] : hack scan for given symbols and specified strategy type")
    print(" --hack --symbols [symbols] [qty] [--mean-reverting | --trend-following] [--sma-filter-on | --sma-filter-off] [entry_pattern]    : execute with specific parameters")

    # STOCK MINER STRATEGY
    print(" STOCK MINER")
    print(" --stock-miner [strategy_config_file.json]              : execute strategy in backtest mode")
    print(" --stock-miner [strategy_config_file.json] --signal     : execute strategy for signal mode")
    print(" --stock-miner [strategy_config_file.json] --backtest   : execute strategy for backtest mode")
    print(" --stock-miner [strategy_config_file.json] --optimize   : execute strategy in optimization mode")

    print(" USAGE")
    # USAGE
    print(" --help                      : usage instructions")
    print(" --documentation             : open online documentation")


def header():
    """
    HEADER
    """
    print("-" * 120)
    print(" Q S t u d i o   " + str(cfg.VERSION))

    print(" " + datetime.date.today().strftime("%Y") + " (c) "+str(cfg.AUTHOR))
    print(" www.surprisalx.com")
    print("-" * 120)


# -----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
