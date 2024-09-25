import os
import sys


def load_ipython_extension(ipython):
    sys.path.append(os.path.abspath('..'))


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass
