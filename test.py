import pandas as pd
import datetime as dt
import core.utils as util

df = pd.DataFrame()

df['serie'] = [1,2,3,4,5,6,7,8,9,10]
df['sma5'] = df['serie'].rolling(5).mean().fillna(0)

print("Show DataFrame content: ")
print(df['serie'].values)
print(df['sma5'].values)


print("Adding value to a serie")
t = pd.DataFrame()
t['serie'] = [99]
df = pd.concat([df, t], ignore_index=True)
print(df['serie'].values)


print("Getting last value from a serie")
print(df['serie'].tolist().pop())

print("Getting the last N values from a serie")
e_0 = df['serie'].tolist()[0:]
e_1 = df['serie'].tolist()[-1:]
e_2 = df['serie'].tolist()[-2:]
print(e_0)
print(e_1)
print(e_2)

for e in df['serie'].tolist()[-3:]:
    print('event:', e)


print("--"*60)
print("TEST sfl_MAIA_bot passive message sender")
from core.telegram_bot import Telegram_Message
#tm = Telegram_Message()
#tm.send_message('Messaggio di test')


import pandas as pd

# Creare un DataFrame di esempio con buchi nelle date
data1 = {'date': ['2022-01-01', '2022-01-02', '2022-01-05', '2022-01-06'],
        'pnl': [10, 15, 25, 30]}
data2 = {'date': ['2022-01-01'],
         'pnl': [2.5]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

df_merged = util.merge_dataframes(df1, df2)

print(df1)
print(df2)
# Stampare il DataFrame risultante
print(df_merged)