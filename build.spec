# build.spec
block_cipher = None

a = Analysis(
    ['main_pygame.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('mazos_guardados', 'mazos_guardados'),
    ],
    hiddenimports=[
        'pygame', 'websockets', 'asyncio', 'json',
        'carta', 'cartas_data', 'mazos_extra', 'tablero',
        'jugador', 'ia', 'juego', 'ventana', 'sprites',
        'efectos', 'reglas', 'editor_mazos', 'multijugador',
        'online',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PatriaOMuerte',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)