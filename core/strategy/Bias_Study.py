#=======================================================================================================================
# QStudio - Bias Study.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# weekday()
# 0	Monday
# 1	Tuesday
# 2	Wednesday
# 3	Thursday
# 4	Friday
# 5	Saturday
# 6	Sunday
#=======================================================================================================================
import pandas

from core.Position import Position, PositionStatus
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import OrderType, OrderSide
from core.patterns.filter_patterns import filter_pattern


class Bias_Study(QBacktester):
    """
    Campari Study Test   BIAS lun-merc positivo
    """
    sma_filter = False
    day_count = 0


    def set_filters(self, sma_filter=False):
        self.sma_filter = sma_filter


    def parameters(self,entry_day=0, exit_day=2, pattern_nr=0, qty=1000):
        self.entry_day = entry_day
        self.exit_day = exit_day
        self.pattern_nr = pattern_nr
        self.qty = qty



    def onEvent(self, event: Candle) -> Candle:

        day   = event.date.weekday()
        self.indicators['sma200'] = self.indicators['close'].rolling(200).mean().fillna(0)

        if self.sma_filter:
            if event.close > self.indicators['sma200'].tolist().pop():
                if day == self.entry_day and not self.atMarket and filter_pattern(self.indicators['events'], self.pattern_nr):
                    if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.qty))
                    self.place_order(event, OrderType.MARKET, OrderSide.BUY, self.qty)
        else:
            if day == self.entry_day and not self.atMarket and filter_pattern(self.indicators['events'], self.pattern_nr):
                if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.qty))
                self.place_order(event, OrderType.MARKET, OrderSide.BUY, self.qty)

        if self.atMarket:
            self.day_count = self.day_count + 1

        if self.day_count >= self.exit_day and self.atMarket:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(self.qty))
            self.place_order(event, OrderType.MARKET, OrderSide.SELL, self.qty)
            self.day_count = 0


