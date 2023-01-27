#=======================================================================================================================
# QStudio - Order.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import enum
import uuid
from enum import Enum

class OrderStatus(Enum):
    OPEN = 'OPEN'
    FILLED = 'FILLED'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    PENDING = 'PENDING'

class OrderType(Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'

class OrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class Order:
    """
    ORDER CLASS
    """
    _sep = ", "

    def __init__(self, symbol, date, order_type : OrderType, order_side, quantity, entry_price=0):

        if order_type == OrderType.LIMIT and  entry_price <= 0:
            raise Exception("ERROR: if LIMIT order, entry_price must be specified!!")


        self.id = str(uuid.uuid4())
        self.symbol = symbol
        self.date = date
        self.order_type = order_type
        self.order_side = order_side
        self.quantity = quantity
        self.entry_price = entry_price
        self.order_status = OrderStatus.OPEN
        self.execution_date = None

    def toString(self):
        return ("id:"+self.id+self._sep+
                "symbol:"+self.symbol+self._sep+
                "datetime:"+str(self.date)+self._sep+
                "order_type:"+str(self.order_type)+self._sep+
                "order_side:"+str(self.order_side)+self._sep+
                "quantity:"+str(self.quantity)+self._sep+
                "entry_price:"+str(self.entry_price)+self._sep+
                "status:"+str(self.order_status)+self._sep+
                "execution_date:"+str(self.execution_date)
                )