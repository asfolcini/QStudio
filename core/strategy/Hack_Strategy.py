#=======================================================================================================================
# QStudio - Empty_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
from core.Order import OrderType, OrderSide
from core.QBacktester import QBacktester, ExecutionMode
from core.Candle import Candle
import pandas_ta as pta
import core.patterns.filter_patterns as ptn

class Hack_Strategy(QBacktester):
    """
    Hack Strategy
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

    def verbose(self, verbose=True):
        """ Sets verbosity level on/off """
        self.verbose = verbose


    def onEvent(self, event: Candle) -> Candle:
        self.indicators['sma200'] = pta.sma(self.indicators['close'], 200)
        self.indicators['rsi'] = pta.rsi(self.indicators['close'], length=10)

        self.indicators['sma200'] = self.indicators['sma200'].fillna(0)
        self.indicators['rsi'] = self.indicators['rsi'].fillna(0)

        sma = self.indicators['sma200'].tolist().pop()
        rsi = self.indicators['rsi'].tolist().pop()
        rsi_low  = 25
        rsi_high = 75

        #print("Close: ", event.close, "Sma: ", sma, "RSI: ", rsi)

        if self.trend_filter:
            trend_filter_condition = event.close > sma
        else:
            trend_filter_condition = True

        events = self.indicators['events']

        if self.trend_follower:
            long_condition = trend_filter_condition and rsi >= rsi_high and ptn.filter_pattern(events, self.entry_pattern)
            exit_long_condition = (not trend_filter_condition) or rsi <= rsi_low
        else:
            long_condition = trend_filter_condition and rsi <= rsi_low and ptn.filter_pattern(events, self.entry_pattern)
            exit_long_condition = (not trend_filter_condition) or rsi >= rsi_high



        if not self.atMarket and long_condition:
            if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.quantity))
            self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, self.quantity)
        if self.atMarket and exit_long_condition:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.quantity))
            self.atMarket = not self.place_order(event, OrderType.MARKET, OrderSide.SELL, self.quantity)
