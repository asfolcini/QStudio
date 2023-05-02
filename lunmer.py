
import pandas
from core.strategy.LunMer_Study import LunMer_Study

symbol = "STLA.MI"

optimize = False
if not optimize:
    s = LunMer_Study("LunMer_Study", symbol)
    s.parameters(4, 2)
    s.set_filter(True)
    s.set_stop_loss(-500)
    s.backtest_period("2010-01-01 00:00:00", "2023-12-31 00:00:00")
    s.set_verbose(True)
    s.run()
    s.get_stats_report()
    s.plot_equity()
    s.plot_yield_by_years()
    #s.plot_yield_by_yearsmonths()
    #s.get_historical_positions()
else:
    _data = []
    for entry_day in range(3, 5):
        for day_count in range(1,6):
            for stopl in range(-1000,-100,50):
                s = LunMer_Study("LunMer_Study", symbol)
                s.parameters(entry_day, day_count)
                s.set_stop_loss(stopl)
                s.backtest_period("2010-01-01 00:00:00", "2019-12-31 00:00:00")
                s.set_verbose(False)
                s.run()

                print("Entry day: "+str(entry_day)+" Exit day: "+str(day_count)+" StopLoss: "+str(stopl)+" ===> PnL:"+str(s.pnl)+" AvgTrade:"+str(s.average_trade))

                _data.append([entry_day, day_count, stopl, s.pnl, s.average_trade])

    opt = pandas.DataFrame(_data, columns=['EntryDay','ExitDay','Stop Loss','pnl','avgtrade'])
    opt = opt.sort_values(['avgtrade','pnl'], ascending=False)
    print("--"*40)
    print("OPTIMIZATION RESULTS")
    print(opt.head(10))





