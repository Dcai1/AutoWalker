from threading import Lock
from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Listener, Controller, Key, KeyCode

from config import HOLD_KEY, TOGGLE_KEY


class KeyHolder(QObject):
    running_changed = Signal(bool)
    key_captured = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._hold_key = HOLD_KEY
        self._toggle_key = TOGGLE_KEY
        self._controller = Controller()
        self._lock = Lock()
        self._capturing = False

        self._ignore_next_press = False
        self._listener = Listener(on_press=self._on_press)
        self._listener.start()

    def _on_press(self, key):
        captured_key = None
        should_toggle = False
        with self._lock:
            if self._ignore_next_press:
                self._ignore_next_press = False
                return

            if self._capturing:
                self._capturing = False
                # capture all key presses but ESC
                if key != Key.esc:
                    captured_key = key
            
            # toggle key press by toggle key or hold key if already running
            elif key == self._toggle_key or (self._running and key == self._hold_key):
                self._running = not self._running
                if self._running:
                    self._ignore_next_press = True
                    self._controller.press(self._hold_key)
                else:
                    self._controller.release(self._hold_key)
                should_toggle = True
        if captured_key is not None:
            self.key_captured.emit(captured_key)
        elif captured_key is None and should_toggle is False:
            pass
        if should_toggle:
            self.running_changed.emit(self._running)

    def start_capture(self):
        with self._lock:
            self._capturing = True

    def set_hold_key(self, key):
        with self._lock:
            if key == self._toggle_key:
                return False
            was_running = self._running
            if was_running:
                self._controller.release(self._hold_key)
            self._hold_key = key
            if was_running:
                self._controller.press(self._hold_key)
            return True

    def set_toggle_key(self, key):
        with self._lock:
            if key == self._hold_key:
                return False
            self._toggle_key = key
            return True

    def toggle(self):
        with self._lock:
            self._running = not self._running
            if self._running:
                self._controller.press(self._hold_key)
            else:
                self._controller.release(self._hold_key)
        self.running_changed.emit(self._running)

    # function to stop key holder
    def stop(self):
        with self._lock:
            if self._running:
                self._controller.release(self._hold_key)
                self._running = False
            self._capturing = False
        if self._listener.running:
            self._listener.stop()

    @property
    def is_running(self):
        with self._lock:
            return self._running

    @property
    def hold_key(self):
        with self._lock:
            return self._hold_key

    @property
    def toggle_key(self):
        with self._lock:
            return self._toggle_key
