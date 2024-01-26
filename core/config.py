#=======================================================================================================================
# QStudio - config.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# QStudio version
VERSION = "v0.3.8"

# Author
AUTHOR="Alberto Sfolcini <a.sfolcini@gmail.com>"

# If true this will prints all the outputs.
VERBOSE=False


# Settign default pandas options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# CSV SEPARATOR
CSV_SEPARATOR = ","

# Online QStudio Docuemntation
ONLINE_DOCS_URL = "https://surprisalx.com/qstudio/"

# Check strategy url
CHECK_STRATEGY_HELP_URL = "https://surprisalx.com/qstudio/index.php?s=2.8%20Strategy%20Evaluator"
STRATEGY_EVALUATOR_LONG_TERM = 378   # 18 months
STRATEGY_EVALUATOR_SHORT_TERM = 63   # 3 months

# File that contains the symbol list separated by comma
SYMBOLS_FILEPATH = "./config/symbols"

# Historical data repository path (with trailing /)
DATA_REPOSITORY = "./data/"

# Output repository path (with trailing /)
OUTPUT_REPOSITORY="./output/"
OUTPUT_FILENAME=datetime.now().strftime("%Y%m%dT%H%M%S")
# MATHPLOT Style
plt.style.use('fast')

OPTIMIZATION_REPORT_TEMPLATE = "./config/optimization_report_template.html"
OPTIMIZATION_REPORT_PATH = OUTPUT_REPOSITORY+"optimization_reports"

# Telegram channel instant messanger
TELEGRAM_BOT_TOKEN = "6048507085:AAHPWlXXCmasC0r1oLo2OnsnAgyxNleeqpI"
TELEGRAM_CHANNEL_ID = "-1001910945256"