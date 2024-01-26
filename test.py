import pandas as pd
import datetime as dt

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
data = {'Data': ['2022-01-01', '2022-01-02', '2022-01-05', '2022-01-06'],
        'Valore': [10, 15, 25, 30]}

df = pd.DataFrame(data)

# Convertire la colonna 'Data' in tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Creare un indice con tutte le date desiderate
date_complete = pd.date_range(start=df['Data'].min(), end=df['Data'].max(), freq='D')
df = df.set_index('Data').reindex(date_complete).reset_index()

# Riempire i buchi con i valori precedenti
df['Valore'] = df['Valore'].fillna(method='ffill')

# Stampare il DataFrame risultante
print(df)