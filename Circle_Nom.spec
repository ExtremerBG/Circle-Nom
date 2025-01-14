# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Circle_Nom.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('images/icon.ico', 'images'),
        ('sounds/nom_1.wav', 'sounds'),
        ('sounds/nom_2.wav', 'sounds'),
        ('sounds/nom_3.wav', 'sounds'),
        ('sounds/nom_4.wav', 'sounds'),
        ('sounds/nom_5.wav', 'sounds'),
        ('sounds/theme_song.wav', 'sounds'),
        ('images/background_image_1.jpg', 'images'),
        ('images/prey_image_0.png', 'images'),
        ('images/prey_image_1.png', 'images'),
        ('images/prey_image_2.png', 'images'),
        ('images/prey_image_3.png', 'images'),
        ('images/prey_image_4.png', 'images'),
        ('images/prey_image_5.png', 'images'),
        ('images/player_image_1.png', 'images')
    ],
    hiddenimports=['pygame', 'random', 'time', 'math', 'sys', 'os', 'game_funcs'],
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
    icon=['images/icon.ico'],
)
