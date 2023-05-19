#=======================================================================================================================
# QStudio - Position.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
from core.Order import OrderSide
from enum import Enum
import uuid

class PositionStatus(Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

class PositionSide(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'



class Position:
    """
    POSITION class
    """

    _sep = ", "

    def __init__(self, side : PositionSide, symbol, open_date, average_price, quantity, market_price, market_date, pnl, status: PositionStatus):
        self.id = str(uuid.uuid4())
        self.side = side
        self.symbol = symbol
        self.open_date = open_date
        self.market_date = market_date
        self.average_price = average_price
        self.quantity = quantity
        self.pnl = pnl
        self.market_price = market_price
        self.status = status

    def update(self, market_date, market_price):
        if self.status == PositionStatus.OPEN:
            self.market_price = market_price
            self.market_date = market_date
            if self.side == PositionSide.LONG:
                # LONG
                self.pnl = (self.market_price - self.average_price) * self.quantity
            else:
                # SHORT
                self.pnl = (self.average_price - self.market_price) * self.quantity


    def close(self):
        self.status = PositionStatus.CLOSE

    def toString(self):
        return ("id:"+self.id+self._sep+
                "symbol:"+self.symbol+self._sep+
                "side:"+str(self.side)+self._sep+
                "open date:"+str(self.open_date)+self._sep+
                "average price:"+str(self.average_price)+self._sep+
                "market date:"+str(self.market_date)+self._sep+
                "market price:"+str(self.market_price)+self._sep+
                "quantity:"+str(self.quantity)+self._sep+
                "PnL:"+str(self.pnl)+self._sep+
                "status:"+str(self.status)
                )

    def toPrettyString(self):
        _nl = "\n"
        return (
                "----------ID:"+self.id+"-----------"+_nl+
                "Symbol       : "+self.symbol+_nl+
                "Side         : "+str(self.side.name)+_nl+
                "Open Date    : "+str(self.open_date)+_nl+
                "Avg Price    : "+str(round(self.average_price,2))+_nl+
                "Market Date  : "+str(self.market_date)+_nl+
                "Market Price : "+str(round(self.market_price,2))+_nl+
                "Quantity     : "+str(self.quantity)+_nl+
                "PnL          : "+str(round(self.pnl,2))+_nl+
                "Status       : "+str(self.status.name)
                )