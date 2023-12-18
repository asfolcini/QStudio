#=======================================================================================================================
# QStudio - Santa_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# https://www.quantifiedstrategies.com/santa-claus-rally/
#=======================================================================================================================
import matplotlib.pyplot as plt
import pandas
import random

from core.Position import Position
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import Order, OrderType, OrderSide

class Santa_Strategy(QBacktester):
    """
    Santa Strategy - Santa Claus Rally Effect (SP500,EUROSTOXX, DAX, etc...)
    """
    atMarket = False
    filter = False
    sma_filter = False

    def set_filters(self, sma_filter=False):
        self.sma_filter = sma_filter

    def parameters(self,entry_day=20, exit_day=3, quantity=1000):
        self.entry_day = entry_day
        self.exit_day = exit_day
        self.quantity = quantity


    def onEvent(self, event: Candle) -> Candle:

        qty = self.quantity

        self.indicators['sma200'] = self.indicators['close'].rolling(200).mean().fillna(0)

        day   = int(event.date.strftime('%d'))
        month = int(event.date.strftime('%m'))

        # enter in december
        if day >= self.entry_day and month == 12 and not self.atMarket:
            if self.sma_filter:
                if event.close > self.indicators['sma200'].tolist().pop():
                    if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                    self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)
                else:
                    if self.verbose: print("[",str(event.date),"]BUY filtered because C < sma200 [",str(event.close),"<",str(self.indicators['sma200'].tolist().pop()),"]")
            else:
                if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)

        # exit january
        if day >= self.exit_day and month == 1 and self.atMarket:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
            self.atMarket = not self.place_order(event, OrderType.MARKET, OrderSide.SELL, qty)


