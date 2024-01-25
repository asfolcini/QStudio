#=======================================================================================================================
# QStudio - Miner_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import datetime

from core.Order import OrderType, OrderSide
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.report import Report
import core.patterns.filter_patterns as ptn
from core.QBacktester import ExecutionMode
import pandas
import time
import json
import core.patterns.filter_patterns as patterns
from core.Datahub import Datahub
import pandas_ta as pta
import core.utils as utils

class Miner_Strategy(QBacktester):
    """
    Miner Strategy
    """

    def __init__(self, strategy_name, symbol):
        super().__init__(strategy_name, symbol)

    def set_quantity(self, qty=1):
        self.quantity = qty

    def set_trend_follower(self, value=False):
        self.trend_follower = value

    def set_trend_filter(self, value=False):
        self.trend_filter = value

    def set_entry_pattern(self, value=0):
        self.entry_pattern = int(value)

    def set_rsi_period(self, rsi_period=14):
        self.rsi_period = int(rsi_period)

    def set_rsi_low_level(self, rsi_low_level=30):
        self.rsi_low_level = rsi_low_level
    def set_rsi_high_level(self, rsi_high_level=70):
        self.rsi_high_level = rsi_high_level


    def verbose(self, verbose=True):
        """ Sets verbosity level on/off """
        self.verbose = verbose


    def onEvent(self, event: Candle) -> Candle:
        self.indicators['sma200'] = pta.sma(self.indicators['close'], 200)
        self.indicators['rsi'] = pta.rsi(self.indicators['close'], length=self.rsi_period)

        self.indicators['sma200'] = self.indicators['sma200'].fillna(0)
        self.indicators['rsi'] = self.indicators['rsi'].fillna(0)

        sma = self.indicators['sma200'].tolist().pop()
        rsi = self.indicators['rsi'].tolist().pop()

        if self.trend_filter:
            trend_filter_condition = event.close > sma
        else:
            trend_filter_condition = True

        events = self.indicators['events']

        if self.trend_follower:
            long_condition = trend_filter_condition and rsi >= self.rsi_high_level and ptn.filter_pattern(events, self.entry_pattern)
            exit_long_condition = (not trend_filter_condition) or rsi <= self.rsi_low_level
        else:
            long_condition = trend_filter_condition and rsi <= self.rsi_low_level and ptn.filter_pattern(events, self.entry_pattern)
            exit_long_condition = (not trend_filter_condition) or rsi >= self.rsi_high_level


        if not self.atMarket and long_condition:
            if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.quantity))
            self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, self.quantity)
        if self.atMarket and exit_long_condition:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.quantity))
            self.atMarket = not self.place_order(event, OrderType.MARKET, OrderSide.SELL, self.quantity)


def strategy_execute(config_file=None, mode=ExecutionMode.BACKTEST):
    '''
        --strategy config/Miner_ENI.json
    '''
    start_time = time.time()
    print("Loading config from file ", config_file)
    f = open(config_file)
    config_data = json.load(f)
    f.close()
    _name = config_data["name"]
    _symbols = config_data["symbols"]
    _qty = config_data["quantity"]
    _type = config_data["strategy"]["type"]
    if _type == "mean-reverting":
        _mean_reverting = True
    else:
        _mean_reverting = False
    _trend_filter = config_data["strategy"]["trend-filter"]
    _entry_pattern = config_data["strategy"]["entry-pattern"]
    _engine = config_data["strategy"]["engine"]
    _rsi_period = config_data["strategy"]["rsi-period"]
    _rsi_low_level = config_data["strategy"]["rsi-low-level"]
    _rsi_high_level = config_data["strategy"]["rsi-high-level"]

    if "backtest-data" in config_data:
        if "from" in config_data["backtest-data"]:
            _backtest_data_from = config_data["backtest-data"]["from"]
        else:
            _backtest_data_from = "1980-01-01 00:00:00"
        if "to" in config_data["backtest-data"]:
            _backtest_data_to = config_data["backtest-data"]["to"]
        else:
            _backtest_data_to = None

    print("Preparing data for strategy", str(_name), "[", mode, "]")

    # Optimization parameters
    if "optimize" in config_data:
        if "order_by" in config_data["optimize"]:
            _order_by = config_data["optimize"]["order_by"]
        else:
            _order_by = ['avgtrade', 'pnl', 'profit_factor', '#Trades']
        if "entry-pattern" in config_data["optimize"]:
            _opt_entry_pattern = config_data["optimize"]["entry-pattern"]
        else:
            _opt_entry_pattern = [_entry_pattern, _entry_pattern+1] # default values
        if "rsi-period" in config_data["optimize"]:
            _opt_rsi_period = config_data["optimize"]["rsi-period"]
        else:
            _opt_rsi_period = [_rsi_period, _rsi_period+1] # default values
        if "rsi-low-level" in config_data["optimize"]:
            _opt_rsi_low_level = config_data["optimize"]["rsi-low-level"]
        else:
            _opt_rsi_low_level = [_rsi_low_level, _rsi_low_level+1] # default values
        if "rsi-high-level" in config_data["optimize"]:
            _opt_rsi_high_level = config_data["optimize"]["rsi-high-level"]
        else:
            _opt_rsi_high_level = [_rsi_high_level, _rsi_high_level+1] # default values
        if "trend-filter" in config_data["optimize"]:
            _opt_trend_filter = config_data["optimize"]["trend-filter"]
        else:
            _opt_trend_filter = [_trend_filter] # default values

    s = Datahub(loadfromconfig=True)
    if _symbols is not None:
        s.set_symbols(_symbols)

    _opt_data = []
    for s in s.get_symbols():
        if mode == ExecutionMode.OPTIMIZE:
            combinations = len(range(*_opt_entry_pattern)) * len(_opt_trend_filter) * len(range(*_opt_rsi_period)) * len(range(*_opt_rsi_low_level)) * len(range(*_opt_rsi_high_level))
            print("--"*40)
            print("-- OPTIMIZATION PARAMETERS  -- Combinations:", combinations, "(it might take a while.. .)")
            print("--"*40)
            print(json.dumps(config_data["optimize"], separators=(',', ':')))
            for opt_entry_pattern in range(*_opt_entry_pattern):
                for opt_trend_filter in _opt_trend_filter:
                    for opt_rsi_period in range(*_opt_rsi_period):
                        for opt_rsi_low_level in range(*_opt_rsi_low_level):
                            for opt_rsi_high_level in range(*_opt_rsi_high_level):
                                x = Miner_Strategy(_name+' '+str(s), s)
                                x.set_quantity(_qty)
                                x.backtest_period(_backtest_data_from, _backtest_data_to)
                                x.set_verbose(False)
                                x.set_rsi_low_level(opt_rsi_low_level)
                                x.set_rsi_high_level(opt_rsi_high_level)
                                x.set_trend_follower(not _mean_reverting)
                                x.set_trend_filter(opt_trend_filter)
                                x.set_entry_pattern(opt_entry_pattern)
                                x.set_rsi_period(opt_rsi_period)
                                x.run()
                                _opt_data.append([x.symbol, _mean_reverting, opt_entry_pattern, opt_trend_filter,
                                                  opt_rsi_period, opt_rsi_low_level, opt_rsi_high_level, '{:,}'.format(x.pnl),
                                                  '{:,}'.format(x.average_trade), "{:.2f}".format(x.winrate),
                                                  "{:.2f}".format(x.profit_factor), x.tot_trades, '{:,.2f}'.format(x.maxdd),
                                                  '{:,.2f}'.format(x.maxdd_pct)])

            opt = pandas.DataFrame(_opt_data, columns=['symbol', 'mean-reverting', 'entry_pattern', 'trend_filter',
                                                       'rsi_period', 'rsi_low', 'rsi_high', 'pnl', 'avgtrade',
                                                       'winrate', 'profit_factor', '#Trades', 'maxdd', '%maxdd'])
            opt = opt.sort_values(_order_by, ascending=False)
            print("--"*60)
            print(" O P T I M I Z A T I O N     R E S U L T S")
            print("--"*60)
            print(opt.head(30))
            Report.save_optimization_report(_name, opt, json.dumps(config_data, indent=4), utils.get_formatted_time(start_time))
        else:
            # BACKTEST / SIGNAL SECTION
            x = Miner_Strategy(_name+' '+str(s), s)
            x.set_quantity(_qty)
            if mode == ExecutionMode.BACKTEST:
                x.backtest_period(_backtest_data_from, _backtest_data_to)
            else:
                x.backtest_period(_backtest_data_from)
            x.set_verbose(False)
            x.set_trend_follower(not _mean_reverting)
            x.set_trend_filter(_trend_filter)
            x.set_entry_pattern(_entry_pattern)
            x.set_rsi_period(_rsi_period)
            x.set_rsi_low_level(_rsi_low_level)
            x.set_rsi_high_level(_rsi_high_level)
            x.run()
            if mode == ExecutionMode.BACKTEST:
                x.get_stats_report()
                x.plot_equity()
                x.plot_yield_by_years()
                #x.plot_yield_by_yearsmonths()
                x.show_historical_positions(20)
            else:
                x.show_target_portfolio()

    print(f"Elapsed Time: {utils.get_formatted_time(start_time)}")
