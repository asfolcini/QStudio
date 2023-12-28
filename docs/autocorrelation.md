# QStudio - Autocorrelation

[Home](index.md)

Autocorrelation measures the degree of similarity between a given time series and a lagged version of itself. This information is valuable for understanding the persistence of patterns and trends in the market.

## Usage

Show or save the autocorrelation (AR) of the last 21 periods for configured symbols or specific symbols. Below are the usage options for the autocorrelation feature:

1. **Show Autocorrelation for Given Symbols:**
   ```textmate
   python qstudio.py --autocorrelation --symbols [symbols]
   ```

2. **Save Autocorrelation for Given Symbols:**
   ```textmate
   python qstudio.py --autocorrelation --symbols [symbols] --save
   ```

## Example

1. **Show Autocorrelation for Given Symbols:**
   ```pythonregexp
   python qstudio.py --autocorrelation --symbols XSX6.DE
   ```
   output:

    ![Autocorrelation](./img/autocorrelation_1.png )


2. **Save Autocorrelation for Given Symbols:**
   ```pythonregexp
   python qstudio.py --autocorrelation --symbols AAPL,GOOGL,MSFT --save
   ```


[Top](#qstudio---autocorrelation)