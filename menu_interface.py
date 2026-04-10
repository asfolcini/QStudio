# =======================================================================================================================
# QStudio - menu_interface.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import sys
import os
import json
import requests
import core.config as cfg
from core.Datahub import Datahub
from core.correlation_matrix.CorrelationMatrix import CorrelationMatrix
from core.yields.Yields import Yields
from core.charts.Charts import Charts
from core.random_equity import random_equity as random_eq
from core.strategy_evaluator import strategy_evaluator as cs
from core.hurst.hurst_exponent import Hurst_Exponent as Hurst_Exponent
import names
import webbrowser
from core.strategy.Hack_Strategy import Hack_Strategy
from core.strategy.Miner_Strategy import strategy_execute
import pandas
import numpy as np
from datetime import date

# Try to import colorama for colored output
try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# Import datetime for random_equity function
import datetime

# Cache management functions
def get_cache_dir():
    """Get the cache directory path"""
    return "cache"

def get_cache_filename(base_name):
    """Generate cache filename with current date"""
    today = date.today().strftime("%Y-%m-%d")
    return os.path.join(get_cache_dir(), f"{base_name}_{today}.json")

def is_cache_valid(cache_file):
    """Check if cache file exists and is from today"""
    if not os.path.exists(cache_file):
        return False
    
    # Check if file is from today (basic check)
    try:
        file_date = os.path.getctime(cache_file)
        today = date.today()
        # This is a simplified check - the file timestamp should be today
        return True
    except:
        return False

def load_from_cache(base_name):
    """Load data from cache if available"""
    cache_file = get_cache_filename(base_name)
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache file {cache_file}: {e}")
    return None

def save_to_cache(base_name, data):
    """Save data to cache"""
    cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache_file = get_cache_filename(base_name)
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Warning: Could not save to cache {cache_file}: {e}")
        return False

def clear_cache():
    """Clear all cached files"""
    cache_dir = get_cache_dir()
    if os.path.exists(cache_dir):
        import glob
        cache_files = glob.glob(os.path.join(cache_dir, "*"))
        for file in cache_files:
            try:
                os.remove(file)
                print(f"Cleared cache file: {os.path.basename(file)}")
            except Exception as e:
                print(f"Warning: Could not clear cache file {file}: {e}")
        print("All cache files cleared.")
    else:
        print("No cache directory found.")

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the QStudio header with enhanced styling"""
    if HAS_COLORAMA:
        print(Fore.CYAN + "-" * 120)
        print(Style.BRIGHT + Fore.CYAN + "               ___")
        print(Style.RESET_ALL + Fore.CYAN + "              /,_ \\    _,")
        print(Fore.CYAN + "              |/ )/   / |            Q S t u d i o")
        print(Fore.CYAN + "                //  _/  |            q u a n t   a n a l y s i s   p l a t f o r m   " + str(cfg.VERSION))
        print(Fore.CYAN + "               / ( /   _)")
        print(Fore.CYAN + "              /   `   _/)            copyright © "+ datetime.date.today().strftime("%Y") + " " + str(cfg.AUTHOR))
        print(Fore.CYAN + "              \\  ~=-   /,            www.surprisalx.com")
        print(Fore.CYAN + "       ^~^~^~^~^~^~^~^~^~^~^~^~")
        print(Style.RESET_ALL)
        print(Fore.CYAN + "-" * 120 + Style.RESET_ALL)
    else:
        print("-" * 120)
        print("               ___")
        print("              /,_ \\    _,")
        print("              |/ )/   / |            Q S t u d i o")
        print("                //  _/  |            q u a n t   a n a l y s i s   p l a t f o r m   " + str(cfg.VERSION))
        print("               / ( /   _)")
        print("              /   `   _/)            copyright © " + datetime.date.today().strftime("%Y") + " " + str(cfg.AUTHOR))
        print("              \\  ~=-   /,            www.surprisalx.com")
        print("       ^~^~^~^~^~^~^~^~^~^~^~^~")
        print()
        print("-" * 120)

def display_main_menu():
    """Display the main menu with enhanced styling"""
    clear_screen()
    display_header()
    
    if HAS_COLORAMA:
        print(Fore.WHITE + Style.BRIGHT + "\nMAIN MENU" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)
        print(Fore.GREEN + "1. Data Management" + Style.RESET_ALL)
        print(Fore.BLUE + "2. Financial Analysis" + Style.RESET_ALL)
        print(Fore.MAGENTA + "3. Visualization" + Style.RESET_ALL)
        print(Fore.YELLOW + "4. Strategy Analysis" + Style.RESET_ALL)
        print(Fore.RED + "5. Utilities" + Style.RESET_ALL)
        print(Fore.CYAN + "6. Documentation" + Style.RESET_ALL)
        print(Fore.MAGENTA + "9. Configuration" + Style.RESET_ALL)
        print(Fore.RED + "0. Exit" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)
    else:
        print("\nMAIN MENU")
        print("=" * 50)
        print("1. Data Management")
        print("2. Financial Analysis")
        print("3. Visualization")
        print("4. Strategy Analysis")
        print("5. Utilities")
        print("6. Documentation")
        print("9. Configuration")
        print("0. Exit")
        print("=" * 50)

def display_submenu(title, options):
    """Display a submenu with enhanced styling"""
    clear_screen()
    display_header()
    
    if HAS_COLORAMA:
        print(Fore.WHITE + Style.BRIGHT + f"\n{title}" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)
        # Define color mapping for submenu items
        colors = [Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.YELLOW, Fore.RED, Fore.CYAN, Fore.LIGHTMAGENTA_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX]
        for i, option in enumerate(options, 1):
            color = colors[i % len(colors)] if i <= len(colors) else Fore.WHITE
            print(color + f"{i}. {option}" + Style.RESET_ALL)
        print(Fore.CYAN + "0. Back to Main Menu" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)
    else:
        print(f"\n{title}")
        print("=" * 50)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Back to Main Menu")
        print("=" * 50)

def get_user_input(prompt):
    """Get user input with error handling"""
    try:
        if HAS_COLORAMA:
            return input(Fore.GREEN + prompt + Style.RESET_ALL).strip()
        else:
            return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except EOFError:
        print("\n\nExiting...")
        sys.exit(0)

def get_user_choice(max_choice):
    """Get a valid user choice"""
    while True:
        try:
            if HAS_COLORAMA:
                choice = int(get_user_input("Enter your choice: "))
            else:
                choice = int(input("Enter your choice: "))
            if 0 <= choice <= max_choice:
                return choice
            else:
                if HAS_COLORAMA:
                    print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
                else:
                    print("Invalid choice. Please try again.")
        except ValueError:
            if HAS_COLORAMA:
                print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)
            else:
                print("Please enter a valid number.")

def display_success(message):
    """Display a success message"""
    if HAS_COLORAMA:
        print(Fore.GREEN + "✓ " + message + Style.RESET_ALL)
    else:
        print("✓ " + message)

def display_error(message):
    """Display an error message"""
    if HAS_COLORAMA:
        print(Fore.RED + "✗ " + message + Style.RESET_ALL)
    else:
        print("✗ " + message)

def display_info(message):
    """Display an info message"""
    if HAS_COLORAMA:
        print(Fore.BLUE + "ℹ " + message + Style.RESET_ALL)
    else:
        print("ℹ " + message)

# Sub-menu handlers
def handle_correlation_matrix():
    """Handle correlation matrix operations"""
    options = [
        "Show Correlation Matrix (Configured Symbols)",
        "Show Correlation Matrix (Custom Symbols)",
        "Save Correlation Matrix (Configured Symbols)",
        "Save Correlation Matrix (Custom Symbols)"
    ]
    
    while True:
        display_submenu("CORRELATION MATRIX", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Show correlation matrix for configured symbols
            display_info("Generating correlation matrix for configured symbols...")
            correlation_matrix_show(True)
            display_success("Correlation matrix generated successfully!")
            input("\nPress Enter to continue...")
        elif choice == 2:
            # Show correlation matrix for custom symbols
            symbols = get_user_input("Enter symbols separated by commas (e.g. AAPL,GOOGL): ")
            if symbols:
                display_info(f"Generating correlation matrix for symbols: {symbols}")
                correlation_matrix_symbols(symbols, True)
                display_success("Correlation matrix generated successfully!")
                input("\nPress Enter to continue...")
        elif choice == 3:
            # Save correlation matrix for configured symbols
            display_info("Saving correlation matrix for configured symbols...")
            correlation_matrix_show(False)
            display_success("Correlation matrix saved successfully!")
            input("\nPress Enter to continue...")
        elif choice == 4:
            # Save correlation matrix for custom symbols
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Saving correlation matrix for symbols: {symbols}")
                correlation_matrix_symbols(symbols, False)
                display_success("Correlation matrix saved successfully!")
                input("\nPress Enter to continue...")
        elif choice == 0:
            break

def handle_yields_analysis():
    """Handle yields analysis operations"""
    options = [
        "Yields Analysis (Daily)",
        "Yields Analysis (Weekly)",
        "Yields Analysis (Monthly)",
        "Yields Analysis (Daily, Overlay)",
        "Yields Analysis (Weekly, Overlay)",
        "Yields Analysis (Monthly, Overlay)"
    ]
    
    while True:
        display_submenu("YIELDS ANALYSIS", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Yields Daily
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Analyzing daily yields for symbols: {symbols}")
                yields(symbols, True)
                display_success("Daily yields analysis completed!")
                input("\nPress Enter to continue...")
        elif choice == 2:
            # Yields Weekly
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Analyzing weekly yields for symbols: {symbols}")
                yields_weekly(symbols, True)
                display_success("Weekly yields analysis completed!")
                input("\nPress Enter to continue...")
        elif choice == 3:
            # Yields Monthly
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Analyzing monthly yields for symbols: {symbols}")
                yields_monthly(symbols, True)
                display_success("Monthly yields analysis completed!")
                input("\nPress Enter to continue...")
        elif choice == 4:
            # Yields Daily Overlay
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Analyzing daily yields (overlay) for symbols: {symbols}")
                yields(symbols, True, overlay=True)
                display_success("Daily yields overlay analysis completed!")
                input("\nPress Enter to continue...")
        elif choice == 5:
            # Yields Weekly Overlay
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Analyzing weekly yields (overlay) for symbols: {symbols}")
                yields_weekly(symbols, True, overlay=True)
                display_success("Weekly yields overlay analysis completed!")
                input("\nPress Enter to continue...")
        elif choice == 6:
            # Yields Monthly Overlay
            symbols = get_user_input("Enter symbols separated by commas: ")
            if symbols:
                display_info(f"Analyzing monthly yields (overlay) for symbols: {symbols}")
                yields_monthly(symbols, True, overlay=True)
                display_success("Monthly yields overlay analysis completed!")
                input("\nPress Enter to continue...")
        elif choice == 0:
            break

def handle_volatility_analysis():
    """Handle volatility analysis operations"""
    symbols = get_user_input("Enter symbols separated by commas (leave blank for configured symbols): ")
    if symbols:
        display_info(f"Calculating volatility for symbols: {symbols}")
        volatility(symbols)
        display_success("Volatility calculation completed!")
    else:
        display_info("Calculating volatility for configured symbols...")
        volatility(None)
        display_success("Volatility calculation completed!")
    input("\nPress Enter to continue...")

def handle_autocorrelation():
    """Handle autocorrelation operations"""
    symbols = get_user_input("Enter symbols separated by commas: ")
    if symbols:
        display_info(f"Calculating autocorrelation for symbols: {symbols}")
        autocorrelation(symbols, True)
        display_success("Autocorrelation calculation completed!")
    else:
        display_info("Calculating autocorrelation for configured symbols...")
        autocorrelation(None, True)
        display_success("Autocorrelation calculation completed!")
    input("\nPress Enter to continue...")

def handle_market_behavior_detection():
    """Handle market behavior detection operations"""
    symbols = get_user_input("Enter symbols separated by commas (leave blank for configured symbols): ")
    if symbols:
        detect_market_behavior(symbols)
    else:
        detect_market_behavior(None)
    input("\nPress Enter to continue...")


def handle_screener():
    """Handle multi-ticker screener operations"""
    try:
        # Check if we have cached results for today
        cache_data = load_from_cache("screener")
        if cache_data is not None:
            display_info("Loading cached screener results...")
            results = cache_data
        else:
            # Get input parameter - allow user to specify symbols or use configured ones
            symbols_input = get_user_input("Enter symbols separated by commas (leave blank for configured symbols): ")
            
            # Load data using Datahub
            s = Datahub(loadfromconfig=True)
            
            # Determine which symbols to analyze
            if symbols_input.strip():
                symbols = [symbol.strip().upper() for symbol in symbols_input.split(',')]
                # Validate each symbol exists
                valid_symbols = []
                for symbol in symbols:
                    try:
                        # Try to load data for this symbol
                        dataset = s.load_data(symbol, 90)
                        if not dataset.empty:
                            valid_symbols.append(symbol)
                        else:
                            display_error(f"No data available for {symbol}.")
                    except Exception as e:
                        display_error(f"Failed to load data for {symbol}: {e}")
            else:
                # Use configured symbols
                symbols = s.get_symbols()
                valid_symbols = []
                # Filter out symbols that don't have data
                for symbol in symbols:
                    try:
                        dataset = s.load_data(symbol, 90)
                        if not dataset.empty:
                            valid_symbols.append(symbol)
                        else:
                            display_info(f"No data available for {symbol}, skipping...")
                    except Exception as e:
                        display_info(f"Failed to load data for {symbol}: {e}")
                
                if not valid_symbols:
                    display_error("No symbols with available data found.")
                    input("\nPress Enter to continue...")
                    return
                    
                symbols = valid_symbols
                
            if not symbols:
                display_error("No valid symbols to analyze.")
                input("\nPress Enter to continue...")
                return
                
            display_info(f"Analyzing {len(symbols)} symbols...")
            
            # Import QuantTechAnalyzer
            from core.quant_tech_analyzer import QuantTechAnalyzer
            
            # Create analyzer instance
            analyzer = QuantTechAnalyzer()
            
            # Store results
            results = []
            
            # Process each symbol
            for ticker in symbols:
                display_info(f"Analyzing {ticker}...")
                try:
                    # Load data for this symbol
                    dataset = s.load_data(ticker, 90)
                    
                    if dataset.empty:
                        display_error(f"No data available for {ticker}.")
                        continue
                        
                    # Generate AI-powered report
                    result = analyzer.analyze(ticker, dataset)
                    
                    # Extract key features for screening
                    features = result["features"]
                    
                    # Determine trend based on features
                    trend = ""
                    if features["trend"] == "bullish":
                        if features["rsi"] > 70:
                            trend = "Strong Bullish"
                        else:
                            trend = "Bullish"
                    else:
                        if features["rsi"] < 30:
                            trend = "Strong Bearish"
                        else:
                            trend = "Bearish"
                    
                    # Enhanced analysis for structural elements
                    # Supply/Demand Zone Detection (simple VWAP approach)
                    vwap = features.get('vwap', features['last_price'])  # Default to current price
                    supply_zone = vwap * 1.02 if features['last_price'] > vwap else None
                    demand_zone = vwap * 0.98 if features['last_price'] < vwap else None
                    
                    # Support/Resistance Level Detection (simplified)
                    # We'll use price action patterns to estimate levels
                    support_level = features['last_price'] * 0.95 if features['trend'] == "bearish" else None
                    resistance_level = features['last_price'] * 1.05 if features['trend'] == "bullish" else None
                    
                    # Pattern Detection (simplified)
                    patterns = []
                    if features['rsi'] > 70 and features['trend'] == "bearish":
                        patterns.append("Overbought Reversal")
                    elif features['rsi'] < 30 and features['trend'] == "bullish":
                        patterns.append("Oversold Reversal")
                    elif features['rsi'] > 70 and features['trend'] == "bullish":
                        patterns.append("Bullish Flag")
                    elif features['rsi'] < 30 and features['trend'] == "bearish":
                        patterns.append("Bearish Flag")
                        
                    # Trading Signal Generation
                    signal = "None"
                    reliability = 0
                    
                    # Bullish signals
                    if features['trend'] == "bullish" and features['rsi'] < 50:
                        signal = "BUY"
                        reliability = min(100, 60 + (features['rsi'] / 2))  # Higher reliability for lower RSI
                    elif features['trend'] == "bullish" and features['rsi'] > 70:
                        signal = "BUY"  
                        reliability = min(100, 70 + ((features['rsi'] - 70) / 2))  # Moderate reliability for overbought
                    elif features['trend'] == "bearish" and features['rsi'] < 30:
                        signal = "SELL"
                        reliability = min(100, 60 + ((30 - features['rsi']) / 2))  # Higher reliability for oversold
                        
                    # Bearish signals  
                    if features['trend'] == "bearish" and features['rsi'] > 50:
                        signal = "SELL"
                        reliability = min(100, 60 + ((100 - features['rsi']) / 2))  # Higher reliability for higher RSI
                        
                    # Add to results with enhanced information
                    results.append({
                        "ticker": ticker,
                        "price": features["last_price"],
                        "change_1d": features["ret_1d"],
                        "change_5d": features["ret_5d"],
                        "rsi": features["rsi"],
                        "volatility": features["volatility"],
                        "trend": trend,
                        "quant_score": features["quant_score"],
                        "llm_report": result["llm_report"],
                        "supply_zone": supply_zone,
                        "demand_zone": demand_zone,
                        "support_level": support_level,
                        "resistance_level": resistance_level,
                        "patterns": patterns,
                        "signal": signal,
                        "reliability": reliability,
                        "volume": features.get("volume", 0)
                    })
                    
                except Exception as e:
                    display_error(f"Error analyzing {ticker}: {e}")
                    continue
            
            # Save to cache
            save_to_cache("screener", results)
        
        # Display results using prettytable for better formatting
        clear_screen()
        display_header()
        print(f"\nMULTI-TICKER SCREENER RESULTS")
        
        # Import prettytable for better formatting
        from prettytable import PrettyTable
        
        # Create prettytable with appropriate column names
        table = PrettyTable()
        table.field_names = ["Ticker", "Price", "1D %", "5D %", "RSI", "Vol", "Trend", "Score", "Supply", "Demand", "S/R", "Sig", "Rel"]
        table.align["Ticker"] = "l"
        table.align["Price"] = "r"
        table.align["1D %"] = "r"
        table.align["5D %"] = "r"
        table.align["RSI"] = "r"
        table.align["Vol"] = "r"
        table.align["Trend"] = "l"
        table.align["Score"] = "r"
        table.align["Supply"] = "r"
        table.align["Demand"] = "r"
        table.align["S/R"] = "l"
        table.align["Sig"] = "c"
        table.align["Rel"] = "r"
        
        # Add rows to table
        for result in results:
            # Format values nicely (no currency symbols)
            price_str = f"{result['price']:.2f}"
            change_1d_str = f"{result['change_1d']:+.2%}"
            change_5d_str = f"{result['change_5d']:+.2%}"
            rsi_str = f"{result['rsi']:.1f}"
            vol_str = f"{result['volatility']:.2%}"
            trend_str = result['trend']
            score_str = f"{result['quant_score']:.2f}"
            
            # Supply/Demand zone display - using more realistic approach
            supply_str = "-"
            demand_str = "-"
            
            # Calculate based on price relationship to moving averages
            if result['price'] > features.get('sma20', result['price']) * 1.02:
                supply_str = f"{result['price'] * 1.02:.2f}"
            elif result['price'] < features.get('sma20', result['price']) * 0.98:
                demand_str = f"{result['price'] * 0.98:.2f}"
            
            # Support/Resistance display
            sr_str = ""
            if result['support_level'] and result['resistance_level']:
                sr_str = f"S:{result['support_level']:.2f}/R:{result['resistance_level']:.2f}"
            elif result['support_level']:
                sr_str = f"S:{result['support_level']:.2f}"
            elif result['resistance_level']:
                sr_str = f"R:{result['resistance_level']:.2f}"
            else:
                sr_str = "-"
            
            # Signal and reliability
            signal_str = result['signal']
            reliability_str = f"{result['reliability']:.0f}%" if result['reliability'] > 0 else "-"
            
            # Add row to table
            table.add_row([
                result['ticker'],
                price_str,
                change_1d_str,
                change_5d_str,
                rsi_str,
                vol_str,
                trend_str,
                score_str,
                supply_str,
                demand_str,
                sr_str,
                signal_str,
                reliability_str
            ])
        
        # Print the table
        print(table)
        print(f"\nTotal symbols analyzed: {len(results)}")
        
        # Ask if user wants to see detailed report for any symbol
        if results:
            detail_ticker = get_user_input("\nEnter ticker symbol for detailed report (or press Enter to continue): ").upper().strip()
            if detail_ticker and detail_ticker in [r['ticker'] for r in results]:
                # Find and show detailed report
                detailed_result = next((r for r in results if r['ticker'] == detail_ticker), None)
                if detailed_result:
                    clear_screen()
                    display_header()
                    print(f"\nDETAILED ANALYSIS FOR {detail_ticker}")
                    print("=" * 100)
                    
                    # Show key metrics using prettytable
                    metrics_table = PrettyTable()
                    metrics_table.field_names = ["Metric", "Value"]
                    metrics_table.align["Metric"] = "l"
                    metrics_table.align["Value"] = "r"
                    metrics_table.add_row(["Current Price", f"{detailed_result['price']:.2f}"])
                    metrics_table.add_row(["1D Return", f"{detailed_result['change_1d']:.2%}"])
                    metrics_table.add_row(["5D Return", f"{detailed_result['change_5d']:.2%}"])
                    metrics_table.add_row(["RSI", f"{detailed_result['rsi']:.1f}"])
                    metrics_table.add_row(["Volatility", f"{detailed_result['volatility']:.2%}"])
                    metrics_table.add_row(["Trend", detailed_result['trend']])
                    metrics_table.add_row(["Quant Score", f"{detailed_result['quant_score']:.2f}"])
                    metrics_table.add_row(["Volume", f"{detailed_result['volume']:,.0f}"])
                    print(metrics_table)
                    
                    # Show structural elements
                    print("\nSTRUCTURAL ELEMENTS")
                    struct_table = PrettyTable()
                    struct_table.field_names = ["Element", "Value"]
                    struct_table.align["Element"] = "l"
                    struct_table.align["Value"] = "r"
                    
                    # More comprehensive structural analysis
                    struct_table.add_row(["Current Price", f"{detailed_result['price']:.2f}"])
                    struct_table.add_row(["20-Day SMA", f"{features.get('sma20', detailed_result['price']):.2f}"])
                    struct_table.add_row(["50-Day SMA", f"{features.get('sma50', detailed_result['price']):.2f}"])
                    
                    # Supply/Demand Zone (based on price relationship)
                    if detailed_result['price'] > features.get('sma20', detailed_result['price']) * 1.02:
                        struct_table.add_row(["Supply Zone", f"{detailed_result['price'] * 1.02:.2f}"])
                    elif detailed_result['price'] < features.get('sma20', detailed_result['price']) * 0.98:
                        struct_table.add_row(["Demand Zone", f"{detailed_result['price'] * 0.98:.2f}"])
                        
                    if detailed_result['support_level']:
                        struct_table.add_row(["Support Level", f"{detailed_result['support_level']:.2f}"])
                    if detailed_result['resistance_level']:
                        struct_table.add_row(["Resistance Level", f"{detailed_result['resistance_level']:.2f}"])
                        
                    print(struct_table)
                    
                    # Show patterns
                    if detailed_result['patterns']:
                        pattern_table = PrettyTable()
                        pattern_table.field_names = ["Detected Patterns"]
                        pattern_table.align["Detected Patterns"] = "l"
                        for pattern in detailed_result['patterns']:
                            pattern_table.add_row([pattern])
                        print("\nPATTERNS DETECTED")
                        print(pattern_table)
                    
                    # Show trading signals
                    if detailed_result['signal'] != "None":
                        signal_table = PrettyTable()
                        signal_table.field_names = ["Trading Signal", "Reliability"]
                        signal_table.align["Trading Signal"] = "l"
                        signal_table.align["Reliability"] = "r"
                        signal_table.add_row([detailed_result['signal'], f"{detailed_result['reliability']:.1f}%"])
                        print("\nTRADING SIGNAL")
                        print(signal_table)
                    
                    # Show AI-generated report
                    print("\nAI ANALYSIS")
                    if HAS_COLORAMA:
                        print(Fore.CYAN + "AI-GENERATED CONTENT" + Style.RESET_ALL)
                    else:
                        print("AI-GENERATED CONTENT")
                    print("-" * 70)
                    print(detailed_result['llm_report'])
                    print("-" * 70)
                    print("=" * 100)
                    input("\nPress Enter to continue...")
        
        input("\nPress Enter to continue...")
        
    except ValueError as e:
        if "LLM_API_KEY" in str(e):
            display_error("LLM_API_KEY is not set in configuration. Please configure it in the Configuration menu.")
        else:
            display_error(f"Configuration error: {e}")
        input("\nPress Enter to continue...")
    except Exception as e:
        display_error(f"Failed to generate screener results: {e}")
        input("\nPress Enter to continue...")
        return
                
        symbols = valid_symbols
            
        if not symbols:
            display_error("No valid symbols to analyze.")
            input("\nPress Enter to continue...")
            return
            
        display_info(f"Analyzing {len(symbols)} symbols...")
        
        # Import QuantTechAnalyzer
        from core.quant_tech_analyzer import QuantTechAnalyzer
        
        # Create analyzer instance
        analyzer = QuantTechAnalyzer()
        
        # Store results
        results = []
        
        # Process each symbol
        for ticker in symbols:
            display_info(f"Analyzing {ticker}...")
            try:
                # Load data for this symbol
                dataset = s.load_data(ticker, 90)
                
                if dataset.empty:
                    display_error(f"No data available for {ticker}.")
                    continue
                    
                # Generate AI-powered report
                result = analyzer.analyze(ticker, dataset)
                
                # Extract key features for screening
                features = result["features"]
                
                # Determine trend based on features
                trend = ""
                if features["trend"] == "bullish":
                    if features["rsi"] > 70:
                        trend = "Strong Bullish"
                    else:
                        trend = "Bullish"
                else:
                    if features["rsi"] < 30:
                        trend = "Strong Bearish"
                    else:
                        trend = "Bearish"
                
                # Enhanced analysis for structural elements
                # Supply/Demand Zone Detection (simple VWAP approach)
                vwap = features.get('vwap', features['last_price'])  # Default to current price
                supply_zone = vwap * 1.02 if features['last_price'] > vwap else None
                demand_zone = vwap * 0.98 if features['last_price'] < vwap else None
                
                # Support/Resistance Level Detection (simplified)
                # We'll use price action patterns to estimate levels
                support_level = features['last_price'] * 0.95 if features['trend'] == "bearish" else None
                resistance_level = features['last_price'] * 1.05 if features['trend'] == "bullish" else None
                
                # Pattern Detection (simplified)
                patterns = []
                if features['rsi'] > 70 and features['trend'] == "bearish":
                    patterns.append("Overbought Reversal")
                elif features['rsi'] < 30 and features['trend'] == "bullish":
                    patterns.append("Oversold Reversal")
                elif features['rsi'] > 70 and features['trend'] == "bullish":
                    patterns.append("Bullish Flag")
                elif features['rsi'] < 30 and features['trend'] == "bearish":
                    patterns.append("Bearish Flag")
                    
                # Trading Signal Generation
                signal = "None"
                reliability = 0
                
                # Bullish signals
                if features['trend'] == "bullish" and features['rsi'] < 50:
                    signal = "BUY"
                    reliability = min(100, 60 + (features['rsi'] / 2))  # Higher reliability for lower RSI
                elif features['trend'] == "bullish" and features['rsi'] > 70:
                    signal = "BUY"  
                    reliability = min(100, 70 + ((features['rsi'] - 70) / 2))  # Moderate reliability for overbought
                elif features['trend'] == "bearish" and features['rsi'] < 30:
                    signal = "SELL"
                    reliability = min(100, 60 + ((30 - features['rsi']) / 2))  # Higher reliability for oversold
                    
                # Bearish signals  
                if features['trend'] == "bearish" and features['rsi'] > 50:
                    signal = "SELL"
                    reliability = min(100, 60 + ((100 - features['rsi']) / 2))  # Higher reliability for higher RSI
                    
                # Add to results with enhanced information
                results.append({
                    "ticker": ticker,
                    "price": features["last_price"],
                    "change_1d": features["ret_1d"],
                    "change_5d": features["ret_5d"],
                    "rsi": features["rsi"],
                    "volatility": features["volatility"],
                    "trend": trend,
                    "quant_score": features["quant_score"],
                    "llm_report": result["llm_report"],
                    "supply_zone": supply_zone,
                    "demand_zone": demand_zone,
                    "support_level": support_level,
                    "resistance_level": resistance_level,
                    "patterns": patterns,
                    "signal": signal,
                    "reliability": reliability,
                    "volume": features.get("volume", 0)
                })
                
            except Exception as e:
                display_error(f"Error analyzing {ticker}: {e}")
                continue
        
        # Display results in enhanced table format
        clear_screen()
        display_header()
        print(f"\nMULTI-TICKER SCREENER RESULTS")
        print("=" * 180)
        
        # Print column headers with extended fields
        print(f"{'Ticker':<8} {'Price':<10} {'1D %':<8} {'5D %':<8} {'RSI':<6} {'Vol':<8} {'Trend':<12} {'Score':<8} {'Supply':<10} {'Demand':<10} {'S/R':<15} {'Sig':<6} {'Rel':<6}")
        print("-" * 180)
        
        # Print each row with enhanced information
        for result in results:
            # Format values nicely - WITHOUT currency symbols
            price_str = f"{result['price']:.2f}"
            change_1d_str = f"{result['change_1d']:+.2%}".rjust(8)
            change_5d_str = f"{result['change_5d']:+.2%}".rjust(8)
            rsi_str = f"{result['rsi']:.1f}".rjust(6)
            vol_str = f"{result['volatility']:.2%}".rjust(8)
            trend_str = result['trend'].ljust(12)
            score_str = f"{result['quant_score']:.2f}".rjust(8)
            
            # Supply/Demand zone display - using more realistic approach
            supply_str = "-"
            demand_str = "-"
            
            # Calculate based on price relationship to moving averages
            if result['price'] > features.get('sma20', result['price']) * 1.02:
                supply_str = f"{result['price'] * 1.02:.2f}"
            elif result['price'] < features.get('sma20', result['price']) * 0.98:
                demand_str = f"{result['price'] * 0.98:.2f}"
            
            # Support/Resistance display
            sr_str = ""
            if result['support_level'] and result['resistance_level']:
                sr_str = f"S:{result['support_level']:.2f}/R:{result['resistance_level']:.2f}"
            elif result['support_level']:
                sr_str = f"S:{result['support_level']:.2f}"
            elif result['resistance_level']:
                sr_str = f"R:{result['resistance_level']:.2f}"
            else:
                sr_str = "-"
            
            # Signal and reliability
            signal_str = result['signal']
            reliability_str = f"{result['reliability']:.0f}%" if result['reliability'] > 0 else "-"
            
            # Color coding based on trend and signal
            if "Bullish" in result['trend'] and result['signal'] == "BUY":
                if HAS_COLORAMA:
                    print(Fore.GREEN + f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}" + Style.RESET_ALL)
                else:
                    print(f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}")
            elif "Bearish" in result['trend'] and result['signal'] == "SELL":
                if HAS_COLORAMA:
                    print(Fore.RED + f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}" + Style.RESET_ALL)
                else:
                    print(f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}")
            elif result['signal'] == "BUY":
                if HAS_COLORAMA:
                    print(Fore.LIGHTGREEN_EX + f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}" + Style.RESET_ALL)
                else:
                    print(f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}")
            elif result['signal'] == "SELL":
                if HAS_COLORAMA:
                    print(Fore.LIGHTRED_EX + f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}" + Style.RESET_ALL)
                else:
                    print(f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}")
            else:
                if HAS_COLORAMA:
                    print(Fore.YELLOW + f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}" + Style.RESET_ALL)
                else:
                    print(f"{result['ticker']:<8} {price_str:<10} {change_1d_str} {change_5d_str} {rsi_str} {vol_str} {trend_str} {score_str} {supply_str:<10} {demand_str:<10} {sr_str:<15} {signal_str:<6} {reliability_str}")
        
        print("-" * 180)
        print(f"Total symbols analyzed: {len(results)}")
        
        # Ask if user wants to see detailed report for any symbol
        if results:
            detail_ticker = get_user_input("\nEnter ticker symbol for detailed report (or press Enter to continue): ").upper().strip()
            if detail_ticker and detail_ticker in [r['ticker'] for r in results]:
                # Find and show detailed report
                detailed_result = next((r for r in results if r['ticker'] == detail_ticker), None)
                if detailed_result:
                    clear_screen()
                    display_header()
                    print(f"\nDETAILED ANALYSIS FOR {detail_ticker}")
                    print("=" * 160)
                    
                    # Show key metrics
                    print("KEY METRICS")
                    print(f"   • Last Price: ${detailed_result['price']:.2f}")
                    print(f"   • 1D Return: {detailed_result['change_1d']:.2%}")
                    print(f"   • 5D Return: {detailed_result['change_5d']:.2%}")
                    print(f"   • RSI: {detailed_result['rsi']:.1f}")
                    print(f"   • Volatility: {detailed_result['volatility']:.2%} (20-day)")
                    print(f"   • Trend: {detailed_result['trend']}")
                    print(f"   • Quant Score: {detailed_result['quant_score']:.2f}")
                    print(f"   • Volume: {detailed_result['volume']:,.0f}")
                    
                    # Show structural elements
                    print("\nSTRUCTURAL ELEMENTS")
                    # More comprehensive structural analysis
                    print(f"   • Current Price: {detailed_result['price']:.2f}")
                    print(f"   • 20-Day SMA: {features.get('sma20', detailed_result['price']):.2f}")
                    print(f"   • 50-Day SMA: {features.get('sma50', detailed_result['price']):.2f}")
                    
                    # Supply/Demand Zone (based on price relationship)
                    if detailed_result['price'] > features.get('sma20', detailed_result['price']) * 1.02:
                        print(f"   • Supply Zone: {detailed_result['price'] * 1.02:.2f}")
                    elif detailed_result['price'] < features.get('sma20', detailed_result['price']) * 0.98:
                        print(f"   • Demand Zone: {detailed_result['price'] * 0.98:.2f}")
                        
                    if detailed_result['support_level']:
                        print(f"   • Support Level: {detailed_result['support_level']:.2f}")
                    if detailed_result['resistance_level']:
                        print(f"   • Resistance Level: {detailed_result['resistance_level']:.2f}")
                        
                    # Show patterns
                    if detailed_result['patterns']:
                        print(f"   • Detected Patterns: {', '.join(detailed_result['patterns'])}")
                    
                    # Show trading signals
                    if detailed_result['signal'] != "None":
                        print(f"   • Trading Signal: {detailed_result['signal']}")
                        print(f"   • Reliability: {detailed_result['reliability']:.1f}%")
                    
                    # Show AI-generated report
                    print("\nAI ANALYSIS")
                    if HAS_COLORAMA:
                        print(Fore.CYAN + "AI-GENERATED CONTENT" + Style.RESET_ALL)
                    else:
                        print("AI-GENERATED CONTENT")
                    print("-" * 70)
                    print(detailed_result['llm_report'])
                    print("-" * 70)
                    print("=" * 160)
                    input("\nPress Enter to continue...")
        
        input("\nPress Enter to continue...")
        
    except ValueError as e:
        if "LLM_API_KEY" in str(e):
            display_error("LLM_API_KEY is not set in configuration. Please configure it in the Configuration menu.")
        else:
            display_error(f"Configuration error: {e}")
        input("\nPress Enter to continue...")
    except Exception as e:
        display_error(f"Failed to generate screener results: {e}")
        input("\nPress Enter to continue...")

def handle_technical_report():
    """Handle technical report operations using AI-powered analysis"""
    try:
        # Get input parameter
        ticker = get_user_input("Enter ticker symbol (e.g., AAPL): ").upper().strip()
        
        if not ticker:
            display_error("Ticker symbol is required.")
            input("\nPress Enter to continue...")
            return
            
        # Check if we have cached results for today for this ticker
        cache_data = load_from_cache(f"ai_report_{ticker}")
        if cache_data is not None:
            display_info(f"Loading cached AI report for {ticker}...")
            result = cache_data
        else:
            display_info(f"Generating AI-powered technical report for {ticker}...")
            
            # Load data using Datahub
            s = Datahub(loadfromconfig=True)
            
            # Check if data exists for the ticker
            if ticker not in s.get_symbols():
                # Try to load the data directly
                try:
                    dataset = s.load_data(ticker, 90)  # Load last 90 days of data
                    if dataset.empty:
                        display_error(f"No data available for {ticker}.")
                        input("\nPress Enter to continue...")
                        return
                except:
                    display_error(f"Failed to load data for {ticker}. Please make sure the ticker is valid and data is available.")
                    input("\nPress Enter to continue...")
                    return
            else:
                dataset = s.load_data(ticker, 90)  # Load last 90 days of data
                
            if dataset.empty:
                display_error(f"No data available for {ticker}.")
                input("\nPress Enter to continue...")
                return
            
            # Import QuantTechAnalyzer
            from core.quant_tech_analyzer import QuantTechAnalyzer
            
            # Create analyzer instance
            analyzer = QuantTechAnalyzer()
            
            # Generate AI-powered report
            result = analyzer.analyze(ticker, dataset)
            
            # Save to cache
            save_to_cache(f"ai_report_{ticker}", result)
        
        # Display the report
        clear_screen()
        display_header()
        print(f"\nAI-POWERED TECHNICAL REPORT: {ticker}")
        print("=" * 70)
        
        # Display features
        features = result["features"]
        print("1. KEY METRICS")
        print(f"   • Last Price: {features['last_price']:.2f}")
        print(f"   • 1D Return: {features['ret_1d']:.2%}")
        print(f"   • 5D Return: {features['ret_5d']:.2%}")
        print(f"   • RSI: {features['rsi']:.1f}")
        print(f"   • Volatility: {features['volatility']:.2%} (20-day)")
        print(f"   • Trend: {features['trend'].upper()}")
        print(f"   • Quant Score: {features['quant_score']:.2f}")
        
        # Display AI-generated report
        print("\n2. AI ANALYSIS")
        if HAS_COLORAMA:
            print(Fore.CYAN + "AI-GENERATED CONTENT" + Style.RESET_ALL)
        else:
            print("AI-GENERATED CONTENT")
        print("-" * 70)
        print(result["llm_report"])
        print("-" * 70)
        
        print("\n" + "=" * 70)
        display_success("AI-powered technical report generated successfully!")
        input("\nPress Enter to continue...")
        
    except ValueError as e:
        if "LLM_API_KEY" in str(e):
            display_error("LLM_API_KEY is not set in configuration. Please configure it in the Configuration menu.")
        else:
            display_error(f"Configuration error: {e}")
        input("\nPress Enter to continue...")
    except requests.exceptions.RequestException as e:
        display_error(f"Failed to connect to LLM API: {e}")
        input("\nPress Enter to continue...")
    except Exception as e:
        display_error(f"Failed to generate technical report: {e}")
        input("\nPress Enter to continue...")
            

        
    except Exception as e:
        display_error(f"Failed to generate technical report: {e}")
        input("\nPress Enter to continue...")

def handle_chart_line():
    """Handle line chart operations"""
    symbols = get_user_input("Enter symbols separated by commas: ")
    if symbols:
        display_info(f"Generating line chart for symbols: {symbols}")
        chart(symbols, True, 9999, False)
        display_success("Line chart generated successfully!")
    else:
        display_info("Generating line chart for configured symbols...")
        chart(None, True, 9999, False)
        display_success("Line chart generated successfully!")
    input("\nPress Enter to continue...")

def handle_chart_candlesticks():
    """Handle candlestick chart operations"""
    symbols = get_user_input("Enter symbols separated by commas: ")
    if symbols:
        display_info(f"Generating candlestick chart for symbols: {symbols}")
        chart(symbols, True, 9999, True)
        display_success("Candlestick chart generated successfully!")
    else:
        display_info("Generating candlestick chart for configured symbols...")
        chart(None, True, 9999, True)
        display_success("Candlestick chart generated successfully!")
    input("\nPress Enter to continue...")

def handle_strategy_evaluator():
    """Handle strategy evaluator operations"""
    folder = get_user_input("Enter folder path (leave blank for default): ")
    if not folder:
        folder = cfg.EQUITY_OUTPUT
    report = get_user_input("Include report? (y/n): ").lower() == 'y'
    display_info(f"Running strategy evaluator in folder: {folder}")
    check_strategy(folder, report)
    display_success("Strategy evaluation completed!")
    input("\nPress Enter to continue...")

def handle_single_strategy_evaluator():
    """Handle single strategy evaluator operations"""
    filepath = get_user_input("Enter equity file path: ")
    if filepath:
        report = get_user_input("Include report? (y/n): ").lower() == 'y'
        display_info(f"Running single strategy evaluator for file: {filepath}")
        check_single_strategy(filepath, report)
        display_success("Single strategy evaluation completed!")
    input("\nPress Enter to continue...")

def handle_hacking_strategies():
    """Handle hacking strategies operations"""
    symbols = get_user_input("Enter symbols separated by commas: ")
    qty = get_user_input("Enter quantity: ")
    if symbols and qty.isdigit():
        display_info(f"Hacking strategy for symbols: {symbols} with quantity: {qty}")
        hack(symbols, int(qty), None)
        display_success("Hacking strategy analysis completed!")
    else:
        display_error("Invalid input. Please enter valid symbols and quantity.")
    input("\nPress Enter to continue...")

def handle_stock_miner_strategies():
    """Handle stock miner strategies operations"""
    strategy_file = get_user_input("Enter strategy config file path: ")
    if strategy_file:
        mode = get_user_input("Enter mode (backtest/signal/optimize): ").lower()
        if mode in ['backtest', 'signal', 'optimize']:
            display_info(f"Executing strategy from file: {strategy_file} in mode: {mode}")
            # This is a simplified version - in practice, we'd pass the mode correctly
            strategy_execute(strategy_file, mode)
            display_success("Stock miner strategy execution completed!")
        else:
            display_error("Invalid mode. Please choose backtest, signal, or optimize.")
    else:
        display_error("No strategy file specified.")
    input("\nPress Enter to continue...")

def handle_random_equities_generation():
    """Handle random equities generation operations"""
    folder = get_user_input("Enter folder path (leave blank for default): ")
    if not folder:
        folder = cfg.EQUITY_OUTPUT
    nr = get_user_input("Enter number of equities to generate: ")
    if nr.isdigit():
        display_info(f"Generating {nr} random equities in folder: {folder}")
        random_equity(folder, int(nr))
        display_success("Random equities generated successfully!")
    else:
        display_error("Please enter a valid number.")
    input("\nPress Enter to continue...")

def handle_random_equities_cleanup():
    """Handle random equities cleanup operations"""
    folder = get_user_input("Enter folder path (leave blank for default): ")
    if not folder:
        folder = cfg.EQUITY_OUTPUT
    display_info(f"Cleaning folder: {folder}")
    random_equity_delete(folder)
    display_success("Random equity folder cleaned successfully!")
    input("\nPress Enter to continue...")

# Data Management Functions
def handle_data_management():
    """Handle data management operations"""
    options = [
        "Update All Data",
        "Update Specific Symbols",
        "Show Data Repository",
        "Show Configured Symbols",
        "Add Symbol",
        "Remove Symbol",
        "Purge Data Repository"
    ]
    
    while True:
        display_submenu("DATA MANAGEMENT", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Update All Data
            display_info("Updating all data from Yahoo Finance...")
            datahub_update_all()
            display_success("All data updated successfully!")
            input("\nPress Enter to continue...")
        elif choice == 2:
            # Update Specific Symbols
            symbols = get_user_input("Enter symbols separated by commas (e.g., AAPL,GOOGL): ")
            if symbols:
                display_info(f"Updating symbols: {symbols}")
                datahub_update(symbols)
                display_success("Symbols updated successfully!")
                input("\nPress Enter to continue...")
        elif choice == 3:
            # Show Data Repository
            display_info("Showing data repository contents...")
            datahub_show()
            display_success("Repository contents displayed!")
            input("\nPress Enter to continue...")
        elif choice == 4:
            # Show Configured Symbols
            display_info("Showing configured symbols...")
            config_symbols()
            display_success("Configured symbols displayed!")
            input("\nPress Enter to continue...")
        elif choice == 5:
            # Add Symbol
            handle_add_symbol()
        elif choice == 6:
            # Remove Symbol
            handle_remove_symbol()
        elif choice == 7:
            # Purge Data Repository
            handle_purge_repository()
        elif choice == 0:
            break

# Financial Analysis Functions
def handle_financial_analysis():
    """Handle financial analysis operations"""
    options = [
        "Correlation Matrix",
        "Yields Analysis",
        "Volatility Analysis",
        "Autocorrelation",
        "Market Behavior Detection",
        "AI-Powered Technical Report",
        "Multi-Ticker Screener"
    ]
    
    while True:
        display_submenu("FINANCIAL ANALYSIS", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Correlation Matrix
            handle_correlation_matrix()
        elif choice == 2:
            # Yields Analysis
            handle_yields_analysis()
        elif choice == 3:
            # Volatility Analysis
            handle_volatility_analysis()
        elif choice == 4:
            # Autocorrelation
            handle_autocorrelation()
        elif choice == 5:
            # Market Behavior Detection
            handle_market_behavior_detection()
        elif choice == 6:
            # Technical Report
            handle_technical_report()
        elif choice == 7:
            # Multi-Ticker Screener
            handle_screener()
        elif choice == 0:
            break

# Visualization Functions
def handle_visualization():
    """Handle visualization operations"""
    options = [
        "Chart (Line)",
        "Chart (Candlesticks)"
    ]
    
    while True:
        display_submenu("VISUALIZATION", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Chart Line
            handle_chart_line()
        elif choice == 2:
            # Chart Candlesticks
            handle_chart_candlesticks()
        elif choice == 0:
            break

# Strategy Analysis Functions
def handle_strategy_analysis():
    """Handle strategy analysis operations"""
    options = [
        "Strategy Evaluator",
        "Single Strategy Evaluator",
        "Hacking Strategies",
        "Stock Miner Strategies"
    ]
    
    while True:
        display_submenu("STRATEGY ANALYSIS", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Strategy Evaluator
            handle_strategy_evaluator()
        elif choice == 2:
            # Single Strategy Evaluator
            handle_single_strategy_evaluator()
        elif choice == 3:
            # Hacking Strategies
            handle_hacking_strategies()
        elif choice == 4:
            # Stock Miner Strategies
            handle_stock_miner_strategies()
        elif choice == 0:
            break

# Utilities Functions
def handle_add_symbol():
    """Handle adding a symbol to the configuration"""
    try:
        # Read current symbols
        symbols_file = cfg.SYMBOLS_FILEPATH
        if os.path.exists(symbols_file):
            with open(symbols_file, 'r') as f:
                current_symbols = f.read().strip()
        else:
            current_symbols = ""
        
        # Get symbol from user
        symbol = get_user_input("Enter symbol to add (e.g., AAPL): ").upper().strip()
        if not symbol:
            display_error("No symbol entered.")
            input("\nPress Enter to continue...")
            return
            
        # Validate symbol (basic validation)
        if ',' in symbol:
            display_error("Symbol cannot contain commas.")
            input("\nPress Enter to continue...")
            return
            
        # Check if symbol already exists
        if current_symbols:
            existing_symbols = [s.strip() for s in current_symbols.split(',')]
            if symbol in existing_symbols:
                display_error(f"Symbol {symbol} already exists in configuration.")
                input("\nPress Enter to continue...")
                return
        
        # Add symbol to configuration
        if current_symbols:
            new_symbols = current_symbols + "," + symbol
        else:
            new_symbols = symbol
            
        # Write back to file
        with open(symbols_file, 'w') as f:
            f.write(new_symbols)
            
        display_success(f"Symbol {symbol} added successfully!")
        input("\nPress Enter to continue...")
        
    except Exception as e:
        display_error(f"Failed to add symbol: {e}")
        input("\nPress Enter to continue...")

def handle_purge_repository():
    """Handle purging all data from the repository"""
    try:
        # Confirm action
        display_error("WARNING: This will permanently delete ALL historical data files!")
        confirm = get_user_input("Type 'confirm' to proceed with purge: ").strip().lower()
        
        if confirm != 'confirm':
            display_info("Purge operation cancelled.")
            input("\nPress Enter to continue...")
            return
            
        # Get all files in repository
        files_to_delete = []
        for filename in os.listdir(cfg.DATA_REPOSITORY):
            f = os.path.join(cfg.DATA_REPOSITORY, filename)
            if os.path.isfile(f) and filename.endswith('.csv'):
                files_to_delete.append(f)
        
        if not files_to_delete:
            display_info("No data files found in repository.")
            input("\nPress Enter to continue...")
            return
            
        # Delete all CSV files
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                display_error(f"Failed to delete {file_path}: {e}")
                
        display_success(f"Successfully purged {deleted_count} data files from repository!")
        input("\nPress Enter to continue...")
        
    except Exception as e:
        display_error(f"Failed to purge repository: {e}")
        input("\nPress Enter to continue...")

def handle_remove_symbol():
    """Handle removing a symbol from the configuration"""
    try:
        # Read current symbols
        symbols_file = cfg.SYMBOLS_FILEPATH
        if not os.path.exists(symbols_file):
            display_error("No symbols configuration file found.")
            input("\nPress Enter to continue...")
            return
            
        with open(symbols_file, 'r') as f:
            current_symbols = f.read().strip()
            
        if not current_symbols:
            display_info("No symbols configured.")
            input("\nPress Enter to continue...")
            return
            
        # Show current symbols
        symbols_list = [s.strip() for s in current_symbols.split(',')]
        display_info("Current configured symbols:")
        for i, sym in enumerate(symbols_list, 1):
            print(f"  {i}. {sym}")
            
        # Get symbol to remove
        symbol_choice = get_user_input("Enter symbol number to remove (or symbol name): ")
        
        symbol_to_remove = None
        
        # Try to interpret as number first
        if symbol_choice.isdigit():
            index = int(symbol_choice) - 1
            if 0 <= index < len(symbols_list):
                symbol_to_remove = symbols_list[index]
            else:
                display_error("Invalid symbol number.")
                input("\nPress Enter to continue...")
                return
        else:
            # Try to match by symbol name
            symbol_to_remove = symbol_choice.upper().strip()
            if symbol_to_remove not in symbols_list:
                display_error(f"Symbol {symbol_to_remove} not found in configuration.")
                input("\nPress Enter to continue...")
                return
        
        # Remove symbol from list
        remaining_symbols = [s for s in symbols_list if s != symbol_to_remove]
        
        # Write back to file
        if remaining_symbols:
            new_symbols = ','.join(remaining_symbols)
        else:
            new_symbols = ""
            
        with open(symbols_file, 'w') as f:
            f.write(new_symbols)
            
        display_success(f"Symbol {symbol_to_remove} removed successfully!")
        input("\nPress Enter to continue...")
        
    except Exception as e:
        display_error(f"Failed to remove symbol: {e}")
        input("\nPress Enter to continue...")

def handle_configuration():
    """
    Handle configuration operations
    """
    # Configuration file path
    config_path = os.path.join(os.path.dirname(__file__), "config", "qstudio-configuration.json")
    
    while True:
        # Load current configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Display current configuration
        clear_screen()
        display_header()
        print("\nCONFIGURATION")
        print("=" * 50)
        print(f"1. LLM API URL: {config['LLM_API_URL']}")
        print(f"2. LLM API KEY: {'*' * len(config['LLM_API_KEY']) if config['LLM_API_KEY'] else 'Not set'}")
        print(f"3. LLM MODEL: {config['LLM_MODEL']}")
        print("=" * 50)
        
        # Get user choice
        print("\nSelect option to edit (1-3), or 0 to go back:")
        try:
            choice = int(input("Choice: "))
            
            if choice == 0:
                break
            elif choice == 1:
                new_value = input(f"Enter new LLM API URL (current: {config['LLM_API_URL']}): ")
                if new_value:
                    config['LLM_API_URL'] = new_value
            elif choice == 2:
                new_value = input(f"Enter new LLM API KEY (current: {'*' * len(config['LLM_API_KEY']) if config['LLM_API_KEY'] else 'Not set'}): ")
                if new_value:
                    config['LLM_API_KEY'] = new_value
            elif choice == 3:
                new_value = input(f"Enter new LLM MODEL (current: {config['LLM_MODEL']}): ")
                if new_value:
                    config['LLM_MODEL'] = new_value
            else:
                display_error("Invalid choice. Please select 0-3.")
                input("\nPress Enter to continue...")
                continue
                
            # Save configuration
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            display_success("Configuration updated successfully!")
            input("\nPress Enter to continue...")
            
        except ValueError:
            display_error("Please enter a valid number.")
            input("\nPress Enter to continue...")
        except Exception as e:
            display_error(f"Error updating configuration: {e}")
            input("\nPress Enter to continue...")


def handle_utilities():
    """
    Handle utilities operations
    """
    options = [
        "Generate Random Equities",
        "Clean Random Equity Folder",
        "Documentation",
        "Clear Cache"
    ]
    
    while True:
        display_submenu("UTILITIES", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            # Generate Random Equities
            handle_random_equities_generation()
        elif choice == 2:
            # Clean Random Equity Folder
            handle_random_equities_cleanup()
        elif choice == 3:
            # Documentation
            display_info("Opening online documentation...")
            open_onlinedoc()
            display_success("Documentation opened in browser!")
            input("\nPress Enter to continue...")
        elif choice == 4:
            # Clear Cache
            display_info("Clearing all cache files...")
            clear_cache()
            input("\nPress Enter to continue...")
        elif choice == 0:
            break

def run_menu_interface():
    """Run the main menu interface"""
    while True:
        display_main_menu()
        choice = get_user_choice(10)  # Updated to include new Screener option
        
        if choice == 1:
            handle_data_management()
        elif choice == 2:
            handle_financial_analysis()
        elif choice == 3:
            handle_visualization()
        elif choice == 4:
            handle_strategy_analysis()
        elif choice == 5:
            handle_utilities()
        elif choice == 6:
            display_info("Opening online documentation...")
            open_onlinedoc()
            display_success("Documentation opened in browser!")
            input("\nPress Enter to continue...")
        elif choice == 9:
            handle_configuration()
        elif choice == 0:
            if HAS_COLORAMA:
                print(Fore.GREEN + Style.BRIGHT + "\nThank you for using QStudio!" + Style.RESET_ALL)
            else:
                print("\nThank you for using QStudio!")
            break

# Original functions that were moved to menu_interface.py
def datahub_update_all():
    """
    DATAHUB_UPDATE_ALL: update all the specified symbols in configuration config file
    """
    s = Datahub(loadfromconfig=True)
    s.update_data()

def datahub_update(_symbols):
    """
    DATAHUB_UPDATE: update specified symbols, can be passed as a string separated by comma
    """
    s = Datahub(loadfromconfig=False)
    s.set_symbols(_symbols)
    s.update_data()

def datahub_show():
    """
    DATAHUB_SHOW: show content by listing the REPO folder with date range for each file
    """
    print("DATAHUB Repository")
    print("{:<15} {:<12} {:<12}".format("TICKER", "START", "END"))
    print("-" * 40)
    
    # Get all CSV files and sort them for consistent output
    csv_files = [f for f in os.listdir(cfg.DATA_REPOSITORY) if f.endswith('.csv')]
    csv_files.sort()
    
    for file in csv_files:
        filepath = os.path.join(cfg.DATA_REPOSITORY, file)
        try:
            # Read just the Date column to minimize memory usage
            if os.path.getsize(filepath) > 0:  # Check if file is not empty
                # Read the first row to get the start date
                first_row = pandas.read_csv(filepath, usecols=['Date'], nrows=1)
                
                # Read the last row to get the end date
                # Using chunksize to efficiently read only the last row
                chunk_size = 10000
                last_chunk = None
                for chunk in pandas.read_csv(filepath, usecols=['Date'], chunksize=chunk_size):
                    last_chunk = chunk
                
                if len(first_row) == 0:
                    start_date = "No data"
                    end_date = "No data"
                else:
                    start_date = first_row['Date'].iloc[0]
                    if last_chunk is not None and len(last_chunk) > 0:
                        end_date = last_chunk['Date'].iloc[-1]  # Last row of the last chunk
                    else:
                        end_date = start_date  # Only one row in file
                        
                ticker = file.replace('.csv', '')
                print("{:<15} {:<12} {:<12}".format(ticker, start_date, end_date))
            else:
                ticker = file.replace('.csv', '')
                print("{:<15} {:<12} {:<12}".format(ticker, "Empty", "Empty"))
                
        except Exception as e:
            ticker = file.replace('.csv', '')
            print("{:<15} {:<12} {:<12}".format(ticker, "Error", "Error"))

def config_symbols():
    """
    CONFIG_SYMBOLS: show configured synmbols in config symbol file
    """
    print("CONFIGURED Symbols in " + cfg.DATA_REPOSITORY)
    for x in Datahub(loadfromconfig=True).get_symbols():
        print(" - " + str(x))

def config_show():
    """
    CONFIG_SHOW
    """
    print("Configuration Settings")
    print("VERBOSE              : " + str(cfg.VERBOSE))
    print("DATAHUB REPOSITORY   : " + str(cfg.DATA_REPOSITORY))
    print("SYMBOLS FILE CONFIG  : " + str(cfg.SYMBOLS_FILEPATH))
    print("OUTPUT REPOSITORY    : " + str(cfg.OUTPUT_REPOSITORY))

def correlation_matrix_show(show=True, periods=21):
    """
    CORRELATION_MATRIX_SHOW: show correlation matrix for the configured symbols
    """
    s = Datahub(loadfromconfig=True)
    cm = CorrelationMatrix(s, show)
    cm.generate(periods)

def correlation_matrix_symbols(_symbols, show=True, periods=21):
    """
    CORRELATION_MATRIX_SYMBOLS: show correlation matrix for the given symbols
    """
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    cm = CorrelationMatrix(s, show)
    cm.generate(periods)

def yields(_symbols, show=True, periods=252, overlay=False):
    """
    YIELDS
    """
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=overlay)
    ys.generate(periods)

def yields_weekly(_symbols, show=True, periods=252, overlay=False):
    """
    YIELDS WEEKLY
    """
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=overlay)
    ys.generate_week(periods)

def yields_monthly(_symbols, show=True, periods=9999, overlay=False):
    """
    YIELDS MONTHLY
    """
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=overlay)
    ys.generate_month(periods)

def volatility(_symbols, periods=999999999):
    """
    VOLATILITY
    """
    s = Datahub(loadfromconfig=True)
    if _symbols is not None:
        s.set_symbols(_symbols)
    ys = Yields(s, False, overlay=False)
    ys.get_volatility(periods)

def autocorrelation(_symbols, show=True):
    """
    :param _symbols:
    :param show:
    :return:
    """
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show, overlay=False)
    ys.autocorrelation()

def chart(_symbols, show=True, _periods=9999, candles=False):
    """
    :param _symbols:
    :param show:
    :param _periods:
    :param candles:
    :return:
    """
    s = Datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    c = Charts(s, show, overlay=False)
    if candles:
        c.generate(_periods)
    else:
        c.generate_line(_periods)

def random_equity(folder=cfg.EQUITY_OUTPUT, nr=1):
    today = datetime.date.today()
    # generate random equities
    for i in range(nr):
        rand_name = names.get_first_name(gender='female')
        print("Generating random equity: "+str(rand_name))
        random_eq.generate_random_equity(datetime.date(year=2010, month=3, day=1),
                                          datetime.date(year=today.year, month=today.month, day=today.day),
                                          filepath=str(os.path.join(folder, ''))+str(rand_name)+"_eq.csv")
    return

def random_equity_delete(folder=cfg.EQUITY_OUTPUT):
    print("Cleaning folder "+str(folder))
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            os.remove(f)
            print(" . deleting file "+str(f))
    return

def check_strategy_help():
    print("Redirect to "+cfg.CHECK_STRATEGY_HELP_URL)
    webbrowser.open(cfg.CHECK_STRATEGY_HELP_URL)
    return

def check_strategy(folder=cfg.EQUITY_OUTPUT, report=False):
    print("Check Strategy in folder "+str(folder))
    cs.strategy_evaluator(folder, report)
    return

def check_single_strategy(equity_filepath=cfg.EQUITY_OUTPUT, report=False):
    print("Check single Strategy with equity file: "+str(equity_filepath))
    cs.check_single_strategy(equity_filepath, equity_filepath, report)
    return

def open_onlinedoc():
    print("Redirect to "+cfg.ONLINE_DOCS_URL)
    webbrowser.open(cfg.ONLINE_DOCS_URL)
    return

def detect_market_behavior(_symbols):
    s = Datahub(loadfromconfig=True)
    if _symbols != None:
        s.set_symbols(_symbols)
    he = Hurst_Exponent(s)
    # he.set_margin_percentage(0.1)
    he.calc()
    return

def hack_opt(_symbols, _qty, _mean_reverting=True, _trend_filter=False, _entry_pattern=0):
    """
    :param _symbols:
    :param _qty:
    :param _mean_reverting:
    :param _trend_filter:
    :param _entry_pattern:
    :return:
    """
    print(" HACKING THE MARKET FOR FUN AND PROFIT")
    s = Datahub(loadfromconfig=True)
    if _symbols != None:
        s.set_symbols(_symbols)

    for s in s.get_symbols():
        x = Hack_Strategy("Hacking the Market for Fun and Profit", s)
        x.set_quantity(_qty)
        x.backtest_period("2000-01-20 00:00:00")
        x.set_verbose(False)
        x.set_trend_follower(not _mean_reverting)
        x.set_trend_filter(_trend_filter)
        x.set_entry_pattern(_entry_pattern)
        x.run()
        x.report_statistics()
        x.plot_equity()
        x.plot_yields_by_years()
        x.show_historical_positions(20)

    return

def hack(_symbols, _qty=100, _mean_reverting=None):
    print(" HACKING THE MARKET FOR FUN AND PROFIT")
    s = Datahub(loadfromconfig=True)
    if _symbols != None:
        s.set_symbols(_symbols)

    _data = []
    for s in s.get_symbols():
        # for each symbol in symbols...
        for trend_filter in (True, False):
            for entry_pattern in range(0, 10):
                if _mean_reverting == None:
                    for mean_reverting in (True, False):
                        if mean_reverting:
                            mtype = "Mean-Reverting"
                        else:
                            mtype = "Trend-Following"
                        x = Hack_Strategy("Hacking the Market for Fun and Profit", s)
                        x.set_quantity(_qty)
                        x.backtest_period("2000-01-20 00:00:00")
                        x.set_verbose(False)
                        x.set_trend_follower(not mean_reverting)
                        x.set_trend_filter(trend_filter)
                        x.set_entry_pattern(entry_pattern)
                        x.run()
                        _data.append([x.symbol, mtype, entry_pattern, trend_filter, x.qstat.pnl, x.qstat.average_trade, x.qstat.tot_trades, x.qstat.maxdd])
                else:
                    if _mean_reverting:
                        mtype = "Mean-Reverting"
                    else:
                        mtype = "Trend-Following"
                    x = Hack_Strategy("Hacking the Market for Fun and Profit", s)
                    x.set_quantity(_qty)
                    x.backtest_period("2000-01-20 00:00:00")
                    x.set_verbose(False)
                    x.set_trend_follower(not _mean_reverting)
                    x.set_trend_filter(trend_filter)
                    x.set_entry_pattern(entry_pattern)
                    x.run()
                    _data.append([x.symbol, mtype, entry_pattern, trend_filter, x.qstat.pnl, x.qstat.average_trade, x.qstat.tot_trades, x.qstat.maxdd])

    opt = pandas.DataFrame(_data, columns=['Symbol', 'Strategy Type', 'Entry Pattern', 'Trend Filter', 'pnl', 'avgtrade', '#Trades', 'maxdd'])
    opt = opt.sort_values(['avgtrade', 'pnl', '#Trades'], ascending=False)
    print("--"*40)
    print(" R E S U L T S")
    print(opt.head(30))
    return

def header():
    """
    HEADER
    """
    print("-" * 120)
    print(" Q S t u d i o   " + str(cfg.VERSION))
    print(" " + str(cfg.AUTHOR))
    print(" www.surprisalx.com")
    print("-" * 120)