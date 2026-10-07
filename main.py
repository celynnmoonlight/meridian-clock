"""
时区展示与转换器主程序
作者: CodeBuddy
功能: 启动时区展示与转换器应用程序
"""

import sys

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main():
    """主函数，启动应用程序"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")

    # 设置应用程序信息
    app.setApplicationName("Meridian Clock")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("MeridianClock")
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()