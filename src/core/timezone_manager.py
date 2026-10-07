"""
时区管理器模块
负责处理时区相关的核心逻辑，包括时区转换、时间计算等
"""

import json
import os
from datetime import datetime
from typing import List, Optional

import pytz


class TimezoneManager:
    """时区管理器类，处理所有时区相关操作"""
    
    def __init__(self):
        """初始化时区管理器"""
        self.common_timezones = []
        self.timezone_display_names = {}
        self.default_timezones = []
        self.load_timezone_config()
    
    def load_timezone_config(self):
        """从JSON配置文件加载时区信息"""
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 1. 加载通用时区配置
        try:
            config_path = os.path.join(current_dir, '..', '..', 'config', 'timezones.json')
            config_path = os.path.normpath(config_path)
            with open(config_path, 'r', encoding='utf-8') as f:
                common_config = json.load(f)
            
            for tz_info in common_config.get('common_timezones', []):
                tz_id = tz_info['id']
                display_name = tz_info['display_name']
                self.common_timezones.append(tz_id)
                self.timezone_display_names[tz_id] = display_name
            
            print(f"成功加载 {len(self.common_timezones)} 个通用时区配置")

        except FileNotFoundError:
            print("错误: 未找到 'timezones.json'。")
        except json.JSONDecodeError:
            print("错误: 解析 'timezones.json' 文件失败。")

        # 2. 加载默认时区配置
        try:
            default_config_path = os.path.join(current_dir, '..', '..', 'config', 'default_timezones.json')
            default_config_path = os.path.normpath(default_config_path)
            with open(default_config_path, 'r', encoding='utf-8') as f:
                self.default_timezones = json.load(f)
            print(f"成功加载 {len(self.default_timezones)} 个默认时区")
        except FileNotFoundError:
            print("警告: 未找到 'default_timezones.json'，将不加载默认时区。")
            self.default_timezones = []
        except json.JSONDecodeError:
            print("错误: 解析 'default_timezones.json' 文件失败。")
            self.default_timezones = []
    
    def get_default_timezones(self) -> List[str]:
        """获取默认时区列表"""
        return self.default_timezones.copy()
    
    def get_all_timezones(self) -> List[str]:
        """获取所有可用的时区列表"""
        return list(pytz.all_timezones)
    
    def get_common_timezones(self) -> List[str]:
        """获取常用时区列表"""
        return self.common_timezones.copy()
    
    def get_timezone_display_name(self, timezone_name: str) -> str:
        """获取时区的显示名称"""
        return self.timezone_display_names.get(timezone_name, timezone_name)
    
    def get_timezone_name_from_display(self, display_name: str) -> Optional[str]:
        for name, label in self.timezone_display_names.items():
            if label == display_name:
                return name
        return display_name if self.is_valid_timezone(display_name) else None

    def get_current_time_in_timezone(self, timezone_name: str) -> Optional[datetime]:
        """获取指定时区的当前时间"""
        try:
            tz = pytz.timezone(timezone_name)
            utc_now = datetime.now(pytz.UTC)
            local_time = utc_now.astimezone(tz)
            return local_time
        except Exception as e:
            print(f"获取时区 {timezone_name} 的时间时出错: {e}")
            return None
    
    def convert_time_between_timezones(self, dt: datetime, from_tz: str, to_tz: str) -> Optional[datetime]:
        """在两个时区之间转换时间"""
        try:
            # 如果输入的datetime没有时区信息，假设它是from_tz时区的时间
            if dt.tzinfo is None:
                from_timezone = pytz.timezone(from_tz)
                dt = from_timezone.localize(dt, is_dst=None)
            
            # 转换到目标时区
            to_timezone = pytz.timezone(to_tz)
            converted_time = dt.astimezone(to_timezone)
            return converted_time
        except (pytz.AmbiguousTimeError, pytz.NonExistentTimeError):
            raise
        except Exception as e:
            print(f"时区转换出错: {e}")
            return None
    
    def get_timezone_offset(self, timezone_name: str) -> Optional[str]:
        """获取时区相对于UTC的偏移量"""
        try:
            tz = pytz.timezone(timezone_name)
            utc_now = datetime.now(pytz.UTC)
            local_time = utc_now.astimezone(tz)
            offset = local_time.strftime('%z')
            # 格式化偏移量显示 (例如: +0800 -> +08:00)
            if len(offset) == 5:
                return f"{offset[:3]}:{offset[3:]}"
            return offset
        except Exception as e:
            print(f"获取时区偏移量出错: {e}")
            return None
    
    def search_timezones(self, keyword: str) -> List[str]:
        """根据关键词搜索时区"""
        keyword = keyword.lower()
        all_timezones = self.get_all_timezones()
        matching_timezones = []
        
        for tz in all_timezones:
            if keyword in tz.lower():
                matching_timezones.append(tz)
        
        return matching_timezones
    
    def is_valid_timezone(self, timezone_name: str) -> bool:
        """检查时区名称是否有效"""
        try:
            pytz.timezone(timezone_name)
            return True
        except (pytz.UnknownTimeZoneError, AttributeError):
            return False