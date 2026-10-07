# Meridian Clock

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[Changelog](CHANGELOG.md)

A desktop world clock and time zone converter built with Python and PySide6.

Track time across cities and convert dates and times between time zones in one window. Meridian Clock is an early-stage project working toward an accurate, approachable, and polished desktop experience. The application interface is currently in Chinese.

## Features

- World clock cards displaying time, date, and UTC offset, refreshed every second.
- Automatic conversion when the source time or selected time zones change.
- Add, remove, and clear clock cards.
- Search the full time zone catalog when adding clocks, with 32 built-in Chinese display names.
- Automatically restore the clock list and window geometry between sessions.
- Runs locally without an account or network connection.

The first launch displays Beijing, UTC, London, New York, and Los Angeles. The converter currently offers the configured common time zones.

## Getting started

Dependencies and the Python environment are managed with uv. Python 3.13 is pinned in `.python-version`; `uv.lock` records exact dependency versions.

```bash
uv sync --locked
uv run python main.py
```

Runtime dependencies live in `[project.dependencies]`; development tools live in `[dependency-groups].dev` in `pyproject.toml`.

```bash
# Add or update dependencies
uv add PACKAGE
uv add --dev PACKAGE
uv lock --upgrade
```

## Usage

Use the left panel to select and add clocks. Type a Chinese display name or an English time zone identifier to search. Click × on a card to remove it, or use the clear button to remove all clocks.

Use the right panel to select a source time zone, enter a date and time, and select a target time zone. Results update automatically. The current-time button fills in the current time in the selected source time zone.

Clock preferences are saved locally through Qt settings when clocks change, and window geometry is saved on exit.

## Project structure

```text
.
├── main.py                           # Application entry point
├── pyproject.toml                    # Project metadata and dependency groups
├── uv.lock                           # Locked dependency versions
├── .python-version                   # Python version
├── packaging/                        # PyInstaller and Windows installer configuration
├── scripts/                          # Windows, macOS, and Linux build commands
├── config/
│   ├── timezones.json                # Common time zones and display names
│   └── default_timezones.json        # Initial clock selection
├── src/
│   ├── core/
│   │   ├── settings.py               # User preferences
│   │   └── timezone_manager.py       # Configuration and time zone calculations
│   └── ui/
│       ├── theme.py                  # Shared visual styles
│       ├── main_window.py            # Window, menus, timer, and persistence
│       ├── timezone_display_panel.py # Clock selection and grid
│       ├── timezone_widget.py        # Individual clock card
│       └── converter_widget.py       # Date and time conversion
└── tests/
    └── test_clocks.py                # Core and headless Qt regression tests
```

## Configuration

Edit the `common_timezones` array in `config/timezones.json`:

- `id`: a pytz time zone identifier, such as `Asia/Shanghai`.
- `display_name`: the name shown in the interface.
- `description`: descriptive metadata, currently unused by the interface.
- `utc_offset`: descriptive metadata, not used for calculations. Actual offsets are obtained from pytz.

Edit `config/default_timezones.json` to change the initial clock selection. Saved user preferences override this list on subsequent launches. Restart the application after editing configuration files.

## Development status

World clock calculation, clock addition, target time display, and the current-time shortcut have been corrected.

Ambiguous and nonexistent local times during daylight saving transitions show an explanation and disable the result. Selecting the first or second occurrence of an ambiguous time is not yet supported; choose a time outside the transition interval.

Clock cards adapt their column count to the available width. The main panels switch to a vertical arrangement in narrow windows. Theme styles and user settings are maintained in separate modules. The latest layout and build changes are pending validation.

Run the tests:

```bash
uv run python -m unittest discover -s tests -v
```

Tests cover current time accuracy, conversion across dates, daylight saving boundaries, converter error recovery, and saved clock lists, including an empty list.

## Roadmap

- [x] Correct clock calculation, conversion display, and clock addition.
- [x] Add time zone conversion and daylight saving regression tests.
- [x] Add clock search and persist clock lists and window geometry.
- [x] Add responsive card layout and a shared visual theme.
- [ ] Improve keyboard access, accessibility, and localization.
- [x] Add native build scripts for Windows, macOS, and Linux.
- [ ] Validate and publish packaged desktop releases.

## Contributing

Issues and pull requests are welcome. For time-related bugs, include your system time zone, source and target time zones, and a reproducible date and time.

## License

Licensed under the [MIT License](LICENSE).

## Building desktop applications

```powershell
# Windows portable application directory
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1
# Windows installer (requires Inno Setup 6)
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1 -Installer
```

```bash
# Run on macOS to create .app and .dmg
bash scripts/build-macos.sh
# Run on Linux to create a portable directory and .tar.gz
bash scripts/build-linux.sh
```

Build on the target operating system. Outputs go to `dist/`. These scripts run tests before packaging when invoked. No build was run for the latest changes. See [packaging configuration](packaging/README.md) for details. Signing and macOS notarization are not configured.
