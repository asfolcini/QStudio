#=======================================================================================================================
# QStudio - ToM_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
from core.Position import Position, PositionStatus
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import OrderType, OrderSide

class LunMer_Study(QBacktester):
    """
    Campari Study Test   BIAS lun-merc positivo
    """
    filter = False
    day_count = 0
    def set_filter(self, filter=False):
        """ Filtra i mesi di luglio e agosto in quanto statisticamente negativi."""
        self.filter = filter

    def parameters(self,entry_day=0, exit_day=2):
        self.entry_day = entry_day
        self.exit_day = exit_day

    def onEvent(self, event: Candle) -> Candle:

        qty = 2000
        day   = event.date.weekday()


        if day == self.entry_day and not self.atMarket:
            if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
            self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)


        if self.atMarket:
            self.day_count = self.day_count + 1


        if self.day_count >= self.exit_day and self.atMarket:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
            self.place_order(event, OrderType.MARKET, OrderSide.SELL, qty)
            self.day_count = 0


