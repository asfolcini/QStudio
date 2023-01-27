#=======================================================================================================================
# QStudio - Position.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================

class Position:
    """
    POSITION class
    """
    def __init__(self, side, symbol, open_date, average_price, quantity, close_price, close_date, pnl, status):
        self.side = side
        self.symbol = symbol
        self.open_date = open_date
        self.close_date = close_date
        self.average_price = average_price
        self.quantity = quantity
        self.pnl = pnl
        self.status = status
        self.close_price = close_price

    def update(self, close_date, pnl, status):
        self.close_date = close_date
        self.pnl = pnl
        self.status = status


    def toString(self):
        return ("symbol:"+self.symbol+self._sep+
                "status:"+self.status+self._sep+
                "side:"+self.side+self._sep+
                "open date:"+str(self.open_date)+self._sep+
                "close date:"+str(self.close_date)+self._sep+
                "average price:"+str(self.average_price)+self._sep+
                "quantity:"+str(self.quantity)+self._sep+
                "PnL:"+str(self.pnl)
                )