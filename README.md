# QStudio
#### https://surprisalx.com

QStudio is a comprehensive financial market analysis tool written in Python by [Alberto Sfolcini](mailto:a.sfolcini@gmail.com). It provides features such as correlation matrix visualization, yield analysis, volatility measurement, and a built-in backtester for algorithmic strategies. Users can configure symbols, generate various charts, update data from Yahoo Finance, and perform in-depth analysis to make informed decisions in financial trading. QStudio's versatility makes it a powerful tool for both quantitative analysis and strategy testing in the financial domain.


## Installation

To install QStudio, follow these steps:

1. Clone the repository: `git clone https://github.com/albertosfolcini/qstudio.git`
2. Navigate to the QStudio directory: `cd qstudio`
3. Install dependencies: `pip install -r requirements.txt`
4. Run QStudio: `python qstudio.py --help`

## New Features & Enhancements

### Caching System
QStudio now includes an intelligent caching system to reduce redundant API calls and computations:
- **AI Reports Caching**: Automatically caches AI-generated technical reports for each ticker
- **Screener Results Caching**: Caches multi-ticker screener results for the current day
- **Daily Expiration**: Cache files expire at midnight and regenerate the next day
- **Automatic Loading**: System automatically loads cached results when available
- **Manual Cache Clearing**: Use "Clear Cache" option in Utilities menu to reset all cached data

### Enhanced User Interface
- **PrettyTable Formatting**: Improved table layouts with better readability
- **Currency-Agnostic Display**: Removed currency symbols for international compatibility
- **Color-Coded Results**: Enhanced visual presentation for easier scanning

### Usage Examples

- Show correlation matrix: `python qstudio.py --correlation_matrix`
- Visualize yields: `python qstudio.py --yields --symbols AAPL,GOOGL`
- Measure volatility: `python qstudio.py --volatility --symbols MSFT`
- Run interactive menu: `python qstudio.py --menu`

For more detailed usage instructions, refer to the [documentation](https://surprisalx.com/qstudio/index.php).

## Security Notice
Sensitive configuration files (like `config/qstudio-configuration.json`) are automatically ignored by `.gitignore` to prevent accidental commits of API keys and other sensitive data.

## Licence
n/a

## TODO LIST
- Add commissions costs
- Add Stop Loss
- Add reading of custom csv for historical data
- A Complete Report for a Symbol (html template)
- Fix strategy Evaluator for (portfolio equity, separate funciton)