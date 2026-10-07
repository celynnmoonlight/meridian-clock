"""统一的桌面应用主题；组件只负责布局与行为。"""
STYLESHEET = """
QMainWindow { background: #eef2f7; }
QWidget { font-family: 'Microsoft YaHei UI', 'Segoe UI'; font-size: 13px; color: #243247; }
QFrame#clockPanel, QFrame#converterPanel { background: #ffffff; border: 1px solid #dce3ed; border-radius: 12px; }
QFrame#clockCard { background: #f6f9fd; border: 1px solid #dce5f2; border-radius: 12px; }
QLabel { background: transparent; border: none; }
QLabel#sectionTitle { font-size: 20px; font-weight: 600; padding: 8px; }
QComboBox, QDateTimeEdit { background: white; border: 1px solid #cbd5e1; border-radius: 6px; padding: 7px; min-height: 22px; }
QComboBox:focus, QDateTimeEdit:focus { border: 1px solid #3868d9; }
QPushButton { background: #3868d9; color: white; border: none; border-radius: 6px; padding: 9px 12px; }
QPushButton:hover { background: #2854b8; }
QPushButton:pressed { background: #20479c; }
QPushButton:disabled { background: #cbd5e1; }
QPushButton#removeClock { background: #e8edf5; color: #526176; padding: 0; }
QPushButton#removeClock:hover { background: #fee2e2; color: #b42318; }
QGroupBox { border: 1px solid #dce3ed; border-radius: 8px; margin-top: 16px; padding: 16px 10px 10px; font-weight: 600; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; }
QScrollArea { background: transparent; border: none; }
QSplitter::handle { background: #eef2f7; width: 10px; height: 10px; }
QStatusBar { background: #eef2f7; color: #64748b; }
"""
