# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.')  # Inclui a logo se existir
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'requests',
        'subprocess',
        'socket',
        'platform',
        'threading',
        're',
        'datetime',
        'os'
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
    name='NetIPShield',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprime o executável
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Mude para True se quiser ver o console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',  # Adicione um ícone se tiver
)