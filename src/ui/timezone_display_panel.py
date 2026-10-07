"""
时区显示面板组件
封装了时区显示相关的所有UI元素和交互
"""

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QCompleter,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class TimezoneDisplayPanel(QFrame):
    """时区显示面板，包含时区选择、添加/清空按钮和时区卡片显示区域"""
    
    # 定义信号，用于通知主窗口用户的操作
    add_timezone_requested = Signal(str)
    clear_all_requested = Signal()

    def __init__(self, timezone_manager, parent=None):
        """
        初始化时区显示面板
        
        Args:
            timezone_manager: 时区管理器实例
            parent: 父组件
        """
        super().__init__(parent)
        self.cards = []
        self.columns = 0
        self.timezone_manager = timezone_manager
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面"""
        self.setFrameStyle(QFrame.StyledPanel)
        
        self.setObjectName("clockPanel")
        layout = QVBoxLayout(self)
        heading = QLabel("世界时钟")
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)
        
        # 1. 创建并添加头部布局
        header_layout = self.create_header_layout()
        layout.addLayout(header_layout)
        
        # 2. 创建并添加时区卡片滚动区域
        scroll_area = self.create_scroll_area()
        layout.addWidget(scroll_area)

    def create_header_layout(self) -> QHBoxLayout:
        """创建面板的头部布局，包含标题、下拉菜单和按钮"""
        header_layout = QHBoxLayout()
        
        # 时区选择器
        self.timezone_combo = QComboBox()
        self.timezone_combo.addItems([
            self.timezone_manager.get_timezone_display_name(tz) 
            for tz in dict.fromkeys(self.timezone_manager.get_common_timezones() + self.timezone_manager.get_all_timezones())
        ])
        
        self.timezone_combo.setEditable(True)
        self.timezone_combo.setInsertPolicy(QComboBox.NoInsert)
        self.timezone_combo.completer().setCaseSensitivity(Qt.CaseInsensitive)
        self.timezone_combo.completer().setFilterMode(Qt.MatchContains)
        self.timezone_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.timezone_combo.setToolTip("输入中文名称或英文时区标识搜索")

        # 添加时区按钮
        add_button = QPushButton("添加时区")
        add_button.clicked.connect(self.on_add_timezone)
        
        # 清空所有按钮
        clear_button = QPushButton("清空所有")
        clear_button.clicked.connect(self.on_clear_all)
        
        header_layout.addWidget(QLabel("选择时区:"))
        header_layout.addWidget(self.timezone_combo, 1)
        header_layout.addWidget(add_button)
        header_layout.addWidget(clear_button)
        
        return header_layout

    def create_scroll_area(self) -> QScrollArea:
        """创建用于显示时区卡片的滚动区域"""
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.viewport().installEventFilter(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 时区显示容器和网格布局
        self.timezone_container = QWidget()
        self.timezone_layout = QGridLayout(self.timezone_container)
        self.timezone_layout.setSpacing(10)
        
        self.timezone_layout.setAlignment(Qt.AlignTop)
        self.empty_label = QLabel("还没有时钟，搜索并添加一个城市开始使用。")
        self.empty_label.setWordWrap(True)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.timezone_layout.addWidget(self.empty_label, 0, 0)

        scroll_area.setWidget(self.timezone_container)
        return scroll_area

    def on_add_timezone(self):
        """处理'添加时区'按钮点击事件，发射信号并传递所选时区的显示名称"""
        display_name = self.timezone_combo.currentText()
        self.add_timezone_requested.emit(display_name)

    def on_clear_all(self):
        """处理'清空所有'按钮点击事件，发射信号"""
        self.clear_all_requested.emit()

    def add_widget_to_grid(self, widget: QWidget, row: int, col: int):
        """向网格布局中添加一个组件"""
        self.timezone_layout.addWidget(widget, row, col)

    def remove_widget_from_grid(self, widget: QWidget):
        """从网格布局中移除一个组件"""
        self.timezone_layout.removeWidget(widget)
    def set_cards(self, cards):
        self.cards = list(cards)
        self.reflow()

    def reflow(self):
        width = self.scroll_area.viewport().width()
        columns = max(1, (width - 18) // 260)
        for column in range(max(self.columns, columns)):
            self.timezone_layout.setColumnStretch(column, 0)
        while self.timezone_layout.count():
            self.timezone_layout.takeAt(0)
        self.columns = columns
        self.empty_label.setVisible(not self.cards)
        if not self.cards:
            self.timezone_layout.addWidget(self.empty_label, 0, 0)
        for index, card in enumerate(self.cards):
            self.timezone_layout.addWidget(card, index // columns, index % columns)
        for column in range(columns):
            self.timezone_layout.setColumnStretch(column, 1)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Resize:
            self.reflow()
        return super().eventFilter(watched, event)
