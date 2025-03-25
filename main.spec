# -*- mode: python ; coding: utf-8 -*-


a = Analysis(  # type: ignore
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        
        # PyGame Icon
        ('image/others/icon.ico', 'image/others'),
        
        # Background images
        ('image/backgrounds/', 'image/backgrounds'),
        
        # Player alive images
        ('image/player/alive/', 'image/player/alive'),
        
        # Player dead images
        ('image/player/dead/', 'image/player/dead'),
        
        # Player aura image
        ('image/player/aura/player_aura_image.png', 'image/player/aura'),
        
        # Player dash images
        ('image/player/dash/', 'image/player/dash'),
        
        # Player eat SFX
        ('sound/effects/player/eat/', 'sound/effects/player/eat'),
        
        # Player hit SFX
        ('sound/effects/player/hit/', 'sound/effects/player/hit'),
        
        # Player dash SFX
        ('sound/effects/player/dash/', 'sound/effects/player/dash'),
        
        # Prey images
        ('image/prey/', 'image/prey'),
        
        # Dagger images
        ('image/dagger/', 'image/dagger'),
        
        # Dagger SFX
        ('sound/effects/dagger/fly/', 'sound/effects/dagger/fly'),
        
        # Bar images
        ('image/bar/', 'image/bar'),
        
        # In-game themes
        ('sound/themes/in_game/', 'sound/themes/in_game'),
        
        # Menu themes
        ('sound/themes/menu/', 'sound/themes/menu'),
        
        # Menu click SFX
        ('sound/effects/menu/', 'sound/effects/menu'),
        
        # Missing Image/Sound
        ('image/error/missing_image.png', 'image/error'),
        ('sound/error/missing_sound.mp3', 'sound/error')
        
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
    icon=['image/others/icon.ico'],
)