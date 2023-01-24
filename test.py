import core.config as cfg
from core.Datahub import datahub
import pandas as pd
from yields.Yields import Yields
import datetime

print("TESTING QStudio packages")
print("-"*60)

s = datahub(loadfromconfig=True)
s.set_symbols("RACE.MI")
ys = Yields(s, False , overlay=False)
r = ys.get_yields("RACE.MI")
r['month'] = pd.DatetimeIndex(r['Date']).month

print(r)


