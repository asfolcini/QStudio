#=======================================================================================================================
# QStudio - ToM_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================

from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import OrderType, OrderSide

class ToM_Strategy(QBacktester):
    """
    ToMMy Strategy - Turn of the Month Effect on american markets (DJ, NSDQ, SP500)
    """
    atMarket = False
    filter = False

    def set_filter(self, filter=False):
        """ Filtra i mesi di luglio e agosto in quanto statisticamente negativi."""
        self.filter = filter

    def parameters(self,entry_day=27, exit_day=1):
        self.entry_day = entry_day
        self.exit_day = exit_day

    def onEvent(self, event: Candle) -> Candle:

        qty = 1000
        # luglio/agosto hanno ritorni stitisticamente negativi
        if self.filter:
            filter_months = ['09']
        else:
            filter_months = []

        day   = int(event.date.strftime('%d'))
        month = event.date.strftime('%m')

        if month not in filter_months:
            if day >= self.entry_day and not self.atMarket:
                if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)

            if day >= self.exit_day and day < self.exit_day+3 and self.atMarket:
                if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                self.atMarket = not self.place_order(event, OrderType.MARKET, OrderSide.SELL, qty)
        else:
            if self.verbose: print('FILTERED '+str(event.toString()))
        return


