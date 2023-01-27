#=======================================================================================================================
# QStudio - ToM_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
from datetime import datetime

from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import Order, OrderType, OrderSide, OrderStatus


class ToM_Strategy(QBacktester):
    """
    ToM Strategy
    """

    atMarket = False

    def verbose(self, verbose=True):
        """ Sets verbosity level on/off """
        self.verbose = verbose

    def onEvent(self, event: Candle) -> Candle:

        qty = 100

        if self.verbose:
            #print(event.toString())

            day   = int(event.date.strftime('%d'))
            month = event.date.strftime('%m')

            if day >= 24 and not self.atMarket:
                self.atMarket = self.place_order(event,OrderType.MARKET, OrderSide.BUY, qty)

            if day >= 1 and day < 4 and self.atMarket:
                print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                self.atMarket = False

        return

