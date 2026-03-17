# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for ExtraDataGenerator
# Built by:  build_exe.bat  (or  pyinstaller ExtraDataGenerator.spec)

import sys
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# ── Collect tkinter TCL/TK data and DLLs ─────────────────────────────────────
datas    = []
binaries = []

try:
    datas += collect_data_files('tkinter')
except Exception:
    pass

tcl_dir = Path(sys.base_prefix) / 'tcl'
if tcl_dir.exists():
    for item in tcl_dir.iterdir():
        if item.is_dir():
            datas.append((str(item), item.name))

dlls_dir = Path(sys.base_prefix) / 'DLLs'
if dlls_dir.exists():
    for dll in dlls_dir.glob('*.dll'):
        if dll.stem.lower().startswith(('tcl', 'tk')):
            binaries.append((str(dll), '.'))
    tkpyd = dlls_dir / '_tkinter.pyd'
    if tkpyd.exists():
        binaries.append((str(tkpyd), '.'))

# ── Bundle the icon ────────────────────────────────────────────────────────────
icon_path = Path('icon.ico')
if icon_path.exists():
    datas.append((str(icon_path), '.'))

# ── Analysis ──────────────────────────────────────────────────────────────────
a = Analysis(
    ['generator.py'],
    pathex=[str(Path('.').resolve())],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'gui_gen',
        'core_gen',
        '_tkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.font',
        'pandas',
        'pandas._libs.tslibs.base',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'numpy',
        'openpyxl',
        'openpyxl.styles',
        'openpyxl.utils',
        'et_xmlfile',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'scipy', 'IPython', 'jupyter',
        'PIL', 'cv2', 'PyQt5', 'wx', 'gi',
        'sqlalchemy', 'psycopg2', 'boto3', 'botocore',
        'chardet', 'natsort',
    ],
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
    name='ExtraDataGenerator',
    debug=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)
