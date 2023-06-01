
import pandas
from core.strategy.Bias_Study import Bias_Study

symbol = "G.MI"

optimize = False
if not optimize:
    s = Bias_Study("Bias_Study ("+str(symbol)+")", symbol)
    #s.parameters(4, 2, 0)  # 4= venerdi quindi compera lunedi in chiusura e vendi mercoledi in chiusura
    s.parameters(4,2,5)
    s.set_filters(sma_filter=True)
    s.set_stop_loss(-5000)
    s.backtest_period("2000-01-01 00:00:00", "2023-12-31 00:00:00")
    s.set_verbose(False)
    s.run()
    s.get_stats_report()
    s.plot_equity()
    s.plot_yield_by_years()
    #s.plot_yield_by_yearsmonths()
    #s.get_historical_positions()
else:
    _data = []
    for entry_day in range(4, 5):
        for day_count in range(2,3):
            for pattern in range(0,8):
                for fil in range(0, 2):
                    s = Bias_Study("Bias_Study", symbol)
                    s.parameters(entry_day, day_count, pattern_nr=pattern)
                    if fil==0:
                        s.set_filters(False)
                    else:
                        s.set_filters(True)
                    s.set_stop_loss(-500)
                    s.backtest_period("2010-01-01 00:00:00", "2019-12-31 00:00:00")
                    s.set_verbose(False)
                    s.run()

                    print("Entry day: "+str(entry_day)+" Exit day: "+str(day_count)+" PatternNr: "+str(pattern)+" sma200_Filter:",str(fil)," ===> PnL:"+str(s.pnl)+" AvgTrade:"+str(s.average_trade)," maxDD:",str(s.maxdd))

                    _data.append([entry_day, day_count, pattern, fil, s.pnl, s.average_trade, s.maxdd])

    opt = pandas.DataFrame(_data, columns=['EntryDay','ExitDay','Pattern Nr','sma200_filer','pnl','avgtrade','maxDD'])
    opt = opt.sort_values(['avgtrade','pnl','maxDD'], ascending=False)
    print("--"*40)
    print("OPTIMIZATION RESULTS")
    print(opt.head(20))





