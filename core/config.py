#=======================================================================================================================
# QStudio - config.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import matplotlib.pyplot as plt
from datetime import datetime


# If true this will prints all the outputs.
VERBOSE=True

# File that contains the symbol list separated by comma
SYMBOLS_FILEPATH="./config/symbols"

# Historical data repository path (with trailing /)
DATA_REPOSITORY="./data/"

# Output repository path (with trailing /)
OUTPUT_REPOSITORY="./output/"
OUTPUT_FILENAME=datetime.now().strftime("%Y%m%dT%H%M%S")
# MATHPLOT Style
plt.style.use('fast')