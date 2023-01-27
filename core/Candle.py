#=======================================================================================================================
# QStudio - Candle.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================

class Candle:
    """
    CANDLE CLASS
    """

    _sep = ", "

    def __init__(self, symbol, date, open, high, low, close, volume=int(0)):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.low = low
        self.high = high
        self.close = close
        self.volume = volume

    def toString(self):
        return ("symbol:"+self.symbol+self._sep+
                "datetime:"+str(self.date)+self._sep+
                "open:"+str(self.open)+self._sep+
                "high:"+str(self.high)+self._sep+
                "low:"+str(self.low)+self._sep+
                "close:"+str(self.close)+self._sep+
                "volume:"+str(self.volume)
                )