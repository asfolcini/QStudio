#=======================================================================================================================
# QStudio - ToM_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# https://www.quantifiedstrategies.com/turn-of-the-month-trading-strategy/
#=======================================================================================================================
import matplotlib.pyplot as plt
import pandas
import random

from core.Position import Position
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import Order, OrderType, OrderSide

class ToM_Strategy(QBacktester):
    """
    ToMMy Strategy - Turn of the Month Effect on american markets (DJ, NSDQ, SP500)
    """
    atMarket = False
    filter = False
    sma_filter = False

    def set_filters(self, months_filter=False, sma_filter=False):
        """ Filtra i mesi di luglio e agosto in quanto statisticamente negativi.
        """
        self.filter = months_filter
        self.sma_filter = sma_filter

    def parameters(self,entry_day=27, exit_day=1, quantity=1000):
        self.entry_day = entry_day
        self.exit_day = exit_day
        self.quantity = quantity


    def onEvent(self, event: Candle) -> Candle:

        qty = self.quantity

        self.indicators['sma200'] = self.indicators['close'].rolling(200).mean().fillna(0)


        # luglio/agosto hanno ritorni stitisticamente negativi
        if self.filter:
            filter_months = ['07','08']
        else:
            filter_months = []

        day   = int(event.date.strftime('%d'))
        month = event.date.strftime('%m')

        if month not in filter_months:
            if day >= self.entry_day and not self.atMarket:
                if self.sma_filter:
                    if event.close > self.indicators['sma200'].tolist().pop():
                        if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                        self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)
                    else:
                        if self.verbose: print("[",str(event.date),"]BUY filtered because C < sma200 [",str(event.close),"<",str(self.indicators['sma200'].tolist().pop()),"]")
                else:
                    if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                    self.atMarket = self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)

            if day >= self.exit_day and day < self.exit_day+3 and self.atMarket:
                if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
                self.atMarket = not self.place_order(event, OrderType.MARKET, OrderSide.SELL, qty)
        else:
            if self.verbose: print('FILTERED '+str(event.toString()))
        return


    def onStop(self):
       mex = self.build_target_portfolio_message(self.strategy_name + " TARGET PORTFOLIO")
       #if (self.verbose):
       self.send_telegram(mex)


