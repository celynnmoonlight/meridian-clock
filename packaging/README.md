<!-- markdownlint-disable MD013 MD024 -->

# 发布配置

本目录只存放构建与安装器配置，不包含应用业务逻辑。

- `meridian.spec`：三平台共用的 PyInstaller 配置，收集程序入口、Qt 依赖、时区配置和许可证。macOS 额外生成 `.app`。
- `windows.iss`：Inno Setup 安装器配置，从 Windows 打包目录生成安装程序，包含开始菜单入口、可选桌面快捷方式和卸载支持。

构建入口位于 `scripts/`：

```powershell
# Windows：独立程序目录
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1
# Windows：同时生成安装器，需要 Inno Setup 6
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1 -Installer
```

```bash
# macOS：独立应用与 DMG
bash scripts/build-macos.sh
# Linux：独立程序目录与 tar.gz
bash scripts/build-linux.sh
```

必须在目标操作系统上构建，PyInstaller 不支持跨系统编译。macOS 产物目前未签名或公证；Windows 安装器也尚未签名。Linux 产物需要桌面系统的图形运行库。

所有生成的文件位于 `dist/`，构建缓存位于 `build/`，均由 Git 忽略。
