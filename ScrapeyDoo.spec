# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/__init__.py'],
    pathex=['src'],
    binaries=[],
    datas=[('src/assets', 'assets'), ('src/resources', 'resources')],
    hiddenimports=['settings'],
    hookspath=['src/hooks'],
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
    name='ScrapeyDoo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/assets/ScrapeyDoo.ico'],
)
