import pandas

import core.config as cfg
from core.Datahub import datahub
import pandas as pd
from yields.Yields import Yields
import datetime

print("TESTING QStudio packages")
print("-"*60)

s = datahub(loadfromconfig=True)
s.set_symbols("RACE.MI")

d = s.load_data("RACE.MI")
c = d.columns.values.tolist()
print(c)
event = pandas.array()
for e in d.itertuples(index=True, name='Event'):
    event['Date'] = e[1]
    print(e)


