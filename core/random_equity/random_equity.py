import datetime
import random

def generate_random_equity(start_date=datetime.date(year=2010, month=1, day=1),
                           end_date=datetime.date(year=2020, month=1, day=1),
                           filepath="random_eq.csv"):

    f = open(filepath, "w")

    current_date = start_date
    while current_date <= end_date:

        if random.randrange(0,10)>5:
            pnl = random.randrange(-1000, 1100)
            line = current_date.strftime("%Y-%m-%d")+str(",")+str(pnl)+"\n"
            f.write(line)

        current_date += datetime.timedelta(days=1)
    f.close()
    return