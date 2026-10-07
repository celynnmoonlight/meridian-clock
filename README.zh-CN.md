# 子午线时钟

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[更新日志](CHANGELOG.md)

子午线时钟是一款桌面世界时钟与时区转换工具，帮助你查看不同城市的时间，换算跨时区的日期与时间。项目目前处于原型阶段，目标是逐步发展成准确、易用、美观的桌面应用。

## 当前功能

- 世界时钟卡片：显示时间、日期和 协调世界时偏移，每秒刷新。
- 时区转换：选择源时区和目标时区，修改日期时间后自动换算。
- 时钟管理界面：提供添加、删除和清空卡片的操作。
- 可配置时区：内置 32 个中文时区条目，添加时钟时可搜索完整时区列表。
- 本地运行：无需账户或网络连接，当前界面语言为中文。

默认显示北京、UTC、伦敦、纽约和洛杉矶。时钟列表和窗口尺寸会自动保存，重启后恢复；首次启动使用默认配置。

## 安装与运行

使用 uv 管理 Python 环境和依赖。项目通过 `.python-version` 固定 Python 3.13，通过 `uv.lock` 锁定依赖版本。

```bash
uv sync --locked
uv run python main.py
```

运行依赖定义在 `pyproject.toml` 的 `[project.dependencies]` 中，开发工具定义在 `[dependency-groups].dev` 中。

```bash
# 添加运行依赖
uv add 包名
# 添加开发依赖
uv add --dev 包名
# 更新锁定版本
uv lock --upgrade
```

## 使用方式

左侧为世界时钟面板，可从下拉菜单选择时区并添加卡片，点击卡片上的 × 删除，或使用“清空所有”移除全部卡片。

右侧为时区转换器：选择源时区、设置日期时间，再选择目标时区。修改输入后会自动转换，也可以点击“转换时间”按钮。

添加时钟的下拉框支持输入中文名称或英文时区标识进行搜索。关闭窗口后会自动保存时钟列表。

## 项目结构

```text
.
├── main.py                           # 应用入口
├── pyproject.toml                    # 项目元数据与依赖分组
├── uv.lock                           # 依赖版本锁定
├── .python-version                   # Python 版本
├── packaging/                        # 应用打包与安装器配置
├── scripts/                          # 三平台构建命令
├── config/
│   ├── timezones.json                # 常用时区及显示名称
│   └── default_timezones.json        # 启动时显示的时区
└── src/
    ├── core/
    │   ├── settings.py               # 用户偏好存储
    │   └── timezone_manager.py       # 配置读取与时区计算
    └── ui/
        ├── theme.py                  # 统一视觉主题
        ├── main_window.py            # 主窗口、菜单和刷新定时器
        ├── timezone_display_panel.py # 时区选择和卡片网格
        ├── timezone_widget.py        # 单个时钟卡片
        └── converter_widget.py       # 时区转换界面
```

## 自定义配置

在 `config/timezones.json` 的 `common_timezones` 数组中维护时区条目：

- `id`：pytz 时区标识，例如 `Asia/Shanghai`。
- `display_name`：界面显示名称。
- `description`：描述信息，目前未用于界面。
- `utc_offset`：偏移说明，目前不参与计算；实际偏移由 pytz 获取。

在 `config/default_timezones.json` 中维护启动时显示的时区标识列表。修改配置后需要重启应用。

## 开发状态与已知问题

当前版本已修复世界时钟、添加时区和转换结果显示的问题。“使用当前时间”会读取所选源时区的时间。

夏令时切换中不存在的时间和重复的时间会显示提示并禁用结果；目前需要选择切换区间之外的时间，尚不支持为重复时间指定第一次或第二次。

卡片根据可用宽度自动调整列数，窄窗口中主面板切换为上下布局。视觉主题与用户设置已拆分为独立模块。最新布局及构建修改尚待验证。

运行测试：

```bash
uv run python -m unittest discover -s tests -v
```

## 开发路线

- [x] 修复时间计算、转换显示和添加时区功能。
- [x] 添加时区转换与夏令时边界测试。
- [x] 实现自适应卡片布局与统一视觉主题。
- [x] 支持添加时钟时搜索时区，保存时钟列表与窗口尺寸。
- [ ] 改善键盘操作、无障碍体验和多语言支持。
- [x] 增加 Windows、macOS 和 Linux 构建脚本。
- [ ] 验证并发布桌面安装包。

## 参与贡献

欢迎提交问题、建议或代码合并请求。报告时间相关问题时，请提供系统时区、源时区、目标时区，以及可复现的日期时间。

## 开源许可

本项目采用 [MIT 开源许可证](LICENSE)。

## 桌面应用构建

```powershell
# Windows：独立应用目录
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1
# Windows：安装程序，需要 Inno Setup 6
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1 -Installer
```

```bash
# 在苹果系统生成应用与磁盘映像
bash scripts/build-macos.sh
# 在 Linux 生成独立目录与压缩包
bash scripts/build-linux.sh
```

在目标操作系统上执行构建，产物输出至 `dist/`。脚本执行时会先运行测试再打包；本轮最新修改尚未执行构建。详细说明见[发布配置](packaging/README.md)。目前未配置代码签名与苹果应用公证。
