# =======================================================================================================================
# QStudio - QBacktester.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import copy
from datetime import datetime

import pandas
import numpy as np
from matplotlib import pyplot as plt

import core.config
from core.Candle import Candle
from core.Datahub import Datahub
from core.Order import Order, OrderSide, OrderStatus, OrderType
from core.Position import Position, PositionStatus, PositionSide
from core.telegram_bot import Telegram_Message

class QBacktester(object):

    telegram_bot = Telegram_Message(core.config.TELEGRAM_BOT_TOKEN, core.config.TELEGRAM_CHANNEL_ID)

    def __init__(self, strategy_name, symbol):
        self.portfolio = []
        self.orders    = []
        self.strategy_name = strategy_name
        self.symbol = symbol
        self.stop_loss = -9999999
        self.atMarket = False
        self.indicators = pandas.DataFrame()
        self.telegram_active = False


    def set_telegram_instant_message(self, active=False):
        self.telegram_active = active;

    def set_verbose(self, verbose=False):
        """ Sets verbosity level on/off """
        self.verbose = verbose

    def header(self):
        print("--" * 40)
        print("Q B a c k t e s t e r  - QStudio package")
        print("--" * 40)
        pass

    def backtest_period(self, backtest_start=None, backtest_end=None):
        '''
        If backtest_end date is not specified uses today date
        :param backtest_start:
        :param backtest_end:
        :return:
        '''
        self.backtest_start = backtest_start
        if backtest_end==None:
            self.backtest_end = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.backtest_end = backtest_end

    def run(self):
        if self.verbose:
            self.header()
            print("symbol   : " + str(self.symbol))
            print("strategy : " + str(self.strategy_name))
            print("--" * 40)
            print("from "+str(self.backtest_start)+" to "+str(self.backtest_end))
            print("--" * 40)
        self.onInit()
        s = Datahub(loadfromconfig=True)
        if self.backtest_start is not None:
            s.set_period(self.backtest_start, self.backtest_end)
        s.set_symbols(self.symbol)
        d = s.load_data(self.symbol)
        self.onStart()
        for e in d.itertuples(index=True):
            event = Candle(self.symbol, e[1], e[2], e[3], e[4], e[5], e[6])

            e = pandas.DataFrame()
            e['date'] = [event.date]
            e['close'] = [event.close]
            e['events'] = [event]
            self.indicators = pandas.concat([self.indicators, e])

            # Update Portfolio with current candle prices
            self.updatePortfolio(event)
            # Check if there are open orders to execute
            self.executeOrders(event)
            # Pass the event to the trading system engine
            self.onEvent(event)
        self.__stop()
        pass


    def set_stop_loss(self,stop_value):
        self.stop_loss = stop_value
        pass

    def place_order(self, event, order_type, order_side, quantity, price=None):
        """
        PLACE_ORDER
        :param event: Candle
        :param order_type: OrderType
        :param order_side: OrderSide
        :param quantity: quantity
        :return: boolean
        """
        order = Order(event.symbol, event.date, order_type, order_side, quantity, entry_price=price)
        self.orders.append(order)
        if self.verbose: print(". order placed: "+order.toString())

        return True



    def updatePortfolio(self, event: Candle) :
        p : Position
        for p in self.portfolio:
            p.update(event.date, event.close)
        return


    def executeOrders(self, event: Candle):
        for order in self.orders:
            # ------------------------------------------------------------------------------------------------------------------------------------------------
            # BUY SIDE
            # ------------------------------------------------------------------------------------------------------------------------------------------------
            if order.order_status == OrderStatus.OPEN and order.order_side == OrderSide.BUY:
                # MARKET ORDERS
                if (order.order_type == OrderType.MARKET) or (order.order_type == OrderType.STOP_LOSS):
                    self.orders.remove(order)
                    order.entry_price = event.close
                    order.order_status = OrderStatus.FILLED
                    order.execution_date = event.date
                    self.orders.append(order)
                    # create portfolio position
                    slippage = 0;
                    p = Position(PositionSide.LONG, order.symbol, order.execution_date, order.entry_price+slippage, order.quantity, event.close, event.date, pnl=0.0, status=PositionStatus.OPEN)
                    self.portfolio.append(p)
                    self.atMarket = True
                    # call onExecution
                    self.onExecution(order)
                # LIMIT ORDERS
                if order.order_type == OrderType.LIMIT:
                    if event.close >= order.entry_price:
                        self.orders.remove(order)
                        order.entry_price = event.close
                        order.order_status = OrderStatus.FILLED
                        order.execution_date = event.date
                        self.orders.append(order)
                        # create portfolio position
                        slippage = 0;
                        p = Position(PositionSide.LONG, order.symbol, order.execution_date, order.entry_price+slippage, order.quantity, event.close, event.date, pnl=0.0, status=PositionStatus.OPEN)
                        self.portfolio.append(p)
                        self.atMarket = True
                        self.onExecution(order)
            # ------------------------------------------------------------------------------------------------------------------------------------------------
            # SELL SIDE
            # ------------------------------------------------------------------------------------------------------------------------------------------------
            if order.order_status == OrderStatus.OPEN and order.order_side == OrderSide.SELL:
                # MARKET ORDERS
                if (order.order_type == OrderType.MARKET) or (order.order_type == OrderType.STOP_LOSS):
                    self.orders.remove(order)
                    order.entry_price = event.close
                    order.order_status = OrderStatus.FILLED
                    order.execution_date = event.date
                    self.orders.append(order)
                    # create portfolio position
                    p : Position
                    for p in self.portfolio:
                        if p.status == PositionStatus.OPEN:
                            p.close()
                    self.atMarket = False
                    # call onExecution
                    self.onExecution(order)
                # LIMIT ORDERS
                if order.order_type == OrderType.LIMIT:
                    if event.close >= order.entry_price:
                        self.orders.remove(order)
                        order.entry_price = event.close
                        order.order_status = OrderStatus.FILLED
                        order.execution_date = event.date
                        self.orders.append(order)
                        # create portfolio position
                        p : Position
                        for p in self.portfolio:
                            if p.status == PositionStatus.OPEN:
                                p.close()
                        self.atMarket = False
                        self.onExecution(order)

        return


    def onEvent(self, candleEvent):
        """ Getting the event from backtest data """
        pass

    def onInit(self):
        if self.verbose: print(". loading historical data.. .")
        pass

    def onStart(self):
        if self.verbose: print(". backtest starts...")
        pass

    def onStop(self):
        if self.telegram_active: self.publish_target_portfolio()
        pass

    def onExecution(self, order : Order):
        if self.verbose: print(". order execued: "+str(order.toString()))
        pass


    def publish_target_portfolio(self):
        mex = self.build_target_portfolio_message(self.strategy_name + " TARGET PORTFOLIO")
        self.send_telegram(mex)


    def show_target_portfolio(self):
        print(' . target portfolio content')
        p : Position
        for p in list(self.portfolio):
            if p.status == PositionStatus.OPEN:
                print(" . " + p.toString())

    def get_target_portfolio(self):
        """
        Returns Dataframe for target portfolio
        :return: target_portfolio (DataFrame)
        """
        tp = []
        p : Position
        for p in list(self.portfolio):
            if p.status == PositionStatus.OPEN:
                tp.append(p)
                #tp.assign(p)
        return tp


    def plot_equity(self):
        if not self.df.empty:
            self.df.plot(x='open_date', y=['cumpnl','drawdown'], kind='line', color=['green','red'], title='Equity '+str(self.strategy_name))
            plt.grid()
            plt.show()


    def get_yields_by_year(self):
        if not self.df.empty:
            _df = self.df
            _df['year'] = _df['open_date'].dt.year
            _df = _df[['year', 'pnl']].groupby(['year'], sort=False).sum().sort_index()
            return _df
        else:
            return pandas.DataFrame()

    def get_yields_by_yearsmonths(self):
        _df = self.df
        _df['yearmonth'] = _df['open_date'].dt.strftime("%Y-%m")
        _df = _df[['yearmonth', 'pnl']].groupby(['yearmonth'], sort=False).sum().sort_index()
        return _df

    def plot_yield_by_yearsmonths(self):
        _df = self.get_yields_by_yearsmonths()
        _df.plot.bar(y=['pnl'], color='cornflowerblue')
        for ym,pnl in _df.iterrows():
            print("Year/Month : ",ym,"     PnL : {:.2f}".format(float(pnl)))
        plt.grid()
        plt.show()

    def plot_yield_by_years(self):
        if not self.df.empty:
            _df = self.get_yields_by_year()
            _df.plot.bar(y=['pnl'], color='cornflowerblue')
            plt.grid()
            plt.show()


    def show_historical_positions(self, last_position_nr=999999):
        """
        Prints Historical Positions
        :return:
        """
        p : Position
        i = 1
        for p  in self.portfolio:
            if last_position_nr > len(self.portfolio) - i: print(p.toPrettyString_inline())
            i = i+1
        pass

    def get_historical_positions(self):
        """
        Gets Historical Positions
        :return:
        """
        return self.portfolio

    def get_stats_report(self):
        print("--"*40)
        print("STRATEGY STATISTICS")
        print("--"*40)
        print("Total Profit       : {:.2f}".format(self.pnl))
        print("Average Trade      : {:.2f}".format(self.average_trade))
        print("--"*40)
        print("Nr Trades          : ", self.tot_trades)
        print("Nr Positive Trades : ", self.tot_trades_pos)
        print("Nr Negative Trades : ", self.tot_trades_neg)
        if self.tot_trades_neg>0:
            print("Profit Factor      : {:.2f}".format(self.tot_trades/self.tot_trades_neg))
        if self.tot_trades>0:
            print("Winning Rate       : {:.2f}".format((self.tot_trades_pos/self.tot_trades)*100), "%")
        print("--"*40)
        print("Standard Deviation : {:.2f}".format(self.stddev))
        print("Max DrawDown       : {:.2f}".format(self.maxdd))
        print("Max Loss           : {:.2f}".format(self.maxloss))
        print("Max Win            : {:.2f}".format(self.maxwin))
        print("Average Loss       : {:.2f}".format(self.avgLoss))
        print("--"*40)
        _df = self.get_yields_by_year()
        for year, pnl in _df.iterrows():
            print("Year ",year,"        : {:.2f}".format(float(pnl)))
        print("--"*40)
        pass

    def __stop(self):
        self.df = pandas.DataFrame(p.__dict__ for p in self.portfolio)
        if not self.df.empty:
            self.df['cumpnl'] = self.df['pnl'].cumsum().round(2)

            self.df['highvalue'] = self.df['cumpnl'].cummax()
            self.df['drawdown'] = self.df['cumpnl'] - self.df['highvalue']

            # STATS
            self.tot_trades = self.df['pnl'].count()
            self.tot_trades_neg = self.df['pnl'][self.df['pnl'] < 1.0 ].count()
            self.tot_trades_pos = self.df['pnl'][self.df['pnl'] > 1.0 ].count()
            self.pnl = self.df['pnl'].sum().round(2)
            self.average_trade = self.df['pnl'].mean().round(2)
            self.stddev = self.df['pnl'].std()
            self.maxdd = self.df['drawdown'].min()
            self.maxloss = self.df['pnl'].min()
            self.maxwin = self.df['pnl'].max()
            self.avgLoss = self.df['pnl'][self.df['pnl'] < 0.0 ].mean()

            if self.verbose: print(". backtest finished.")
            self.onStop()
        else:
            self.tot_trades = 0
            self.tot_trades_neg = 0
            self.tot_trades_pos = 0
            self.pnl = 0.0
            self.average_trade = 0.0
            self.stddev = 0.0
            self.maxdd = 0.0
            self.maxloss = 0.0
            self.maxwin = 0.0
            self.avgLoss = 0.0
        pass

    def build_target_portfolio_message(self, title=None):
        sep = "--"*40
        signal_day = datetime.today().strftime('%Y-%m-%d')
        target_portfolio = self.get_target_portfolio()
        if title != None:
            text = signal_day +"  "+ title+"\n"
        text = text + sep +"\n"

        if len(target_portfolio) == 0:
            last_trade : Position;
            last_trade = self.get_historical_positions().pop()
            text = text + "All position have been closed, here is the last one:\n"
            text = text + last_trade.toPrettyString()+"\n"
        else:
            p : Position
            for p in target_portfolio:
                text = text + p.toPrettyString()+"\n"

        text = text + sep+"\n"
        return text;


    def send_telegram(self, message):
        """
        Use this function to send out telegram instant message!
        In order to send out messages, you have to activate telegram active flag,
        by default is false.
        :param message:
        :return:
        """
        if self.telegram_active:
            self.telegram_bot.send_message(message);

    def sma(self, data, n):
        sma = data.rolling(window = n).mean()
        return pandas.DataFrame(sma)
