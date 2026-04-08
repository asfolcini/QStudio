import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

# Parametri di inizializzazione
initial_cash = 20000  # Capitale iniziale
monthly_investment = 1000  # Investimento mensile
trade_fee = 0.019 / 100  # 0,019% per trade
max_fee = 19  # Massimo costo per trade
tickers = ['RACE.MI']  # Ferrari come esempio
start_date = '2021-01-01'
end_date = '2024-12-31'
dist_threshold = 0.05  # Soglia del 5% tra medie mobili

# Funzione per calcolare le medie mobili
def moving_average(data, window):
    return data.rolling(window=window).mean()

# Simulazione portfolio manager
class PortfolioManager:
    def __init__(self, cash, tickers, max_cash=20000):
        self.cash = cash
        self.max_cash = max_cash  # Limite massimo di capitale
        self.extra_cash = 0  # Variabile per tracciare il Profit & Loss accumulato dalle vendite
        self.positions = {ticker: {'quantity': 0, 'average_price': 0} for ticker in tickers}
        self.history = []
        self.total_equity = []

    def buy(self, ticker, price, amount, date):

        if self.cash < amount:
            return
        quantity = int(amount // price)  # Quantità intera
        if quantity == 0:
            return
        total_cost = quantity * price
        trade_cost = min(total_cost * trade_fee, max_fee)
        if self.cash < total_cost + trade_cost:
            return
        self.cash -= (total_cost + trade_cost)
        current_pos = self.positions[ticker]
        total_quantity = current_pos['quantity'] + quantity
        current_pos['average_price'] = (
                (current_pos['quantity'] * current_pos['average_price'] + total_cost) / total_quantity
        )
        current_pos['quantity'] = total_quantity
        self.history.append((date, 'BUY', ticker, quantity, price, self.cash, total_quantity, current_pos['average_price']))

    def sell(self, ticker, price, amount, date):
        current_pos = self.positions[ticker]
        if current_pos['quantity'] <= 0:
            return
        quantity_to_sell = int(amount // price)  # Quantità intera
        if quantity_to_sell > current_pos['quantity']:
            quantity_to_sell = current_pos['quantity']
        if quantity_to_sell == 0:
            return
        sell_value = quantity_to_sell * price
        trade_cost = min(sell_value * trade_fee, max_fee)
        self.cash += (sell_value - trade_cost)
        current_pos['quantity'] -= quantity_to_sell
        if current_pos['quantity'] == 0:
            current_pos['average_price'] = 0
        # Calcola il profit & loss e aggiungilo all'extra_cash
        pl = (sell_value - trade_cost) - (quantity_to_sell * current_pos['average_price'])
        self.extra_cash += pl
        self.history.append((date, 'SELL', ticker, quantity_to_sell, price, self.cash, current_pos['quantity'], current_pos['average_price'], pl))

    def evaluate_portfolio(self, prices, date):
        equity = self.cash + self.extra_cash  # Somma il profit&loss accumulato
        for ticker, pos in self.positions.items():
            equity += pos['quantity'] * prices[ticker]
        self.total_equity.append((date, equity))
        return equity

    def portfolio_summary(self):
        summary = {}
        for ticker, pos in self.positions.items():
            current_price = data[ticker].iloc[-1]  # Ultimo prezzo disponibile
            current_value = pos['quantity'] * current_price
            pl = current_value - (pos['quantity'] * pos['average_price'])  # Calcola il P&L
            summary[ticker] = {
                'Total Contracts': pos['quantity'],
                'Average Price': pos['average_price'],
                'Current Value': current_value,
                'Profit & Loss': pl
            }
        # Aggiungi l'extra_cash come una voce nel riepilogo del portfolio
        summary['Extra Cash'] = self.extra_cash
        return summary

# Scaricamento dei dati da Yahoo Finance
data = {}
for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)
    data[ticker] = df['Close']
data = pd.DataFrame(data)

# Calcolo delle medie mobili
data['20_MA'] = moving_average(data[tickers[0]], 20)
data['50_MA'] = moving_average(data[tickers[0]], 50)
data['Dist_MA'] = (data['20_MA'] - data['50_MA']) / data['50_MA']

# Simulazione
pm = PortfolioManager(initial_cash, tickers)
for date, row in data.iterrows():
    # Condizione per acquisto (tra il 20 e il 26 del mese)
    if 20 <= date.day <= 26:
        for ticker in tickers:
            if row['Dist_MA'] > dist_threshold:
                pm.buy(ticker, row[ticker], monthly_investment, date)  # Esegui acquisto se la dist. è positiva
            elif row['Dist_MA'] < -dist_threshold and pm.positions[ticker]['quantity'] > 0:
                pm.sell(ticker, row[ticker], monthly_investment, date)  # Esegui vendita se la dist. è negativa

    # Condizione per vendita (tra il 3 e il 10 del mese)
    if 3 <= date.day <= 10:
        for ticker in tickers:
            if row['Dist_MA'] < -dist_threshold and pm.positions[ticker]['quantity'] > 0:
                pm.sell(ticker, row[ticker], monthly_investment, date)  # Esegui vendita se la dist. è negativa

    pm.evaluate_portfolio({ticker: row[ticker] for ticker in tickers}, date)

# Output delle operazioni
operations = pd.DataFrame(pm.history, columns=['Date', 'Action', 'Ticker', 'Quantity', 'Price', 'Cash', 'Portfolio Quantity', 'Avg Price', 'Profit & Loss'])
operations['Date'] = pd.to_datetime(operations['Date'])

# Mostra extra-cash separatamente
print(f"Extra Cash (Profit & Loss accumulato dalle vendite): {pm.extra_cash:.2f} EUR")

# Portfolio Summary
portfolio_summary = pd.DataFrame(pm.portfolio_summary()).T
portfolio_summary['Total Equity'] = portfolio_summary['Current Value'].sum() + portfolio_summary.get('Extra Cash', 0)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print(operations)
print(portfolio_summary)

# Grafico equity
portfolio_values = pd.DataFrame(pm.total_equity, columns=['Date', 'Equity'])
portfolio_values['Date'] = pd.to_datetime(portfolio_values['Date'])
plt.figure(figsize=(12, 6))
plt.plot(portfolio_values['Date'], portfolio_values['Equity'], label='Portfolio Equity')
plt.title('Cumulative Equity Over Time')
plt.xlabel('Date')
plt.ylabel('Equity Value')
plt.legend()
plt.show()
