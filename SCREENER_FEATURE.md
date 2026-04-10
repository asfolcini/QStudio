# Multi-Ticker Screener Feature

## Overview
The Multi-Ticker Screener is a new feature that allows users to analyze multiple stock tickers simultaneously, providing a comprehensive overview of market conditions and technical indicators across selected securities.

## Features
- **Multiple Ticker Analysis**: Analyze multiple tickers at once
- **Default Symbol Support**: Automatically uses configured symbols when no input is provided
- **Comprehensive Metrics**: Displays key financial indicators for each ticker
- **Trend Classification**: Provides clear trend indicators (Bullish, Bearish, Strong Bullish, Strong Bearish)
- **Detailed Reporting**: Option to view detailed AI analysis for individual tickers
- **Visual Indicators**: Color-coded results for quick identification of market conditions

## Usage

### From Main Menu
1. Navigate to **Financial Analysis** section
2. Select **Multi-Ticker Screener**
3. Choose to either:
   - Enter specific tickers separated by commas (e.g., AAPL,MSFT,GOOGL)
   - Press Enter to use configured symbols

### Results Display
The screener presents results in a tabular format showing:
- Ticker symbol
- Current price
- 1-day return percentage
- 5-day return percentage
- RSI indicator
- Volatility measurement
- Trend classification
- Quantitative score

### Color Coding
- **Green**: Bullish trend indicators
- **Red**: Bearish trend indicators
- **Yellow**: Neutral or mixed signals

## Technical Implementation
- Leverages existing `QuantTechAnalyzer` for AI-powered analysis
- Uses configured symbols from `config/symbols` file as default
- Integrates with Datahub for data retrieval
- Maintains consistency with existing technical report formatting

## Example Output
```
MULTI-TICKER SCREENER RESULTS
================================================================================
Ticker     Price      1D %     5D %     RSI    Vol      Trend        Score   
--------------------------------------------------------------------------------
AAPL       $175.43    +1.25%   +3.42%   58.3   12.45%   Bullish      1.25    
MSFT       $340.21    -0.87%   +1.23%   62.1   8.92%    Bearish     -0.34    
GOOGL      $138.45    +2.15%   +5.67%   54.7   15.23%   Bullish      2.12    
================================================================================
Total symbols analyzed: 3
```

## Additional Features
- **Detailed Reports**: Select any ticker to view full AI-generated analysis
- **Real-time Data**: Uses most recent 90 days of data for analysis
- **Error Handling**: Gracefully handles missing or invalid symbols
- **Export Ready**: Results displayed in clean, structured format