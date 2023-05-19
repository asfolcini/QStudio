#=======================================================================================================================
# QStudio - config.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import matplotlib.pyplot as plt
from datetime import datetime

# QStudio version
VERSION = "v0.3.0"

# Author
AUTHOR="Alberto Sfolcini <a.sfolcini@gmail.com>"

# If true this will prints all the outputs.
VERBOSE=False

# Check strategy url
CHECK_STRATEGY_HELP_URL="https://surprisalx.com/check_strategy.html"

# File that contains the symbol list separated by comma
SYMBOLS_FILEPATH="./config/symbols"

# Historical data repository path (with trailing /)
DATA_REPOSITORY="./data/"

# Output repository path (with trailing /)
OUTPUT_REPOSITORY="./output/"
OUTPUT_FILENAME=datetime.now().strftime("%Y%m%dT%H%M%S")
# MATHPLOT Style
plt.style.use('fast')

# Telegram channel instant messanger
TELEGRAM_BOT_TOKEN = "6048507085:AAHPWlXXCmasC0r1oLo2OnsnAgyxNleeqpI"
TELEGRAM_CHANNEL_ID = "-1001910945256"