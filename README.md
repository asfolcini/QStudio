# QStudio
#### https://surprisalx.com

QStudio is a comprehensive financial market analysis tool written in Python by [Alberto Sfolcini](mailto:a.sfolcini@gmail.com). It provides features such as correlation matrix visualization, yield analysis, volatility measurement, and a built-in backtester for algorithmic strategies. Users can configure symbols, generate various charts, update data from Yahoo Finance, and perform in-depth analysis to make informed decisions in financial trading. QStudio's versatility makes it a powerful tool for both quantitative analysis and strategy testing in the financial domain.


## Installation

To install QStudio, follow these steps:

1. Clone the repository: `git clone https://github.com/albertosfolcini/qstudio.git`
2. Navigate to the QStudio directory: `cd qstudio`
3. Install dependencies: `pip install -r requirements.txt`
4. Run QStudio: `python qstudio.py --help`

## Usage

QStudio offers a variety of commands for different analyses. Here are some examples:

- Show correlation matrix: `python qstudio.py --correlation_matrix`
- Visualize yields: `python qstudio.py --yields --symbols AAPL,GOOGL`
- Measure volatility: `python qstudio.py --volatility --symbols MSFT`

For more detailed usage instructions, refer to the [documentation](https://surprisalx.com/qstudio/index.php).

## Licence
n/a

## TODO LIST
- Add commissions costs
- Add reading of custom csv for historical data
- A Complete Report for a Symbol (html template)
- Basket of systems ( generate report for single system and one full report with summarized equity line)