<!-- markdownlint-disable MD013 MD024 -->

# Changelog

Notable changes to Meridian Clock are recorded here.

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Dates use the YYYY-MM-DD format. Entries describe source versions; packaged releases are not yet available.

## [0.1.0] - 2026-10-07

First public source version of Meridian Clock.

### Added

- Author contact details and a Star History chart in all four README languages.
- Japanese and Korean README translations.
- Language navigation between English, Simplified Chinese, Japanese, and Korean documentation.
- This changelog to track user-facing changes by version.
- World clock cards showing time, date, and UTC offset with updates every second.
- Date and time conversion between configured time zones.
- Search across the full time zone catalog when adding clocks, with 32 Chinese display names.
- Persistent clock lists and window geometry, including support for an empty clock list.
- Responsive card columns and vertical panel arrangement for narrow windows.
- Explanations for ambiguous and nonexistent times during daylight saving transitions.
- Regression tests for time calculations, conversion, persistence, and responsive layout.
- uv project configuration, a pinned Python version, and a dependency lockfile.
- Native build scripts for Windows, macOS, and Linux, with PyInstaller configuration and a Windows Inno Setup installer definition.
- English and Simplified Chinese documentation, an MIT license, and Git ignore and line-ending rules.

### Changed

- Adopted the Meridian Clock product name.
- Centralized visual styles and separated user settings from window code.
- Replaced requirements files with dependency groups in pyproject.toml.

### Fixed

- System local time being incorrectly interpreted as UTC by world clocks.
- Missing display-name lookup preventing users from adding clock cards.
- Converted times being displayed in the system time zone rather than the selected target time zone.
- The current-time shortcut using the system time zone rather than the selected source time zone.

[0.1.0]: https://github.com/celynnmoonlight/meridian-clock/tree/28e958887122f3397191d095fd37f65920920918
