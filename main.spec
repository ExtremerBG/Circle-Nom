# -*- mode: python ; coding: utf-8 -*-


a = Analysis(  # type: ignore
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('image/others/icon.ico', 'image/others'),
        ('sound/effects/nom/nom_1.mp3', 'sound/effects/nom'),
        ('sound/effects/nom/nom_2.mp3', 'sound/effects/nom'),
        ('sound/effects/nom/nom_3.mp3', 'sound/effects/nom'),
        ('sound/effects/nom/nom_4.mp3', 'sound/effects/nom'),
        ('sound/effects/nom/nom_5.mp3', 'sound/effects/nom'),
        ('sound/themes/theme_song_1.mp3', 'sound/themes'),
        ('sound/themes/theme_song_2.mp3', 'sound/themes'),
        ('sound/themes/theme_song_3.mp3', 'sound/themes'),
        ('sound/themes/theme_song_4.mp3', 'sound/themes'),
        ('sound/themes/theme_song_5.mp3', 'sound/themes'),
        ('sound/themes/theme_song_6.mp3', 'sound/themes'),
        ('sound/themes/theme_song_7.mp3', 'sound/themes'),
        ('sound/themes/theme_song_8.mp3', 'sound/themes'),
        ('sound/themes/theme_song_9.mp3', 'sound/themes'),
        ('sound/themes/theme_song_10.mp3', 'sound/themes'),
        ('sound/themes/theme_song_11.mp3', 'sound/themes'),
        ('sound/themes/theme_song_12.mp3', 'sound/themes'),
        ('sound/themes/theme_song_13.mp3', 'sound/themes'),
        ('sound/themes/theme_song_14.mp3', 'sound/themes'),
        ('sound/themes/theme_song_15.mp3', 'sound/themes'),
        ('sound/menu/menu_theme_song_1.mp3', 'sound/menu'),
        ('sound/menu/menu_theme_song_2.mp3', 'sound/menu'),
        ('sound/menu/menu_click_up_down.mp3', 'sound/menu'),
        ('sound/menu/menu_click_left_right.mp3', 'sound/menu'),
        ('sound/menu/menu_click_unknown.mp3', 'sound/menu'),
        ('image/backgrounds/background_image_1.jpg', 'image/backgrounds'),
        ('image/backgrounds/background_image_2.jpg', 'image/backgrounds'),
        ('image/backgrounds/background_image_3.jpg', 'image/backgrounds'),
        ('image/bar/hunger_bar_inner.png', 'image/bar'),
        ('image/bar/hunger_bar_outer.png', 'image/bar'),
        ('image/prey/prey_image_1.png', 'image/prey'),
        ('image/prey/prey_image_2.png', 'image/prey'),
        ('image/prey/prey_image_3.png', 'image/prey'),
        ('image/prey/prey_image_4.png', 'image/prey'),
        ('image/prey/prey_image_5.png', 'image/prey'),
        ('image/prey/prey_image_6.png', 'image/prey'),
        ('image/prey/prey_image_7.png', 'image/prey'),
        ('image/prey/prey_image_8.png', 'image/prey'),
        ('image/prey/prey_image_9.png', 'image/prey'),
        ('image/prey/prey_image_10.png', 'image/prey'),
        ('image/prey/prey_image_11.png', 'image/prey'),
        ('image/prey/prey_aura.png', 'image/prey'),
        ('image/menu/aura.png', 'image/menu'),
        ('image/player_alive/player_image_1.png', 'image/player_alive'),
        ('image/player_alive/player_image_2.png', 'image/player_alive'),
        ('image/player_alive/player_image_3.png', 'image/player_alive'),
        ('image/player_dead/player_image_1_dead.png', 'image/player_dead'),
        ('image/player_dead/player_image_2_dead.png', 'image/player_dead'),
        ('image/player_dead/player_image_3_dead.png', 'image/player_dead'),
        ('image/dagger/flame_dagger_right.gif', 'image/dagger'),
        ('image/dagger/flame_dagger_left.gif', 'image/dagger'),
        ('image/dagger/flame_dagger_up.gif', 'image/dagger'),
        ('image/dagger/flame_dagger_down.gif', 'image/dagger'),
        ('image/dagger/dagger_image_1.png', 'image/dagger'),
        ('sound/effects/dagger/fly/whoosh_1.mp3', 'sound/effects/dagger/fly'),
        ('sound/effects/dagger/fly/whoosh_2.mp3', 'sound/effects/dagger/fly'),
        ('sound/effects/dagger/fly/whoosh_3.mp3', 'sound/effects/dagger/fly'),
        ('sound/effects/dagger/fly/whoosh_4.mp3', 'sound/effects/dagger/fly'),
        ('sound/effects/dagger/fly/whoosh_5.mp3', 'sound/effects/dagger/fly'),
        ('sound/effects/dagger/hit/dagger_ouch_1.mp3', 'sound/effects/dagger/hit'),
        ('sound/effects/dagger/hit/dagger_ouch_2.mp3', 'sound/effects/dagger/hit'),
        ('sound/effects/dagger/hit/dagger_ouch_3.mp3', 'sound/effects/dagger/hit'),
        ('sound/effects/dagger/hit/dagger_ouch_4.mp3', 'sound/effects/dagger/hit'),
        ('sound/effects/dagger/hit/dagger_ouch_5.mp3', 'sound/effects/dagger/hit'),
        ('image/dash/dash_available.png', 'image/dash'),
        ('image/dash/dash_unavailable.png', 'image/dash'),
        ('sound/effects/dash/whoosh_1.mp3', 'sound/effects/dash'),
        ('sound/effects/dash/whoosh_2.mp3', 'sound/effects/dash'),
        ('sound/effects/dash/whoosh_3.mp3', 'sound/effects/dash'),
        ('sound/effects/dash/whoosh_4.mp3', 'sound/effects/dash')
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