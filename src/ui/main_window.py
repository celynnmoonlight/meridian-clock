"""
主窗口模块
定义应用程序的主窗口界面和交互逻辑
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QSplitter, QStatusBar, QWidget

from src.core.settings import AppSettings
from src.core.timezone_manager import TimezoneManager
from src.ui.converter_widget import ConverterWidget
from src.ui.theme import STYLESHEET
from src.ui.timezone_display_panel import TimezoneDisplayPanel
from src.ui.timezone_widget import TimezoneWidget


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.settings = AppSettings()
        self.restoring = True
        self.timezone_manager = TimezoneManager()
        self.timezone_widgets = []  # 存储所有时区卡片实例
        self.setup_ui()
        self.setup_timer()
        self.setup_menu()
        self.setup_status_bar()
        self.add_default_timezones()
        self.restoring = False
        geometry = self.settings.value("geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("Meridian Clock")
        self.setMinimumSize(620, 620)
        self.setStyleSheet(STYLESHEET)
        self.resize(1200, 800)
        
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter = main_splitter
        main_splitter.setChildrenCollapsible(False)
        
        # 左侧面板：时区显示
        self.timezone_display_panel = TimezoneDisplayPanel(self.timezone_manager)
        self.timezone_display_panel.add_timezone_requested.connect(self.add_timezone_by_display_name)
        self.timezone_display_panel.clear_all_requested.connect(self.clear_all_timezones)
        
        # 右侧面板：时区转换器
        right_panel = ConverterWidget(self.timezone_manager)
        right_panel.setMinimumWidth(300)
        
        main_splitter.addWidget(self.timezone_display_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([700, 400])
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.addWidget(main_splitter)
        
    def setup_timer(self):
        """设置定时器, 用于更新所有卡片的时间"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all_times)
        self.timer.start(1000)
        
    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件(&F)")
        exit_action = QAction("退出(&X)", self, shortcut="Ctrl+Q", triggered=self.close)
        file_menu.addAction(exit_action)
        
        timezone_menu = menubar.addMenu("时区(&T)")
        add_action = QAction("添加时区(&A)", self, shortcut="Ctrl+A", triggered=self.timezone_display_panel.on_add_timezone)
        clear_action = QAction("清空所有时区(&C)", self, shortcut="Ctrl+Shift+C", triggered=self.clear_all_timezones)
        timezone_menu.addAction(add_action)
        timezone_menu.addAction(clear_action)
        
        help_menu = menubar.addMenu("帮助(&H)")
        about_action = QAction("关于(&A)", self, triggered=self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
    def add_default_timezones(self):
        """添加配置文件中定义的默认时区"""
        zones = self.settings.value("clocks", self.timezone_manager.get_default_timezones())
        if isinstance(zones, str):
            zones = [zones]
        for tz_name in zones or []:
            if self.timezone_manager.is_valid_timezone(tz_name):
                self.add_timezone_widget(tz_name)
            
    def add_timezone_by_display_name(self, display_name: str):
        """根据显示名称添加时区"""
        tz_name = self.timezone_manager.get_timezone_name_from_display(display_name)
        if tz_name:
            self.add_timezone_widget(tz_name)
        else:
            self.status_bar.showMessage("请选择有效的时区")

    def add_timezone_widget(self, timezone_name: str):
        """创建并添加一个新的时区卡片"""
        if any(widget.get_timezone_name() == timezone_name for widget in self.timezone_widgets):
            QMessageBox.information(self, "提示", f"时区 \"{self.timezone_manager.get_timezone_display_name(timezone_name)}\" 已经存在！")
            return
                
        widget = TimezoneWidget(timezone_name, self.timezone_manager)
        widget.remove_button.clicked.connect(lambda: self.remove_timezone_widget(widget))
        self.timezone_widgets.append(widget)
        self.rearrange_timezone_widgets()
        self.save_clocks()
        self.status_bar.showMessage(f"已添加时区: {self.timezone_manager.get_timezone_display_name(timezone_name)}")
        
    def remove_timezone_widget(self, widget_to_remove: TimezoneWidget):
        """移除一个指定的时区卡片"""
        if widget_to_remove in self.timezone_widgets:
            display_name = self.timezone_manager.get_timezone_display_name(widget_to_remove.get_timezone_name())
            self.timezone_widgets.remove(widget_to_remove)
            self.timezone_display_panel.remove_widget_from_grid(widget_to_remove)
            widget_to_remove.deleteLater()
            self.rearrange_timezone_widgets()
            self.save_clocks()
            self.status_bar.showMessage(f"已移除时区: {display_name}")
            
    def rearrange_timezone_widgets(self):
        """重新排列网格中的所有时区卡片"""
        self.timezone_display_panel.set_cards(self.timezone_widgets)

    def clear_all_timezones(self):
        """清空所有时区显示"""
        reply = QMessageBox.question(self, "确认", "确定要清空所有时区显示吗？",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for widget in self.timezone_widgets[:]:
                self.remove_timezone_widget(widget)
            self.status_bar.showMessage("已清空所有时区")
            
    def update_all_times(self):
        """更新所有时区卡片的时间"""
        for widget in self.timezone_widgets:
            widget.update_time()
            
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于", 
                         "Meridian Clock\n\n"
                         "Meridian Clock contributors\n"
                         "基于: Python + PySide6")
                         
    def save_clocks(self):
        if not self.restoring:
            self.settings.setValue("clocks", [w.get_timezone_name() for w in self.timezone_widgets])

    def closeEvent(self, event):
        self.save_clocks()
        self.settings.setValue("geometry", self.saveGeometry())
        self.timer.stop()
        event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "main_splitter"):
            orientation = Qt.Vertical if self.width() < 950 else Qt.Horizontal
            if self.main_splitter.orientation() != orientation:
                self.main_splitter.setOrientation(orientation)
                self.main_splitter.setSizes([600, 400])
