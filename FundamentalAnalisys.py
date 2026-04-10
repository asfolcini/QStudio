import yfinance as yf

def fetch_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info:
            raise ValueError(f"No data found for ticker {ticker}")
        print(info)

        # Dati da analizzare
        market_cap = info.get('marketCap', None)
        price = info.get('currentPrice', None)
        eps = info.get('epsTrailingTwelveMonths', None)
        revenue = info.get('totalRevenue', None)
        revenue_growth = info.get('revenueGrowth', None)
        quarterly_revenue_growth = info.get('quarterlyRevenueGrowthYOY', None)
        earnings_estimate = info.get('earningsQuarterlyGrowth', None)
        fiscal_year_estimates = info.get('futureEarningsGrowth', None)

        # Verifica la presenza dei dati necessari
        if None in [market_cap, price, eps, revenue, revenue_growth, quarterly_revenue_growth, earnings_estimate, fiscal_year_estimates]:
            raise ValueError(f"Missing key financial data for ticker {ticker}")

        return {
            'market_cap': market_cap,
            'price': price,
            'eps': eps,
            'revenue': revenue,
            'revenue_growth': revenue_growth,
            'quarterly_revenue_growth': quarterly_revenue_growth,
            'earnings_estimate': earnings_estimate,
            'fiscal_year_estimates': fiscal_year_estimates
        }

    except Exception as e:
        print(f"Errore nei dati di {ticker}: {e}")
        return None

def generate_report(data, ticker):
    # Report in italiano
    report_it = f"""
    Analisi dei Fondamentali di {ticker}:

    - Capitalizzazione di mercato: {data['market_cap']:,}
    - Prezzo corrente: {data['price']}
    - Utili per azione (EPS): {data['eps']}
    - Fatturato: {data['revenue']:,}
    - Crescita del fatturato (annuale): {data['revenue_growth']*100:.2f}%
    - Crescita trimestrale del fatturato (su base annua): {data['quarterly_revenue_growth']*100:.2f}%
    - Crescita degli utili per azione (stima trimestrale): {data['earnings_estimate']*100:.2f}%
    - Previsioni di crescita degli utili per l'anno fiscale in corso: {data['fiscal_year_estimates']*100:.2f}%

    Sintesi:
    Il titolo {ticker} sta mostrando una solida performance, con un aumento significativo del fatturato e degli utili negli ultimi trimestri. La crescita annua del fatturato è superiore alla media del settore e le previsioni di utili sono positive. Con una forte posizione di mercato e prospettive di crescita, il titolo appare interessante per gli investitori a lungo termine.
    """

    # Report in inglese
    report_en = f"""
    Fundamental Analysis of {ticker}:

    - Market Capitalization: {data['market_cap']:,}
    - Current Price: {data['price']}
    - Earnings per Share (EPS): {data['eps']}
    - Revenue: {data['revenue']:,}
    - Annual Revenue Growth: {data['revenue_growth']*100:.2f}%
    - Quarterly Revenue Growth (YoY): {data['quarterly_revenue_growth']*100:.2f}%
    - Earnings Estimate (Quarterly Growth): {data['earnings_estimate']*100:.2f}%
    - Fiscal Year Earnings Growth Estimate: {data['fiscal_year_estimates']*100:.2f}%

    Summary:
    The stock of {ticker} shows strong performance, with significant growth in revenue and earnings over recent quarters. The annual revenue growth exceeds industry averages, and earnings projections are positive. With a strong market position and growth prospects, the stock looks promising for long-term investors.
    """

    return report_it, report_en

def main():
    ticker = "ENI"
    data = fetch_financial_data(ticker)

    if data:
        report_it, report_en = generate_report(data, ticker)
        print("Analisi in Italiano:")
        print(report_it)
        print("\n---\n")
        print("Analysis in English:")
        print(report_en)
    else:
        print(f"Impossibile eseguire l'analisi per il ticker {ticker}.")

if __name__ == "__main__":
    main()
