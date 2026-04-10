# Changes Made to Remove Currency Symbols

## Summary
This update removes currency symbols ($USD) from financial reports to support tickers in different currencies (USD, EUR, etc.).

## Files Modified

### 1. menu_interface.py
- Removed dollar signs from technical report key metrics display
- Lines 363: Changed `"• Last Price: ${features['last_price']:.2f}"` to `"• Last Price: {features['last_price']:.2f}"`

### 2. FundamentalAnalisys.py
- Removed "USD" currency indicators from fundamental analysis reports
- Lines 45, 46, 47, 48, 62, 63, 64, 65: Removed " USD" from formatting strings
- Both Italian and English versions of reports updated

## Impact
- Reports are now currency-agnostic
- Works with any ticker regardless of underlying currency
- Maintains all numerical values and formatting
- Improves compatibility with international stocks