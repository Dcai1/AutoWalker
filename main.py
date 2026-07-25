import sys
from PySide6.QtWidgets import QApplication
from holder import KeyHolder
from gui import AutoHolderWindow


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    holder = KeyHolder()
    window = AutoHolderWindow(holder)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
