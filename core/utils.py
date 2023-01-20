#=======================================================================================================================
# QStudio - utils.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
#=======================================================================================================================


#-----------------------------------------------------------------------------------------------------------------------
# Load content from text file and return it
#-----------------------------------------------------------------------------------------------------------------------
def load_from_file(filepath):
    with open(filepath) as f:
        content = f.read()
    return content