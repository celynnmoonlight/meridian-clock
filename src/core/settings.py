"""用户偏好存储，独立于窗口实现。"""
from PySide6.QtCore import QSettings


class AppSettings:
    def __init__(self):
        self._settings = QSettings("MeridianClock", "MeridianClock")

    def value(self, key, default=None):
        return self._settings.value(key, default)

    def setValue(self, key, value):
        self._settings.setValue(key, value)
