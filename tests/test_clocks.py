import os

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import tempfile
import unittest
from datetime import datetime

import pytz
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from src.core.timezone_manager import TimezoneManager
from src.ui.converter_widget import ConverterWidget
from src.ui.main_window import MainWindow

app = QApplication.instance() or QApplication([])

class ClockTests(unittest.TestCase):
    def setUp(self):
        self.settings_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.settings_directory.cleanup)
        QSettings.setDefaultFormat(QSettings.IniFormat)
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, self.settings_directory.name)
        self.manager = TimezoneManager()

    def test_current_time_is_same_instant(self):
        value = self.manager.get_current_time_in_timezone('Asia/Shanghai')
        self.assertLess(abs((value - datetime.now(pytz.UTC)).total_seconds()), 2)

    def test_cross_day_conversion(self):
        value = self.manager.convert_time_between_timezones(datetime(2026, 1, 1, 1), 'Asia/Shanghai', 'UTC')
        self.assertEqual(value.strftime('%Y-%m-%d %H:%M'), '2025-12-31 17:00')

    def test_dst_boundaries(self):
        for value, error in [(datetime(2026, 3, 8, 2, 30), pytz.NonExistentTimeError),
                             (datetime(2026, 11, 1, 1, 30), pytz.AmbiguousTimeError)]:
            with self.assertRaises(error):
                self.manager.convert_time_between_timezones(value, 'America/New_York', 'UTC')

    def test_converter_displays_target_wall_time_and_recovers(self):
        widget = ConverterWidget(self.manager)
        widget.source_datetime_edit.setDateTime(widget.wall_datetime(datetime(2026, 1, 1, 1)))
        self.assertEqual(widget.target_datetime_edit.dateTime().toString('yyyy-MM-dd HH:mm'), '2025-12-31 17:00')
        widget.source_timezone_combo.setCurrentText(self.manager.get_timezone_display_name('America/New_York'))
        widget.source_datetime_edit.setDateTime(widget.wall_datetime(datetime(2026, 3, 8, 2, 30)))
        self.assertFalse(widget.target_datetime_edit.isEnabled())
        widget.source_datetime_edit.setDateTime(widget.wall_datetime(datetime(2026, 3, 8, 3, 30)))
        self.assertTrue(widget.target_datetime_edit.isEnabled())
        self.assertEqual(widget.target_datetime_edit.dateTime().toString('HH:mm'), '07:30')
        widget.deleteLater()

    def test_responsive_grid_and_window(self):
        window = MainWindow()
        if not window.timezone_widgets:
            window.add_timezone_widget("Asia/Shanghai")
            window.add_timezone_widget("UTC")
        window.show()
        window.resize(1400, 800)
        app.processEvents()
        panel = window.timezone_display_panel
        wide_columns = panel.columns
        self.assertGreaterEqual(wide_columns, 2)
        window.resize(660, 800)
        app.processEvents()
        from PySide6.QtCore import Qt
        self.assertEqual(window.main_splitter.orientation(), Qt.Vertical)
        self.assertLessEqual(panel.columns, wide_columns)
        self.assertEqual(panel.timezone_layout.count(), len(window.timezone_widgets))
        window.close()

    def test_saved_clocks_and_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            QSettings.setDefaultFormat(QSettings.IniFormat)
            QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, directory)
            window = MainWindow()
            window.add_timezone_by_display_name('Asia/Kolkata')
            window.close()
            restored = MainWindow()
            self.assertIn('Asia/Kolkata', [w.get_timezone_name() for w in restored.timezone_widgets])
            for card in restored.timezone_widgets[:]:
                restored.remove_timezone_widget(card)
            restored.close()
            empty = MainWindow()
            self.assertEqual(empty.timezone_widgets, [])
            empty.close()

if __name__ == '__main__':
    unittest.main()
