from datetime import datetime

from core.Datahub import Datahub
from core.strategy.Empty_Strategy import Empty_Strategy
from core.strategy.ToM_Strategy import ToM_Strategy

#es = Empty_Strategy("Empty Strategy", "CPR.MI")
#es.verbose(False)
#es.fire()

symbol = "SPY"

s = ToM_Strategy("ToM", symbol)
s.backtest_period("2010-01-20 00:00:00", "2010-02-5 00:00:00")
s.verbose(True)
s.fire()

