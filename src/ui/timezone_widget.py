"""
时区显示组件
用于显示单个时区的当前时间信息
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout

from src.core.timezone_manager import TimezoneManager


class TimezoneWidget(QFrame):
    """时区显示组件类"""
    
    def __init__(self, timezone_name: str, timezone_manager: TimezoneManager, parent=None):
        """
        初始化时区显示组件
        
        Args:
            timezone_name: 时区名称
            timezone_manager: 时区管理器实例
            parent: 父组件
        """
        super().__init__(parent)
        self.timezone_name = timezone_name
        self.timezone_manager = timezone_manager
        self.setup_ui()
        self.update_time()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setObjectName("clockCard")
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(1)
        
        # 主垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        
        # 顶部布局 (时区名称 + 删除按钮)
        top_layout = QHBoxLayout()
        self.timezone_label = QLabel(self.timezone_manager.get_timezone_display_name(self.timezone_name))
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.timezone_label.setFont(font)
        self.timezone_label.setWordWrap(True)
        
        self.remove_button = QPushButton("×")
        self.remove_button.setFixedSize(28, 28)
        self.remove_button.setObjectName("removeClock")
        self.remove_button.setToolTip("移除时钟")
        self.remove_button.setAccessibleName("移除 " + self.timezone_name)
        
        top_layout.addWidget(self.timezone_label)
        top_layout.addStretch()
        top_layout.addWidget(self.remove_button)
        
        # 中间信息
        self.time_label = QLabel("--:--:--")
        self.time_label.setAlignment(Qt.AlignCenter)
        time_font = QFont("Consolas", 25)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        
        self.date_label = QLabel("----/--/--")
        self.date_label.setAlignment(Qt.AlignCenter)
        date_font = QFont()
        date_font.setPointSize(10)
        self.date_label.setFont(date_font)
        
        self.offset_label = QLabel("UTC+00:00")
        self.offset_label.setAlignment(Qt.AlignCenter)
        offset_font = QFont()
        offset_font.setPointSize(9)
        self.offset_label.setFont(offset_font)
        
        # 添加到主布局
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.date_label)
        main_layout.addWidget(self.offset_label)
        
        # 设置尺寸策略
        self.setMinimumSize(240, 180)
        self.setMaximumHeight(220)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def update_time(self):
        """更新时间显示"""
        current_time = self.timezone_manager.get_current_time_in_timezone(self.timezone_name)
        if current_time:
            self.time_label.setText(current_time.strftime("%H:%M:%S"))
            self.date_label.setText(current_time.strftime("%Y/%m/%d"))
            offset = self.timezone_manager.get_timezone_offset(self.timezone_name)
            if offset:
                self.offset_label.setText(f"UTC{offset}")
        else:
            self.time_label.setText("错误")
            self.date_label.setText("无法获取时间")
            self.offset_label.setText("UTC+00:00")
    
    def get_timezone_name(self) -> str:
        """获取时区名称"""
        return self.timezone_name
