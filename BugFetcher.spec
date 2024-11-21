# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['BugFetcher.py'],
    pathex=['/opt/homebrew/Caskroom/miniconda/base/lib/python3.12/site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BugFetcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons.icns'],
)
app = BUNDLE(
    exe,
    name='BugFetcher.app',
    icon='icons.icns',
    bundle_identifier=None,
)
