import sys
import os
from pathlib import Path

from PySide6.QtGui import QIcon


if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)



def create_app_icon():
    return QIcon(os.path.join(basedir, "favicon.ico"))