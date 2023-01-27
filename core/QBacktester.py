# =======================================================================================================================
# QStudio - QBacktester.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import copy

import pandas

from core.Candle import Candle
from core.Datahub import Datahub
from core.Order import Order, OrderSide, OrderStatus, OrderType


class QBacktester(object):


    portfolio = []
    orders    = []

    backtest_start = None
    backtest_end = None

    def __init__(self, strategy_name, symbol):
        self.strategy_name = strategy_name
        self.symbol = symbol

    def header(self):
        print("--" * 20)
        print("Q B a c k t e s t e r  - QStudio package")
        print("--" * 20)
        pass

    def backtest_period(self, backtest_start=None, backtest_end=None):
        self.backtest_start = backtest_start
        self.backtest_end = backtest_end

    def fire(self):
        self.header()
        print("symbol   : " + str(self.symbol))
        print("strategy : " + str(self.strategy_name))
        print("--" * 20)
        self.onInit()
        s = Datahub(loadfromconfig=True)
        if self.backtest_start is not None:
            s.set_period(self.backtest_start, self.backtest_end)
        s.set_symbols(self.symbol)
        d = s.load_data(self.symbol)
        self.onStart()
        for e in d.itertuples(index=True):
            event = Candle(self.symbol, e[1], e[2], e[3], e[4], e[5], e[6])
            # Update Portfolio with current candle prices
            self.updatePortfolio(event)
            # Check if there are open orders to execute
            self.executeOrders(event)
            # Pass the event to the trading system engine
            self.onEvent(event)
        self.onStop()


    def place_order(self, event, order_type, order_side, quantity):
        """
        PLACE_ORDER
        :param event: Candle
        :param order_type: OrderType
        :param order_side: OrderSide
        :param quantity: quantity
        :return: boolean
        """
        order = Order(event.symbol, event.date, order_type, order_side, quantity)
        self.orders.append(order)
        print(". order placed: "+order.toString())

        return True



    def updatePortfolio(self, event: Candle) :
        for p in self.portfolio:
            print("Update position "+str(p))
        return


    def executeOrders(self, event: Candle):
        for order in self.orders:
            if order.order_status == OrderStatus.OPEN and order.order_side == OrderSide.BUY:
                # MARKET ORDERS
                if order.order_type == OrderType.MARKET:
                    self.orders.remove(order)
                    order.entry_price = event.close
                    order.order_status = OrderStatus.FILLED
                    order.execution_date = event.date
                    self.orders.append(order)
                    self.onExecution(order)
                # LIMIT ORDERS
                if order.order_type == OrderType.LIMIT:
                    if event.close >= order.entry_price:
                        self.orders.remove(order)
                        order.entry_price = event.close
                        order.order_status = OrderStatus.FILLED
                        order.execution_date = event.date
                        self.orders.append(order)
                        self.onExecution(order)
        return


    def onEvent(self, candleEvent):
        """ Getting the event from backtest data """
        pass

    def onInit(self):
        print(". loading historical data.. .")
        pass

    def onStart(self):
        print(". backtest starts...")
        pass

    def onStop(self):
        print(". backtest finished.")
        pass

    def onExecution(self, order : Order):
        print(". order execued: "+str(order.toString()))
        pass