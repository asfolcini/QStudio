#=======================================================================================================================
# QStudio - Easter_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import matplotlib.pyplot as plt
import pandas
import random

from core.Position import Position
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import Order, OrderType, OrderSide
from dateutil.easter import *
from datetime import datetime, timedelta

class Easter_Strategy(QBacktester):
    """
    Easter Strategy - Easter Effect (SP500,EUROSTOXX, DAX, etc...)
    """
    atMarket = False
    filter = False
    sma_filter = False
    easter = False

    def set_filters(self, sma_filter=False):
        self.sma_filter = sma_filter

    def parameters(self, offset=3, quantity=1000):
        self.offset = offset
        self.quantity = quantity

    def onEvent(self, event: Candle) -> Candle:

        qty = self.quantity

        self.indicators['sma200'] = self.indicators['close'].rolling(200).mean().fillna(0)

        day = int(event.date.strftime('%d'))
        month = int(event.date.strftime('%m'))
        year = int(event.date.strftime('%Y'))

        easter_date = easter(year)
        entry_date = easter_date - timedelta(days=self.offset)
        exit_date = easter_date + timedelta(days=self.offset)
        entry_day = int(entry_date.strftime('%d'))
        entry_month = int(entry_date.strftime('%m'))
        exit_day = int(exit_date.strftime('%d'))
        exit_month = int(exit_date.strftime('%m'))

        # ENTRY
        if day >= entry_day and day < int(easter_date.strftime('%d')) and month == entry_month and not self.atMarket:
            if self.sma_filter:
                if event.close > self.indicators['sma200'].tolist().pop():
                    if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                    self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)
                else:
                    if self.verbose: print("[",str(event.date),"]BUY filtered because C < sma200 [",str(event.close),"<",str(self.indicators['sma200'].tolist().pop()),"]")
            else:
                if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)

        # EXIT
        if day >= exit_day and month == exit_month and self.atMarket:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
            self.atMarket = not self.place_order(event, OrderType.MARKET, OrderSide.SELL, qty)


