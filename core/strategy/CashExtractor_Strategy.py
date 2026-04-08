import pandas as pd
from core.Position import Position
from core.QBacktester import QBacktester
from core.Candle import Candle
from core.Order import Order, OrderType, OrderSide

class CashExtractor_Strategy(QBacktester):
    """
    Strategy based on the crossover between 20-period and 50-period moving averages.
    Buys when the 20-period MA is less than 5% below the 50-period MA and sells when the 20-period MA is more than 5% above the 50-period MA.
    Buys on the first available day between the 20th and 25th of the month, and sells on the first available day between the 3rd and 10th of the month.
    """

    atMarket = False

    def parameters(self, entry_day_start=20, entry_day_end=25, exit_day_start=3, exit_day_end=10, quantity=1000, threshold=0.05):
        """
        Impostazione dei parametri della strategia.
        threshold è il limite percentuale tra MM20 e MM50 per determinare quando comprare e vendere.
        """
        self.entry_day_start = entry_day_start
        self.entry_day_end = entry_day_end
        self.exit_day_start = exit_day_start
        self.exit_day_end = exit_day_end
        self.quantity = quantity
        self.threshold = threshold  # Imposta la soglia percentuale per acquisto e vendita

    def onEvent(self, event: Candle) -> Candle:
        qty = self.quantity

        self.indicators['sma20'] = self.indicators['close'].rolling(20).mean().fillna(0)
        self.indicators['sma50'] = self.indicators['close'].rolling(50).mean().fillna(0)

        day = int(event.date.strftime('%d'))
        month = event.date.strftime('%m')
        year = event.date.strftime('%YYYY')

        # Condizione per acquistare tra il 20 e il 25 del mese
        if day == "20":
            self.place_order(event, OrderType.MARKET, OrderSide.BUY, 10)

        return
