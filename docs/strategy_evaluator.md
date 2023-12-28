# QStudio - Strategy Evaluator

[Home](index.md)

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Evaluation Method](#evaluation-method)
- [Usage](#usage)


## Introduction

Provides a comprehensive toolkit for strategy evaluation. This functionality enables users to evaluate the effectiveness of their strategies by providing comprehensive reports and metrics.

## Prerequisites:

Before using the **Strategy Evaluator** in QStudio, ensure the following prerequisites:

1. **Equity Data Format:**
    - Save equity data for each strategy in a folder in CSV format with two columns: `date` and `equity value`.
    - The filename should correspond to the name of the strategy.

For example, if you have a strategy named "MyStrategy," the equity data file should be named "MyStrategy.csv" and have the following format:

```csv
2023-01-01, 10000
2023-01-02, 10200
2023-01-03, 9800
...
```

This format is crucial for the **Strategy Evaluator** to accurately assess and analyze the performance of each strategy. Ensure that equity data files are prepared accordingly before running the evaluator.

## Evaluation method

## Usage

### Multi-Strategy Evaluator

- Show how to use the `strategy_evaluator`:
  ```textmate
  python qstudio.py --strategy_evaluator --help
  ```

- Run the `strategy_evaluator` for strategies in a specific folder without generating charts:
  ```textmate
  python qstudio.py --strategy_evaluator --folder [folder]
  ```

- Run the `strategy_evaluator` for strategies in a specific folder and generate a report:
  ```textmate
  python qstudio.py --strategy_evaluator --folder [folder] --report
  ```

### Single Strategy Evaluator

- Run the `strategy_evaluator` for a single strategy from a file without generating charts:
  ```textmate
  python qstudio.py --single_strategy_evaluator --file [file]
  ```

- Run the `strategy_evaluator` for a single strategy from a file and generate a report:
  ```textmate
  python qstudio.py --single_strategy_evaluator --file [file] --report
  ```

These examples demonstrate how to use the **Strategy Evaluator** to assess the performance of trading strategies either in bulk from a folder or for a single strategy from a file, with or without generating detailed reports.



[Top](#qstudio---strategy-evaluator)