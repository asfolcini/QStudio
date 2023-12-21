# =======================================================================================================================
# QStudio - Hurst_Exponent.py class
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
'''
 The goal of the Hurst Exponent is to provide us with a scalar value that will help us to identify
 (within the limits of statistical estimation) whether a series is mean reverting, random walking or trending.
 A time series can then be characterised in the following manner:

 H < 0.5  The time series is mean reverting
 H = 0.5  The time series is a Geometric Brownian Motion
 H > 0.5 The time series is trending

 In addition to characterisation of the time series the Hurst Exponent also describes the extent to which a series behaves in the manner categorised. For instance, a value of
 near 0 is a highly mean reverting series, while for
 near 1 the series is strongly trending.

'''

from core.Datahub import Datahub
from numpy import cumsum, log, polyfit, sqrt, std, subtract
import statsmodels.tsa.stattools as ts

class Hurst_Exponent:
    """
    HURST_EXPONENT CLASS.
    call the calc() method
    """
    s = Datahub()

    # setting the offset to 5% (default)
    margin_percentage = 0.05

    """
    INIT
    """

    def __init__(self, _s):
        self.s = _s

    def set_margin_percentage(self, percentage):
        """
        Setting margin_percentage in order to detect trend, mean-revert or random walk
        Ex. 0.05 means 5%
        :param percentage:
        :return:
        """
        self.margin_percentage = percentage

    def decodeH(self, H):
        offset = 0.5 * self.margin_percentage
        if (H>(0.5-offset) and H<(0.5+offset)):
            decoded_text = "RANDOM WALK"
        else:
            if H>(0.5+offset):
                decoded_text = "TRENDING"
            else:
                decoded_text = "MEAN-REVERTING"

        return decoded_text



    def calc(self):
        """
        COMPUTE HURST EXPONENT
        """
        for s in self.s.get_symbols():
            r = self.s.load_data(s)
            r['Symbol'] = s
            H = self.hurst(r['Close'].values)
            print(s, "is likely a", self.decodeH(H), " (Hurst=%s)" %H, "using margin of", self.margin_percentage*100, "%")



    def hurst(self, ts):
        """
        Returns the Hurst Exponent of the time series vector ts

        Parameters
        ----------
        ts : `numpy.array`
            Time series upon which the Hurst Exponent will be calculated

        Returns
        -------
        'float'
            The Hurst Exponent from the poly fit output
        """
        # Create the range of lag values
        lags = range(2, 100)

        # Calculate the array of the variances of the lagged differences
        tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

        # Use a linear fit to estimate the Hurst Exponent
        poly = polyfit(log(lags), log(tau), 1)

        # Return the Hurst exponent from the polyfit output
        return poly[0]*2.0

    def augmented_dickey_fuller(self):
        """
        Carry out the Augmented Dickey-Fuller test for Google data.

        Parameters
        ----------
        goog : `pd.DataFrame`
          A DataFrame containing Google (GOOG) OHLCV data from
              01/09/2004-31/08/2020. Index is a Datetime object.

        Returns
        -------
        None
        """
        for s in self.s.get_symbols():
            r = self.s.load_data(s)
            # Output the results of the Augmented Dickey-Fuller test for Google
            # with a lag order value of 1
            adf = ts.adfuller(r['Close'], 1)
            print(adf)