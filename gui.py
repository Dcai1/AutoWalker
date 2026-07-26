from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt, QTimer
from pynput.keyboard import Key, KeyCode

from config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from icon import create_app_icon


def key_to_str(key):
    if isinstance(key, KeyCode):
        if key.char is not None:
            return key.char.upper()
        return str(key)
    elif isinstance(key, Key):
        name = str(key).replace('Key.', '').upper()
        return name
    return str(key).upper()


class AutoHolderWindow(QWidget):
    def __init__(self, holder):
        super().__init__()
        self._holder = holder
        self._capture_target = None

        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(create_app_icon())

        self._setup_ui()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._connect_signals()
        self._update_display()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(6)

        hold_label = QLabel("Key to Hold:")
        self.hold_display = QPushButton()
        self.hold_display.setFixedHeight(32)
        self.hold_display.setCursor(Qt.PointingHandCursor)
        self.hold_display.clicked.connect(self._start_hold_capture)

        hold_hint = QLabel("Click above and press any key to rebind")
        hold_hint.setStyleSheet("color: gray; font-size: 11px;")

        layout.addWidget(hold_label)
        layout.addWidget(self.hold_display)
        layout.addWidget(hold_hint)

        layout.addSpacing(6)

        toggle_label = QLabel("Toggle Keybind:")
        self.toggle_display = QPushButton()
        self.toggle_display.setFixedHeight(32)
        self.toggle_display.setCursor(Qt.PointingHandCursor)
        self.toggle_display.clicked.connect(self._start_toggle_capture)

        toggle_hint = QLabel("Click above and press any key to rebind")
        toggle_hint.setStyleSheet("color: gray; font-size: 11px;")

        layout.addWidget(toggle_label)
        layout.addWidget(self.toggle_display)
        layout.addWidget(toggle_hint)

        layout.addSpacing(10)

        self.start_stop_btn = QPushButton()
        self.start_stop_btn.setFixedHeight(36)
        
        # Set the background color of the button to grey
        self.start_stop_btn.setStyleSheet("background-color: #666666;")

        layout.addWidget(self.start_stop_btn)

        layout.addStretch()

        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignCenter)
        self.msg_label.setWordWrap(True)
        self.msg_label.setStyleSheet("color: #cc0000; font-size: 11px;")
        
        # Set the color of the message label to black
        self.msg_label.setStyleSheet("color: #cc0000; font-size: 11px;")

        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: gray; font-size: 11px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # Set the color of the status label to black
        self.status_label.setStyleSheet("color: gray; font-size: 11px;")

        admin_hint = QLabel(
            "If the keys aren't working in-game, try running this program as an Administrator."
        )
        admin_hint.setStyleSheet("color: gray; font-size: 11px;")
        admin_hint.setAlignment(Qt.AlignCenter)
        admin_hint.setWordWrap(True)

        layout.addWidget(self.msg_label)
        layout.addWidget(self.status_label)
        layout.addWidget(admin_hint)

        self.setLayout(layout)

    def _connect_signals(self):
        self._holder.running_changed.connect(self._on_running_changed)
        self._holder.key_captured.connect(self._on_key_captured)
        self.start_stop_btn.clicked.connect(self._toggle_start_stop)

    # Update the display to reflect the current state
    def _on_running_changed(self, running):
        self.start_stop_btn.setText("Running!" if running else "Stopped")
        color = "green" if running else "red"
        self.start_stop_btn.setStyleSheet(f"background-color: {color}; color: white;")

    def _toggle_start_stop(self):
        self._holder.toggle()

    def _start_hold_capture(self):
        self._capture_target = 'hold'
        self.hold_display.setText("Press a key...")
        self._holder.start_capture()

    def _start_toggle_capture(self):
        self._capture_target = 'toggle'
        self.toggle_display.setText("Press a key...")
        self._holder.start_capture()

    def _on_key_captured(self, key):
        if key is None:
            self._capture_target = None
            self._update_display()
            return

        if self._capture_target == 'hold':
            success = self._holder.set_hold_key(key)
            if success:
                self.hold_display.setText(key_to_str(self._holder.hold_key))
                self._show_message(f"Hold key changed to {key_to_str(key)}", "green")
            else:
                self.hold_display.setText(key_to_str(self._holder.hold_key))
                self._show_message("Cannot use the same key as toggle key!", "red")
        elif self._capture_target == 'toggle':
            success = self._holder.set_toggle_key(key)
            if success:
                self.toggle_display.setText(key_to_str(self._holder.toggle_key))
                self._show_message(f"Toggle key changed to {key_to_str(key)}", "green")
            else:
                self.toggle_display.setText(key_to_str(self._holder.toggle_key))
                self._show_message("Cannot use the same key as hold key!", "red")
        else:
            self._update_display()
        self._capture_target = None

    def _show_message(self, text, color="green"):
        self.msg_label.setStyleSheet(f"color: {color}; font-size: 11px;")
        self.msg_label.setText(text)
        QTimer.singleShot(3000, self._clear_message)

    def _clear_message(self):
        self.msg_label.clear()

    def _update_display(self):
        self.hold_display.setText(key_to_str(self._holder.hold_key))
        self.toggle_display.setText(key_to_str(self._holder.toggle_key))
        running = self._holder.is_running
        self.start_stop_btn.setText("Stop" if running else "Start")

    def closeEvent(self, event):
        self._holder.stop()
        event.accept()
