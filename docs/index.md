# QStudio Documentation
#### version 0.3.5

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

QStudio is an advanced tool designed for in-depth analysis of financial markets, written in Python. QStudio offers a wide range of features for correlation analysis, yield visualization, volatility measurement, and more. A distinctive feature of QStudio is its integrated backtester, allowing users to test algorithmic strategies in a virtual environment.

The tool allows users to explore, analyze, and identify potential anomalies using advanced quantitative techniques.

## Features

- **[Correlation Matrix](correlation_matrix.md):** Generate a correlation matrix between symbols.
- **Yields Visualization:** Visualize yields (daily, weekly, monthly).
- **[Volatility Measurement](volatility.md):** Measure volatility for specified periods.
- **Autocorrelation:** Measure AR(x).
- **[Detect Market Behavior](detect_market_behavior.md):** Identifies the nature of a specific financial symbol, indicating whether its price behavior is characterized by mean-reverting, trending, or random movements.
- **Backtester:** Test algorithmic strategies in a virtual environment.
- **[Datahub Integration](datahub.md):** Manage financial data with ease using the integrated Datahub.
- **Charting:** Produce basic charts (line or candles)
- **Strategy Equity Check:** Provides in-depth information on the performance of implemented trading strategies, facilitating a thorough evaluation of the tactics employed.

## Requirements

**Python Version:**
- QStudio is developed in Python, so make sure you have a compatible version installed. It is recommended to use Python version 3.9 or higher.

**Dependencies:**
- Install the necessary dependencies as specified in the `requirements.txt` file. Common dependencies include libraries such as NumPy, Pandas, Matplotlib, and others.


## Installation

To install QStudio, follow these steps:

1. Clone the repository: `git clone https://github.com/albertosfolcini/qstudio.git`
2. Navigate to the QStudio directory: `cd qstudio`
3. Install dependencies: `pip install -r requirements.txt`
4. Run QStudio: `python qstudio.py --help`

## Configuration

QStudio allows you to configure default symbols. To view or modify the configuration, use:

- Show actual configuration: `python qstudio.py --config --show`
- Show configured symbols: `python qstudio.py --config --symbols`

You can edit symbols in the config/symbols file, following the syntax used by Yahoo Finance symbols.

## Examples

Explore advanced examples of QStudio usage in the [examples.md](./docs/examples.md) file.

## Contributing

If you would like to contribute to QStudio, please follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

QStudio is licensed under the [MIT License](./LICENSE).
