# QStudio v0.3.5 - Documentation

**Intro**

QStudio is an advanced tool designed for in-depth analysis of financial markets, written in Python. QStudio offers a wide range of features for correlation analysis, yield visualization, volatility measurement, and more. A distinctive feature of QStudio is its integrated backtester, allowing users to test algorithmic strategies in a virtual environment.

The tool allows users to explore, analyze, and identify potential anomalies using advanced quantitative techniques.

## Key Features

- **Correlation Matrix:** Allows users to visualize and analyze correlations among different financial instruments.


- **Yields:** Provides tools to examine and visualize the yields of financial instruments, enabling comparative analysis.


- **Volatility:** Helps measure and visualize the volatility of a specific financial instrument over time.


- **Autocorrelation:** Offers analysis of AR(x) autocorrelation over the last periods to assess past trends.


- **Algorithmic Backtester:** Allows users to test algorithmic strategies in a virtual environment, evaluating the historical performance of strategies.


- **Datahub:** Serving as a centralized repository for financial data, QStudio's Datahub relies on Yahoo Daily as its primary data source. This feature empowers users to effortlessly manage and update financial information, ensuring a streamlined process for accessing and maintaining pertinent market data. Notably, the Datahub facilitates seamless updates from Yahoo Finance, enabling users to stay up-to-date with the latest market information. In essence, QStudio's Datahub stands as a pivotal tool, playing a crucial role in organizing and accessing financial data. Its functionality significantly optimizes the analytical workflow within the application, enhancing the overall user experience.


- **Candlestick Charts:** Provides basic visualizations through candlestick charts for technical analysis.


- **Random Equity:**
Allows users to generate a specified number of random equities and organize them within a designated folder. This feature is valuable for creating simulated datasets that mimic the characteristics of real equities, enabling users to test various scenarios and strategies.


- **Check Strategy:**
Provides a comprehensive toolkit for strategy evaluation. Users can run the check strategy on a specified folder or file, with options to include or exclude the generation of charts. Additionally, the tool can produce detailed reports, aiding users in assessing the effectiveness of their financial strategies.


- **Detect Trend:**
Empowers users to analyze a set of symbols and determine their market behavior. It categorizes symbols into mean-reverting, trending, or random, offering insights that are crucial for making informed decisions in financial markets. This feature is particularly valuable for traders seeking to adapt their strategies based on prevailing market trends.

## Requirements

**Python Version:**
- QStudio is developed in Python, so make sure you have a compatible version installed. It is recommended to use Python version 3.9 or higher.

**Dependencies:**
- Install the necessary dependencies as specified in the `requirements.txt` file. Common dependencies include libraries such as NumPy, Pandas, Matplotlib, and others.



  
## Usage:

QStudio can be run from the command line with various parameters and options. Below are the main commands:


### CONFIGURATION
- `--config --show`: Show actual configuration in ./config/symbols
- `--config --symbols`: Show configured symbols in ./config/symbols

### CORRELATION MATRIX
- `--correlation_matrix`: Show correlation matrix for configured symbols
- `--correlation_matrix --save`: Save correlation matrix chart for configured symbols in repository ./output/
- `--correlation_matrix --periods [periods]`: Show correlation matrix for configured symbols and given periods
- `--correlation_matrix --periods [periods] --save`: Save correlation matrix for configured symbols and given periods in repository ./output/
- `--correlation_matrix --symbols [symbols]`: Show correlation matrix for given symbols
- `--correlation_matrix --symbols [symbols] --save`: Save correlation matrix chart for given symbols in repository ./output/
- `--correlation_matrix --symbols [symbols] --periods [periods]`: Show correlation matrix chart for given symbols for the given periods
- `--correlation_matrix --symbols [symbols] --periods [periods] --save`: Save correlation matrix chart for given symbols for the given periods

### YIELDS
- `--yields --symbols [symbols]`: Show yields for the given symbols
- `--yields --symbols [symbols] --overlay`: Show yields for the given symbols
- `--yields --symbols [symbols] --save`: Save yields chart for given symbols in repository ./output/
- `--yields --symbols [symbols] --save --overlay`: Save yields chart for given symbols in repository ./output/
- `--yields --symbols [symbols] --periods [periods]`: Show yields chart for given symbols for the given periods
- `--yields --symbols [symbols] --periods [periods] --overlay`: Show yields chart for given symbols for the given periods
- `--yields --symbols [symbols] --periods [periods] --save --overlay`: Save yields chart for given symbols for the given periods

### YIELDS WEEKLY
- `--yields_weekly --symbols [symbols]`: Show weekly yields for the given symbols
- `--yields_weekly --symbols [symbols] --save`: Save weekly yields chart for given symbols in repository ./output/
- `--yields_weekly --symbols [symbols] --periods [periods]`: Show weekly yields chart for given symbols for the given periods
- `--yields_weekly --symbols [symbols] --periods [periods] --save`: Save weekly yields chart for given symbols for the given periods

### YIELDS MONTHLY
- `--yields_monthly --symbols [symbols]`: Show monthly yields for the given symbols
- `--yields_monthly --symbols [symbols] --save`: Save monthly yields chart for given symbols in repository ./output/
- `--yields_monthly --symbols [symbols] --periods [periods]`: Show monthly yields chart for given symbols for the given periods
- `--yields_monthly --symbols [symbols] --periods [periods] --save`: Save monthly yields chart for given symbols for the given periods

### VOLATILITY
- `--volatility --symbols [symbols] --periods`: Find volatility for a given periods

### AUTOCORRELATION
- `--autocorrelation --symbols [symbols]`: Show autocorrelation AR(x) of last 21 periods
- `--autocorrelation --symbols [symbols] --save`: Save autocorrelation AR(x) of last 21 periods

### DATAHUB
- `--datahub --show`: Show DATAHUB repository in ./data/
- `--datahub --update-all`: Update the whole datahub from Yahoo Finance
- `--datahub --update [symbols]`: Update the given symbols separated by comma (e.g., --datahub update AAPL,G,MS,XOM)

### CHARTS
- `--chart --symbols [symbols]`: Show candlestick chart of given symbols
- `--chart --symbols [symbols] --save`: Save candlestick chart of given symbols
- `--chart --symbols [symbols] --periods [periods]`: Show candlestick chart of given symbols, for given periods
- `--chart --symbols [symbols] --periods [periods] --save`: Save candlestick chart of given symbols, for given periods

### RANDOM EQUITIES
- `--random_equity --folder [folder] [Nr]`: Generate a number of random equities in the given folder
- `--random_equity --clean [folder]`: Clean the given folder

### CHECK STRATEGIES
- `--check_strategy --help`: Show how to use the check strategy
- `--check_strategy --folder [folder]`: Run the check strategy, no charts
- `--check_strategy --folder [folder] --report`: Run the check strategy and produce a report
- `--check_single_strategy --file [folder]`: Run the check strategy, no charts
- `--check_single_strategy --file [folder] --report`: Run the check strategy and produce a report

### DETECT TREND
- `--detect_trend --symbols [symbols]`: Detect if the symbol(s) is mean-reverting, trending, or random

### USAGE
- `--help`: Usage instructions
- `--documentation`: Open online documentation

