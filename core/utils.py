#=======================================================================================================================
# QStudio - utils.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
from core import Candle
import time
import pandas as pd

#-----------------------------------------------------------------------------------------------------------------------
# Load content from text file and return it
#-----------------------------------------------------------------------------------------------------------------------
def load_from_file(filepath):
    with open(filepath) as f:
        content = f.read()
    return content


def get_formatted_time(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    return formatted_time

def get_last_values(events, last_value_nr=2):
    """
    Return array with the last N values, v[0] is the current event, v[1] is the 1period last event, etc...
    :param events:
    :param last_value_nr:
    :return:
    """
    v = []

    if last_value_nr<2:
        print("WARNING: last_values must be equal or greater than 2, using default value as 2")
        last_value_nr=2

    e : Candle
    i = 0
    for e in events.tolist()[-last_value_nr:]:
        v.insert(i, e)
        i = i + 1

    # reverse the array order to have the v[0] as the actual event
    return v[::-1]