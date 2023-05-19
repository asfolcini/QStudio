import pandas as pd

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


print("--"*60)
print("TEST sfl_MAIA_bot passive message sender")
from core.telegram_bot import Telegram_Message
tm = Telegram_Message()
tm.send_message('Messaggio di test')
