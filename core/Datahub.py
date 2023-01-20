#=======================================================================================================================
# QStudio - config.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import core.config as cfg
import core.utils as utils
import yfinance as yf
import os
import pandas


class datahub:
    """
    SYMBOLS CLASS ( download from yfinance, load the dataset, update data etc... )
    """

    symbols_filepath = ""
    symbols = []


    def __init__(self, loadfromconfig=True):
        """
        INIT
        """
        if loadfromconfig:
            self.symbols = utils.load_from_file(cfg.SYMBOLS_FILEPATH).split(",")


    def get_symbols(self):
        """
        GET SYMBOLS list
        """
        return self.symbols

    def add_symbol(self, symbol):
        """
        ADD SYMBOL, add a single symbol to the symbols list
        """
        self.symbols.append(symbol)

    def set_symbols(self, symbols):
        """
        SET SYMBOLS from a string with comma as a separator, example 'G.MI,ENI.MI,AAPL,GS'
        """
        self.symbols.clear()
        for x in symbols.split(","):
            self.add_symbol(x)


    def load_data(self, symbol,lastperiods=None):
        """
        LOAD DATA from repository, if doesnt exist, download from the internet, returns panda dataframe,
        by default lastperiods is null
        """
        fp = str(cfg.DATA_REPOSITORY)+str(symbol)+str('.csv')
        if os.path.exists(fp):
            if cfg.VERBOSE: print("Load data from "+fp)
            if lastperiods:
                dataset = pandas.read_csv(fp, parse_dates=['Date']).tail(lastperiods)
            else:
                dataset = pandas.read_csv(fp, parse_dates=['Date'])
            return dataset
        else:
            if cfg.VERBOSE: print(fp+" does not exist, checking from yfinance...", end="")
            if self.download_data(symbol):
                if lastperiods:
                    dataset = pandas.read_csv(fp, parse_dates=['Date']).tail(lastperiods)
                else:
                    dataset = pandas.read_csv(fp, parse_dates=['Date'])
                if cfg.VERBOSE: print(" done.")
                return dataset
            else:
                if cfg.VERBOSE: print("Download from yfinance failed")
                return pandas.DataFrame()


    def download_data(self, symbol):
        """
        DOWNLOAD FROM YAHOO FINANCE and save in CSV
        """
        try:
            fp = str(cfg.DATA_REPOSITORY)+str(symbol)+str('.csv')
            # get historical market data
            hq = yf.Ticker(symbol)
            ds = hq.history(period="max")
            ds.reset_index(inplace=True)
            ds['Date'] = ds['Date'].dt.strftime('%Y-%m-%d')
            ds.to_csv(fp, index=False)
            return True
        except:
            return False


    def update_data(self):
        """
        UPDATE DATA FROM YAHOO FINANCE for the whole symbol list
        """
        for symbol in self.get_symbols():
            if cfg.VERBOSE: print("Updating "+str(symbol)+"...", end='')
            if self.download_data(symbol):
                print("done.")
            else:
                print("FAILED!")

