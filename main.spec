# -*- mode: python ; coding: utf-8 -*-


a = Analysis(  # type: ignore
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        
        # Image files
        ('image/', 'image'),
        
        # Sound files
        ('sound/', 'sound')
        
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1, # =2 breaks for some reason
)
pyz = PYZ(a.pure)  # type: ignore

exe = EXE(  # type: ignore
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Circle_Nom',
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
    icon=['image/icon/icon.ico'],
)