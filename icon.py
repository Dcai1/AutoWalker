import sys
from pathlib import Path

from PySide6.QtGui import QIcon


def _icon_path():
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_dir / "img" / "favicon.ico"


def create_app_icon():
    icon_path = _icon_path()
    return QIcon(str(icon_path))
