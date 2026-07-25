from PySide6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QFont, QIcon
from PySide6.QtCore import Qt


def create_app_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setPen(QPen(QColor("#333333"), 2))
    painter.setBrush(QColor("#666666"))
    painter.drawEllipse(8, 16, 22, 22)

    painter.drawRect(28, 24, 28, 6)

    painter.drawRect(34, 30, 6, 8)
    painter.drawRect(46, 30, 6, 4)

    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor("#999999"))
    painter.drawEllipse(14, 22, 10, 10)

    painter.end()
    return QIcon(pixmap)
