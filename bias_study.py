# ------------------------------------------------------------------------------------------------------------ #
# Bias_Study Strategy
# Example of usage:
#   - Under crond will post on telegram channel the portfolio target
#       python3 bias_study.py --signal SPY5.DE 50 --sma-filter-off
#   - Backtest the strategy with charts and stats
#       python3 bias_study.py --backtest SPY5.DE 50 --sma-filter-off
#   - Optimize the strategy
#       python3 bias_study.py --optimize SPY5.DE 50 --sma-filter-off
# ------------------------------------------------------------------------------------------------------------ #

import pandas
from core.strategy.Bias_Study import Bias_Study
import sys


def main():
    """
    MAIN
    """
    args = sys.argv[1:]

    """
    STARTER
    """
    if len(args) == 4 and args[0] == '--backtest' and args[3]!='':
        if args[1] != '':
            symbol = args[1]
            qty = int(args[2])
            if args[3] == "--sma-filter-on":
                run_backtest(symbol, qty, _sma_filter=True)
            else:
                run_backtest(symbol, qty, _sma_filter=False)
            return

    if len(args) == 4 and args[0] == '--signal' and args[3]!='':
        if args[1] != '':
            symbol = args[1]
            qty = int(args[2])
            if args[3] == "--sma-filter-on":
                run_backtest(symbol, qty, _sma_filter=True, mode='SIGNAL')
            else:
                run_backtest(symbol, qty, _sma_filter=False, mode='SIGNAL')
            return

    if len(args) == 3 and args[0] == '--optimize' and args[2]!='':
        if args[1] != '':
            symbol = args[1]
            qty = int(args[2])
            run_optimize(symbol, qty)
            return

    show_usage();

def show_usage():
    print("--"*60)
    print("QStudio - Bias Study v1.0 <a.sfolcini@gmail.com>")
    print("--"*60)
    print(" USAGE:")
    print("   python3 bias_study.py [--backtest/--optimize/--signal] [symbol] [quantity] [--sma-filter-on/--sma-filter-off]")
    print(" Examples:")
    print("   - BACKTEST: Backtest the strategy with the given symbol and quantity, filtering by sma200")
    print("         python3 bias_study.py --backtest SPY 100 --sma-filter-on")
    print("   - OPTIMIZE:Optimize the strategy with the given symbol and quantity")
    print("         python3 bias_study.py --optimize SPY 100")
    print("   - SIGNAL: Running the strategy, publishing Target Portfolio on telegramìs channel, filtering by sma200")
    print("         python3 bias_study.py --signal SPY 100 --sma-filter-off")
    print("")



def run_backtest(symbol, qty=100, mode='BACKTEST', _sma_filter=False,verbose=False):
    s = Bias_Study("Bias_Study ("+str(symbol)+")", symbol)
    # 4= venerdi quindi compera lunedi in chiusura e vendi mercoledi in chiusura
    s.parameters(4,2,5, qty) # G.MI
    #s.parameters(2,4,7,qty)
    s.set_filters(sma_filter=_sma_filter)
    s.set_stop_loss(-500)
    s.backtest_period("2000-07-01 00:00:00")
    if mode == 'SIGNAL':
        s.set_telegram_instant_message(True)
    s.set_verbose(verbose)
    s.run()
    if mode == 'BACKTEST':
        s.report_statistics()
        s.plot_equity()
        s.plot_yields_by_years()
        #s.plot_yields_by_months()
        s.show_historical_positions(20)
        #s.save_equity_data()




def run_optimize(symbol, qty=100, verbose=False):
    _data = []
    for entry_day in range(3, 5):
        for day_count in range(1,3):
            for pattern in range(0,9):
                for fil in range(0, 2):
                    s = Bias_Study("Bias_Study", symbol)
                    s.parameters(entry_day, day_count, pattern_nr=pattern, qty=qty)
                    if fil==0:
                        s.set_filters(False)
                    else:
                        s.set_filters(True)
                    #s.set_stop_loss(-500)
                    s.backtest_period("2000-01-01 00:00:00", "2019-12-31 00:00:00")
                    s.set_verbose(False)
                    s.run()

                    print("Entry day: "+str(entry_day)+" Exit day: "+str(day_count)+" PatternNr: "+str(pattern)+" sma200_Filter:",str(fil)," ===> PnL:"+str(s.pnl)+" AvgTrade:"+str(s.average_trade)," maxDD:",str(s.maxdd))

                    _data.append([entry_day, day_count, pattern, fil, s.pnl, s.average_trade, s.maxdd])

    opt = pandas.DataFrame(_data, columns=['EntryDay','ExitDay','Pattern Nr','sma200_filer','pnl','avgtrade','maxDD'])
    opt = opt.sort_values(['avgtrade','pnl','maxDD'], ascending=False)
    print("--"*40)
    print("OPTIMIZATION RESULTS")
    print(opt.head(20))




# -----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

