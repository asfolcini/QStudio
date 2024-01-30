# ------------------------------------------------------------------------------------------------------------ #
# Santa Rally Strategy
# Example of usage:
#   - Under crond will post on telegram channel the portfolio target
#       python3 santarally.py --signal EWG 50 --sma-filter-off
#   - Backtest the strategy with charts and stats
#       python3 santarally.py --backtest EWG 50 --sma-filter-off
#   - Optimize the strategy
#       python3 santarally.py --optimize EWG 50 --sma-filter-off
# ------------------------------------------------------------------------------------------------------------ #

import pandas
import sys
import core.strategy.Santa_Strategy


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

    if len(args) == 4 and args[0] == '--optimize' and args[3]!='':
        if args[1] != '':
            symbol = args[1]
            qty = int(args[2])
            if args[3] == "--sma-filter-on":
                run_optimize(symbol, qty, _sma_filter=True)
            else:
                run_optimize(symbol, qty, _sma_filter=False)
            return

    show_usage();



def show_usage():
    print("--"*60)
    print(" SantaRally Strategy v1.0 <a.sfolcini@gmail.com>")
    print("--"*60)
    print(" USAGE:")
    print("   python3 santarally.py [--backtest/--optimize/--signal] [symbol] [quantity] [--sma-filter-on/--sma-filter-off]")
    print(" Examples:")
    print("   - BACKTEST: Backtest the strategy with the given symbol and quantity, filtering by sma200")
    print("         python3 santarally.py --backtest EWG 1000 --sma-filter-on")
    print("   - OPTIMIZE:Optimize the strategy with the given symbol and quantity, filtering by sma200")
    print("         python3 santarally.py --optimize EWG 1000 --sma-filter-on")
    print("   - SIGNAL: Running the strategy, publishing Target Portfolio on telegramìs channel, filtering by sma200")
    print("         python3 santarally.py --signal EWG 1000 --sma-filter-off")
    print("")

def run_backtest(symbol, qty=100, mode='BACKTEST', _sma_filter=False,verbose=False):
    _strategy_name = "SantaRally ("+symbol+")"
    s = core.strategy.Santa_Strategy.Santa_Strategy(_strategy_name, symbol)
    s.parameters(14, 4, qty)
    s.set_filters(sma_filter=_sma_filter)
    s.backtest_period("2000-01-20 00:00:00")
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
        s.save_equity_data()


def run_optimize(symbol,qty=100, _sma_filter=False, verbose=False):
    _data = []
    for entry_day in range(10, 22):
        for exit_day in range(1,10):
            _strategy_name = "SantaRally ("+symbol+")"
            s = core.strategy.Santa_Strategy.Santa_Strategy(_strategy_name, symbol)
            s.parameters(entry_day, exit_day,qty)
            s.set_filters(sma_filter= _sma_filter)
            s.backtest_period("2000-01-20 00:00:00")
            s.set_telegram_instant_message(False) # Avoid to send out messages !!
            s.set_verbose(verbose)
            s.run()

            print("Entry day: "+str(entry_day)+" Exit day: "+str(exit_day)+" ===> PnL:"+str(s.pnl)+" AvgTrade:"+str(s.average_trade)+ " MaxDD:"+str(s.maxdd))

            _data.append([entry_day, exit_day, s.pnl, s.average_trade, s.maxdd])

    opt = pandas.DataFrame(_data, columns=['EntryDay','ExitDay','pnl','avgtrade','maxdd'])
    opt = opt.sort_values(['avgtrade','pnl','maxdd'], ascending=False)
    print("--"*40)
    print("OPTIMIZATION RESULTS")
    print(opt.head(20))





# -----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

