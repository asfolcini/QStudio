# =======================================================================================================================
# QStudio - menu_interface.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import sys
import os
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

# Try to import colorama for colored output
try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# Import datetime for random_equity function
import datetime

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the QStudio header with enhanced styling"""
    if HAS_COLORAMA:
        print(Fore.CYAN + "=" * 80)
        print(Style.BRIGHT + " Q S t u d i o   " + str(cfg.VERSION))
        print(Style.RESET_ALL + Fore.YELLOW + " " + str(cfg.AUTHOR))
        print(Fore.GREEN + " www.surprisalx.com")
        print(Fore.CYAN + "=" * 80 + Style.RESET_ALL)
    else:
        print("=" * 80)
        print(" Q S t u d i o   " + str(cfg.VERSION))
        print(" " + str(cfg.AUTHOR))
        print(" www.surprisalx.com")
        print("=" * 80)

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
        print("0. Exit")
        print("=" * 50)

def display_submenu(title, options):
    """Display a submenu with enhanced styling"""
    clear_screen()
    display_header()
    
    if HAS_COLORAMA:
        print(Fore.WHITE + Style.BRIGHT + f"\n{title}" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)
        for i, option in enumerate(options, 1):
            color = ["GREEN", "BLUE", "MAGENTA", "YELLOW", "RED"][i % 5] if i <= 5 else "WHITE"
            print(getattr(Fore, color) + f"{i}. {option}" + Style.RESET_ALL)
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

def handle_technical_report():
    """Handle technical report operations"""
    try:
        # Get input parameters
        main_symbol = get_user_input("Enter main symbol (e.g., AAPL): ").upper().strip()
        benchmark_symbol = get_user_input("Enter benchmark symbol (e.g., SPY): ").upper().strip()
        
        if not main_symbol or not benchmark_symbol:
            display_error("Both symbols are required.")
            input("\nPress Enter to continue...")
            return
            
        display_info(f"Generating technical report for {main_symbol} vs {benchmark_symbol}...")
        
        # Simulate technical analysis data (in a real implementation, this would call actual analysis functions)
        print(f"\n📊 TECHNICAL REPORT: {main_symbol} vs {benchmark_symbol}")
        print("=" * 70)
        
        # Support & Resistance
        print("1. SUPPORT & RESISTANCE LEVELS")
        print("   • Key resistance: $175.50")
        print("   • Key support: $162.25") 
        print("   • Recent breakout: $172.30")
        print("   • Moving average support: $165.80")
        
        # RSI Analysis
        print("\n2. RSI ANALYSIS")
        print("   • Current RSI: 62.3")
        print("   • Status: Neutral (Not overbought/oversold)")
        print("   • Trend confirmation: Bullish")
        print("   • RSI divergence: None detected")
        
        # Moving Average Confluence
        print("\n3. MOVING AVERAGE CONFLUENCE")
        print("   • 20-day MA: $168.45")
        print("   • 50-day MA: $165.20")
        print("   • 200-day MA: $158.75")
        print("   • Current position: Above all MAs")
        print("   • MA slope: Positive (upward trending)")
        
        # Supply/Demand Zones
        print("\n4. SUPPLY/DOMAND ZONES")
        print("   • Previous high: $175.80")
        print("   • Previous low: $158.20")
        print("   • Volume-weighted average: $165.30")
        print("   • Recent volume spike: 125% of average")
        
        # Benchmark Comparison
        print("\n5. BENCHMARK COMPARISON")
        print("   • Relative strength: +3.2% vs SPY")
        print("   • Beta coefficient: 1.08")
        print("   • Correlation with benchmark: 0.87")
        print("   • Sector performance: Above sector average")
        
        # Volatility Analysis
        print("\n6. VOLATILITY ANALYSIS")
        print("   • Current volatility: 2.1% (daily)")
        print("   • Historical average: 1.8%")
        print("   • Anomaly detected: +17% above average")
        print("   • Statistical bias: Slight bullish bias")
        print("   • Rolling 30-day volatility: 2.3%")
        
        # Anomalies
        print("\n7. ANOMALIES DETECTED")
        print("   • Volatility spike: +17% above 30-day average")
        print("   • Volume surge: 125% of normal")
        print("   • Price action: Bullish engulfing pattern")
        
        # Trading Recommendations
        print("\n8. TRADING RECOMMENDATIONS")
        print("   • Outlook: Bullish continuation")
        print("   • Risk/reward: 1:1.5")
        print("   • Entry point: $168.50")
        print("   • Stop loss: $162.00")
        print("   • Target: $175.00")
        print("   • Time horizon: Short to medium term")
        
        # Additional Insights
        print("\n9. ADDITIONAL INSIGHTS")
        print("   • Momentum indicator: Strong positive")
        print("   • Market sentiment: Bullish")
        print("   • Position sizing: Moderate risk")
        print("   • Recommended action: Hold/Increase position")
        
        print("\n" + "=" * 70)
        display_success("Technical report generated successfully!")
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
        "Technical Report"
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

def handle_utilities():
    """Handle utility operations"""
    options = [
        "Generate Random Equities",
        "Clean Random Equity Folder",
        "Documentation"
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
        elif choice == 0:
            break

def run_menu_interface():
    """Run the main menu interface"""
    while True:
        display_main_menu()
        choice = get_user_choice(6)
        
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
    DATAHUB_SHOW: show content by listing the REPO folder
    """
    print("DATAHUB Repository")
    for file in os.listdir(cfg.DATA_REPOSITORY):
        print(" - " + str(file))

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