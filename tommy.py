
import pandas
from core.strategy.ToM_Strategy import ToM_Strategy

symbol = "SPY"

optimize = False
if not optimize:
    s = ToM_Strategy("ToM", symbol)
    s.parameters(24, 4)
    s.set_filter(True)
    s.backtest_period("2010-01-20 00:00:00", "2019-12-31 00:00:00")
    s.set_verbose(False)
    s.run()
    s.get_stats_report()
    s.plot_equity()
    s.plot_yield_by_years()
    #s.plot_yield_by_yearsmonths()
else:
    _data = []
    for entry_day in range(20, 30):
        for exit_day in range(1,6):
            s = ToM_Strategy("ToM", symbol)
            s.parameters(entry_day, exit_day)
            s.backtest_period("2010-01-20 00:00:00", "2019-12-31 00:00:00")
            s.set_verbose(False)
            s.run()

            print("Entry day: "+str(entry_day)+" Exit day: "+str(exit_day)+" ===> PnL:"+str(s.pnl)+" AvgTrade:"+str(s.average_trade))

            _data.append([entry_day, exit_day, s.pnl, s.average_trade])

    opt = pandas.DataFrame(_data, columns=['EntryDay','ExitDay','pnl','avgtrade'])
    opt = opt.sort_values(['avgtrade','pnl'], ascending=False)
    print("--"*40)
    print("OPTIMIZATION RESULTS")
    print(opt.head(10))

#s.plot_equity()



