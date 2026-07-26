import sys
from PySide6.QtWidgets import QApplication
from holder import KeyHolder
from gui import AutoHolderWindow
from icon import create_app_icon


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setWindowIcon(create_app_icon())

    holder = KeyHolder()
    window = AutoHolderWindow(holder)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
