#=======================================================================================================================
# QStudio - ToM_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# weekday()
# 0	Monday
# 1	Tuesday
# 2	Wednesday
# 3	Thursday
# 4	Friday
# 5	Saturday
# 6	Sunday
#=======================================================================================================================
from core.Position import Position, PositionStatus
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import OrderType, OrderSide

class LunMer_Study(QBacktester):
    """
    Campari Study Test   BIAS lun-merc positivo
    """
    filter = False
    day_count = 0
    def set_filter(self, filter=False):
        """ Filtra i mesi di luglio e agosto in quanto statisticamente negativi."""
        self.filter = filter

    def parameters(self,entry_day=0, exit_day=2, pattern_nr=0):
        self.entry_day = entry_day
        self.exit_day = exit_day
        self.pattern_nr = pattern_nr

    def filter_pattern(self, events, pattern_nr):
        if pattern_nr == 0:
            return True
        if pattern_nr == 1:
            e_0: float
            e_1: float
            e_2: float

            e : Candle
            for e in list(events[-3:]):
                print("**********   ", e.toString())
            #e_0 = events[0:]
            #e_1 = events[-1:0]
            #e_2 = events[-2:-1]
            #print(e_0,' * ', e_1, ' * ', e_2)
            #if e_0 > e_1 and e_1 > e_2:
            #    return True


        # by default return False
        return False

    def onEvent(self, event: Candle) -> Candle:

        qty = 2000
        day   = event.date.weekday()
        self.indicators['events'] = event

        if day == self.entry_day and not self.atMarket and self.filter_pattern(self.indicators['events'].tolist(), self.pattern_nr):
            if self.verbose: print("BUY "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
            self.place_order(event, OrderType.MARKET, OrderSide.BUY, qty)


        if self.atMarket:
            self.day_count = self.day_count + 1


        if self.day_count >= self.exit_day and self.atMarket:
            if self.verbose: print("SELL "+str(event.symbol)+" at market "+str(event.date)+" qty="+str(qty))
            self.place_order(event, OrderType.MARKET, OrderSide.SELL, qty)
            self.day_count = 0


