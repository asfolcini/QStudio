from core.utils import *
import array
from core.Candle import Candle
def filter_pattern(events, pattern_nr):
    """
    List of Patterns to use as a filter or entry/exit conditions.
    :param pattern_nr:
    :return:
    """

    """
    PATTERN #0
    No pattern applied, returns true 
    """
    if pattern_nr == 0:
        return True

    """
    PATTERN #1
    Check if actual close is greater than previous 
    """
    if pattern_nr == 1:
        c = get_last_values(events, 2)
        if len(c)>1 and c[0].close>c[1].close:
            return True

    """
    PATTERN #2
    Check if actual close is greater than previous 2
    """
    if pattern_nr == 2:
        c = get_last_values(events, 3)
        if len(c)>2 and c[0].close>c[1].close and c[0].close>c[2].close:
            return True
    """
    PATTERN #3
    Check if actual close is greater than previous and the previous is greater than pre-previous
    """
    if pattern_nr == 3:
        c = get_last_values(events, 3)
        if len(c)>2 and c[0].close>c[1].close and c[1].close>c[2].close:
            return True

    """
    PATTERN #4
    Check if actual close is greater than previous 3
    """
    if pattern_nr == 4:
        c = get_last_values(events, 4)
        if len(c)>3 and c[0].close>c[1].close and c[0].close>c[2].close and c[0].close>c[3].close:
            return True

    """
    PATTERN #5
    If h/l excursion of today is lower than H-L of yesterday
    """
    if pattern_nr == 5:
        c = get_last_values(events, 2)
        if len(c)>1:
            r1 = c[0].high - c[0].low
            r2 = c[1].high - c[1].low
            if r1<r2:
                return True

    """
    PATTERN #6
    If the ration co/hl is less than 30% than it's good to go 
    """
    if pattern_nr == 6:
        c = get_last_values(events, 2)
        if len(c)>1:
            hl = c[0].high - c[0].low
            co = c[0].close - c[0].open
            if hl==0.0: hl=0.000000001

            if (co/hl)<0.3:
                return True

    """
    PATTERN #7
    If the ration co/hl is less than 20% than it's good to go 
    """
    if pattern_nr == 7:
        c = get_last_values(events, 2)
        if len(c)>1:
            hl = c[0].high - c[0].low
            co = c[0].close - c[0].open

            if hl==0.0: hl=0.000000001

            if (co/hl)<0.15:
                return True

    """
     PATTERN #8
     If the ration co1/co0 is less than 25% than it's good to go 
     """
    if pattern_nr == 8:
        c = get_last_values(events, 2)
        if len(c)>1:
            co0 = c[0].close - c[0].open
            co1 = c[1].close - c[1].open

            if co0==0.0: co0=0.000000001

            if (co1/co0)<0.4:
                return True



    # by default return False
    return False