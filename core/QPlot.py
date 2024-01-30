import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class QPlot(object):

    def __init__(self):
        # Imposta il tema scuro di seaborn
        sns.set_theme(style="dark")
        sns.set_style("dark")
        sns.dark_palette("seagreen")
        pass

    def plot_yields_by_years(self, df , title):
        if not df.empty:
            df['year'] = df.index
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='year', y='pnl', palette=sns.color_palette(['red' if x < 0 else 'green' for x in df['pnl']]), alpha=0.8)

            plt.title(title, fontsize=16)
            plt.grid(True)
            plt.xlabel('years', fontsize=12)
            plt.ylabel('yields', fontsize=12)

            # Imposta le etichette dell'ascissa in verticale
            plt.xticks(rotation=90)

            plt.show()

    def plot_yields_by_months(self, df, title):
        if not df.empty:
            df['yearmonth'] = df.index
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='yearmonth', y='pnl', palette=sns.color_palette(['red' if x < 0 else 'green' for x in df['pnl']]), alpha=0.8)

            plt.title(title, fontsize=16)
            plt.grid(True)
            plt.xlabel('months', fontsize=12)
            plt.ylabel('yields', fontsize=12)

            # Imposta le etichette dell'ascissa in verticale
            plt.xticks(rotation=90)

            plt.show()

    def plot_equity(self, df, title='Equity'):
        if not df.empty:
            if 'market_date' in df:
                date_field = 'market_date'
            else:
                date_field = 'date'

            df_plot = df[['cumpnl', 'drawdown', date_field]].copy()
            df_plot.set_index(date_field, inplace=True)

            # Creare il grafico
            fig, ax = plt.subplots(figsize=(10, 6))
            df_plot['drawdown'].fillna(method='ffill').plot(ax=ax, color='red', label='Drawdown', linewidth=2)
            df_plot['cumpnl'].fillna(method='ffill').plot(ax=ax, color='green', label='Equity', linewidth=2)

            # Aggiungere una legenda
            ax.legend()

            # Aggiungere etichette e titolo
            ax.set_xlabel('time')
            ax.set_ylabel('value')
            ax.set_title(title)

            ax.grid(True)

            plt.show()
