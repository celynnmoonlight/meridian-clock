"""
时区转换器组件
用于在不同时区之间转换时间
"""

import pytz
from PySide6.QtCore import QDate, QDateTime, Qt, QTime, QTimeZone
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from src.core.timezone_manager import TimezoneManager


class ConverterWidget(QFrame):
    """时区转换器组件类"""
    
    def __init__(self, timezone_manager: TimezoneManager, parent=None):
        """
        初始化时区转换器组件
        
        Args:
            timezone_manager: 时区管理器实例
            parent: 父组件
        """
        super().__init__(parent)
        self.timezone_manager = timezone_manager
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 设置框架样式
        self.setObjectName("converterPanel")
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(1)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("时区转换器")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(16)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        
        # 源时区组
        source_group = QGroupBox("源时区")
        source_layout = QFormLayout()
        
        self.source_timezone_combo = QComboBox()
        self.source_timezone_combo.addItems([
            self.timezone_manager.get_timezone_display_name(tz) 
            for tz in self.timezone_manager.get_common_timezones()
        ])
        self.source_timezone_combo.setCurrentText(
            self.timezone_manager.get_timezone_display_name('Asia/Shanghai')
        )
        
        self.source_datetime_edit = QDateTimeEdit()
        self.source_datetime_edit.setTimeZone(QTimeZone.utc())
        self.source_datetime_edit.setDateTime(self.wall_datetime(self.timezone_manager.get_current_time_in_timezone("Asia/Shanghai")))
        self.source_datetime_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        self.source_datetime_edit.setCalendarPopup(True)
        
        source_layout.addRow("时区:", self.source_timezone_combo)
        source_layout.addRow("时间:", self.source_datetime_edit)
        source_group.setLayout(source_layout)
        
        # 目标时区组
        target_group = QGroupBox("目标时区")
        target_layout = QFormLayout()
        
        self.target_timezone_combo = QComboBox()
        self.target_timezone_combo.addItems([
            self.timezone_manager.get_timezone_display_name(tz) 
            for tz in self.timezone_manager.get_common_timezones()
        ])
        self.target_timezone_combo.setCurrentText(
            self.timezone_manager.get_timezone_display_name('UTC')
        )
        
        self.target_datetime_edit = QDateTimeEdit()
        self.target_datetime_edit.setTimeZone(QTimeZone.utc())
        self.target_datetime_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        self.target_datetime_edit.setReadOnly(True)
        
        target_layout.addRow("时区:", self.target_timezone_combo)
        target_layout.addRow("转换后时间:", self.target_datetime_edit)
        target_group.setLayout(target_layout)
        
        # 转换按钮
        convert_button = QPushButton("转换时间")
        convert_button.clicked.connect(self.convert_time)
        
        # 当前时间按钮
        current_time_button = QPushButton("使用当前时间")
        current_time_button.clicked.connect(self.use_current_time)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(current_time_button)
        button_layout.addWidget(convert_button)
        
        # 添加组件到主布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(source_group)
        main_layout.addWidget(target_group)
        main_layout.addLayout(button_layout)
        self.result_status = QLabel()
        self.result_status.setWordWrap(True)
        main_layout.addWidget(self.result_status)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # 连接信号
        self.source_timezone_combo.currentTextChanged.connect(self.convert_time)
        self.target_timezone_combo.currentTextChanged.connect(self.convert_time)
        self.source_datetime_edit.dateTimeChanged.connect(self.convert_time)
        
        # 初始转换
        self.convert_time()
        
    def get_timezone_name_from_display(self, display_name: str) -> str:
        """从显示名称获取时区名称"""
        for tz_name in self.timezone_manager.get_common_timezones():
            if self.timezone_manager.get_timezone_display_name(tz_name) == display_name:
                return tz_name
        return 'UTC'  # 默认返回UTC
        
    def convert_time(self):
        """执行时区转换"""
        try:
            # 获取源时区和目标时区
            source_tz = self.get_timezone_name_from_display(
                self.source_timezone_combo.currentText()
            )
            target_tz = self.get_timezone_name_from_display(
                self.target_timezone_combo.currentText()
            )
            
            # 获取源时间
            source_qdt = self.source_datetime_edit.dateTime()
            source_dt = source_qdt.toPython().replace(tzinfo=None)
            
            # 执行转换
            converted_time = self.timezone_manager.convert_time_between_timezones(
                source_dt, source_tz, target_tz
            )
            
            if converted_time:
                # 更新目标时间显示
                target_qdt = self.wall_datetime(converted_time)
                self.target_datetime_edit.setDateTime(target_qdt)
                self.target_datetime_edit.setEnabled(True)
                self.result_status.setText(f"{target_tz} · {converted_time.tzname()} · UTC{converted_time.strftime('%z')}")
            else:
                self.show_conversion_error("无法转换，请检查时区和输入时间。")
            
        except pytz.AmbiguousTimeError:
            self.show_conversion_error("该时间因夏令时结束出现两次，请选择切换区间之外的时间。")
        except pytz.NonExistentTimeError:
            self.show_conversion_error("该时间因夏令时开始而不存在，请选择其他时间。")
        except Exception as e:
            self.show_conversion_error(f"转换失败：{e}")
    
    def use_current_time(self):
        """使用当前时间"""
        timezone = self.get_timezone_name_from_display(self.source_timezone_combo.currentText())
        current_qdt = self.wall_datetime(self.timezone_manager.get_current_time_in_timezone(timezone))
        self.source_datetime_edit.setDateTime(current_qdt)
    @staticmethod
    def wall_datetime(value):
        # 编辑器只承载所选时区的钟面值，避免系统时区和夏令时隐式转换。
        return QDateTime(QDate(value.year, value.month, value.day),
                         QTime(value.hour, value.minute, value.second), QTimeZone.utc())

    def show_conversion_error(self, message):
        self.target_datetime_edit.clear()
        self.target_datetime_edit.setEnabled(False)
        self.result_status.setText(message)
