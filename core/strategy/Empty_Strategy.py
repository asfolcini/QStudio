#=======================================================================================================================
# QStudio - Empty_Strategy.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
from core.QBacktester import QBacktester
from core.Candle import Candle

class Empty_Strategy(QBacktester):
    """
    Empty Strategy
    """

    def verbose(self, verbose=True):
        """ Sets verbosity level on/off """
        self.verbose = verbose

    def onEvent(self, event: Candle) -> Candle:
        if self.verbose: print(event.toString())
        return


