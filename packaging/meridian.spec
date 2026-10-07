# Run from the repository root: uv run pyinstaller packaging/meridian.spec
from pathlib import Path
import sys
root = Path(SPECPATH).parent
analysis = Analysis(
    [str(root / 'main.py')], pathex=[str(root)],
    datas=[(str(root / 'config' / 'timezones.json'), 'config'),
           (str(root / 'config' / 'default_timezones.json'), 'config'),
           (str(root / 'LICENSE'), '.')],
    hiddenimports=[], hookspath=[], runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'tkinter', 'matplotlib', 'numpy', 'pandas'],
    noarchive=False,
)
pyz = PYZ(analysis.pure)
exe = EXE(pyz, analysis.scripts, [], exclude_binaries=True,
          name='MeridianClock', console=False, debug=False, strip=False, upx=False)
collection = COLLECT(exe, analysis.binaries, analysis.datas,
                     strip=False, upx=False, name='MeridianClock')

if sys.platform == 'darwin':
    app = BUNDLE(collection, name='Meridian Clock.app',
                 bundle_identifier='io.meridianclock.desktop',
                 info_plist={'CFBundleShortVersionString': '0.2.0',
                             'NSHighResolutionCapable': True})
