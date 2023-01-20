# =======================================================================================================================
# QStudio - qstudio.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import datetime
import sys
import core.config as cfg
from core.Datahub import datahub
import os
from correlation_matrix.CorrelationMatrix import CorrelationMatrix
from yields.Yields import Yields

# QStudio version
VERSION = "v0.1.0"


def datahub_update_all():
    """
    DATAHUB_UPDATE_ALL: update all the specified symbols in configuration config file
    """
    header()
    s = datahub(loadfromconfig=True)
    s.update_data()


def datahub_update(_symbols):
    """
    DATAHUB_UPDATE: update specified symbols, can be passed as a string separated by comma
    """
    header()
    s = datahub(loadfromconfig=False)
    s.set_symbols(_symbols)
    s.update_data()


def datahub_show():
    """
    DATAHUB_SHOW: show content by listing the REPO folder
    """
    header()
    print("DATAHUB Repository")
    for file in os.listdir(cfg.DATA_REPOSITORY):
        print(" - " + str(file))


def config_symbols():
    """
    CONFIG_SYMBOLS: show configured synmbols in config symbol file
    """
    header()
    print("CONFIGURED Symbols in " + cfg.DATA_REPOSITORY)
    for x in datahub(loadfromconfig=True).get_symbols():
        print(" - " + str(x))



def config_show():
    """
    CONFIG_SHOW
    """
    header()
    print("Configuration Settings")
    print("VERBOSE              : " + str(cfg.VERBOSE))
    print("DATAHUB REPOSITORY   : " + str(cfg.DATA_REPOSITORY))
    print("SYMBOLS FILE CONFIG  : " + str(cfg.SYMBOLS_FILEPATH))
    print("OUTPUT REPOSITORY    : " + str(cfg.OUTPUT_REPOSITORY))




def correlation_matrix_show(show=True,periods=21):
    """
    CORRELATION_MATRIX_SHOW: show correlation matrix for the configured symbols
    """
    header()
    s = datahub(loadfromconfig=True)
    cm = CorrelationMatrix(s, show)
    cm.generate(periods)



def correlation_matrix_symbols(_symbols, show=True,periods=21):
    """
    CORRELATION_MATRIX_SYMBOLS: show correlation matrix for the given symbols
    """
    header()
    s = datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    cm = CorrelationMatrix(s, show)
    cm.generate(periods)

def yields(_symbols, show=True, periods=252, overlay=False):
    """
    YIELDS
    """
    header()
    s = datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show,overlay=overlay)
    ys.generate(periods)

def yields_weekly(_symbols, show=True, periods=252, overlay=False):
    """
    YIELDS WEEKLY
    """
    header()
    s = datahub(loadfromconfig=True)
    s.set_symbols(_symbols)
    ys = Yields(s, show,overlay=overlay)
    ys.generate_week(periods)


def main():
    """
    MAIN
    """
    args = sys.argv[1:]

    """
    DATA HUB
    """
    if len(args) == 2 and args[0] == '--datahub':
        if args[1] == '--show':
            datahub_show()
            return
    if len(args) == 2 and args[0] == '--datahub':
        if args[1] == '--update-all':
            datahub_update_all()
            return
    if len(args) == 3 and args[0] == '--datahub':
        if args[1] == '--update' and args[2] != '':
            datahub_update(args[2])
            return

    """
    CONFIGURATION
    """
    if len(args) == 2 and args[0] == '--config':
        if args[1] == '--show':
            config_show()
            return
    if len(args) == 2 and args[0] == '--config':
        if args[1] == '--symbols':
            config_symbols()
            return

    """
    CORRELATION MATRIX
    """
    if len(args) == 1 and args[0] == '--correlation_matrix':
        correlation_matrix_show(True)
        return
    if len(args) == 2  and args[0] == '--correlation_matrix':
        if args[1] == '--save':
            correlation_matrix_show(False)
            return
    if len(args) == 3 and args[0] == '--correlation_matrix':
        if args[1] == '--periods' and args[2] != '':
            correlation_matrix_show(True,int(args[2]))
            return
    if len(args) == 4 and args[0] == '--correlation_matrix':
        if args[1] == '--periods' and args[2] != '' and args[3] == '--save':
            correlation_matrix_show(False,int(args[2]))
            return
    if len(args) == 3 and args[0] == '--correlation_matrix':
        if args[1] == '--symbols' and args[2] != '':
            correlation_matrix_symbols(args[2], True)
            return
    if len(args) == 4 and args[0] == '--correlation_matrix' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            correlation_matrix_symbols(args[2], False)
            return
    if len(args) == 5 and args[0] == '--correlation_matrix' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            correlation_matrix_symbols(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--correlation_matrix' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            correlation_matrix_symbols(args[2], False, int(args[4]))
            return

    """
    YIELDS
    """
    if len(args) == 3 and args[0] == '--yields':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], True)
            return
    if len(args) == 4 and args[0] == '--yields' and args[3] == '--overlay':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], True, overlay=True)
            return
    if len(args) == 4 and args[0] == '--yields' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], False)
            return
    if len(args) == 5 and args[0] == '--yields' and args[3] == '--save' and args[4] == '--overlay':
        if args[1] == '--symbols' and args[2] != '':
            yields(args[2], False, overlay=True)
            return
    if len(args) == 5 and args[0] == '--yields' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--yields' and args[3] == '--periods' and args[5] == '--overlay':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], True, int(args[4]), overlay=True)
            return
    if len(args) == 6 and args[0] == '--yields' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], False, int(args[4]))
            return
    if len(args) == 7 and args[0] == '--yields' and args[3] == '--periods' and args[5] == '--save' and args[6] == '--overlay':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields(args[2], False, int(args[4]),overlay=True)
            return
    """
    YIELDS_WEEKLY
    """
    if len(args) == 3 and args[0] == '--yields_weekly':
        if args[1] == '--symbols' and args[2] != '':
            yields_weekly(args[2], True)
            return
    if len(args) == 4 and args[0] == '--yields_weekly' and args[3] == '--save':
        if args[1] == '--symbols' and args[2] != '':
            yields_weekly(args[2], False)
            return
    if len(args) == 5 and args[0] == '--yields_weekly' and args[3] == '--periods':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields_weekly(args[2], True, int(args[4]))
            return
    if len(args) == 6 and args[0] == '--yields_weekly' and args[3] == '--periods' and args[5] == '--save':
        if args[1] == '--symbols' and args[2] != '' and args[4] != '':
            yields_weekly(args[2], False, int(args[4]))
            return
    usage()




def usage():
    """
    USAGE
    """
    header()
    print("USAGE:")
    # CONFIG
    print(" CONFIGURATION")
    print(" --config --show               : show actual configurationn " + cfg.SYMBOLS_FILEPATH)
    print(" --config --symbols            : show configured symbols in " + cfg.SYMBOLS_FILEPATH)
    print(" CORRELATION MATRIX ")

    # CORRELATION MATRIX
    print(" --correlation_matrix                                    : show correlation matrix for configured symbols")
    print(" --correlation_matrix --save                             : save correlation matrix chart for configured symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --correlation_matrix --periods [periods]                : show correlation matrix for configured symbols and given periods")
    print(" --correlation_matrix --periods [periods] --save         : save correlation matrix for configured symbols and given periods in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --correlation_matrix --symbols [symbols]                : show correlation matrix for given symbols")
    print(" --correlation_matrix --symbols [symbols] --save         : save correlation matrix chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --correlation_matrix --symbols [symbols] --periods [periods]        : show correlation matrix chart for given symbols for the given periods")
    print(" --correlation_matrix --symbols [symbols] --periods [periods] --save : save correlation matrix chart for given symbols for the given periods")

    # YIELDS
    print(" YIELDS")
    print(" --yields --symbols [symbols]                                        : show yields for the given symbols")
    print(" --yields --symbols [symbols] --overlay                              : show yields for the given symbols")
    print(" --yields --symbols [symbols] --save                                 : save yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields --symbols [symbols] --save --overlay                       : save yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields --symbols [symbols] --periods [periods]                    : show yields chart for given symbols for the given periods")
    print(" --yields --symbols [symbols] --periods [periods] --overlay          : show yields chart for given symbols for the given periods")
    print(" --yields --symbols [symbols] --periods [periods] --save --overlay   : save yields chart for given symbols for the given periods")

    # YIELDS WEEKLY
    print(" YIELDS WEEKLY")
    print(" --yields_weekly --symbols [symbols]                             : show weekly yields for the given symbols")
    print(" --yields_weekly --symbols [symbols] --save                      : save weekly yields chart for given symbols in repository "+cfg.OUTPUT_REPOSITORY)
    print(" --yields_weekly --symbols [symbols] --periods [periods]         : show weekly yields chart for given symbols for the given periods")
    print(" --yields_weekly --symbols [symbols] --periods [periods] --save  : save weekly yields chart for given symbols for the given periods")


    # DATA HUB
    print(" DATAHUB ")
    print(" --datahub --show              : show DATAHUB repository in " + cfg.DATA_REPOSITORY)
    print(" --datahub --update-all        : update the whole datahub from yfinance")
    print(" --datahub --update [symbols]  : update the given symbols separated by comma")
    print("   example: --datahub update AAPL,G,MS,XOM")
    print(" USAGE")
    # USAGE
    print(" --help                      : usage instructions")

def header():
    """
    HEADER
    """
    print("-" * 120)
    print(" Q S t u d i o  " + str(VERSION))
    print(" " + datetime.date.today().strftime("%Y") + " (c) Alberto Sfolcini <a.sfolcini@gmail.com>")
    print(" www.surprisalx.com")
    print("-" * 120)


# -----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
