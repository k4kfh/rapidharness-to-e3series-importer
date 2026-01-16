# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for RapidHarness to E3.series Importer
This ensures consistent, reproducible builds across all environments
"""

import os
from PyInstaller.utils.hooks import collect_all

# Use os.path.join for cross-platform compatibility
script_path = os.path.join('src', 'from-to-converter.py')
src_path = 'src'

datas = []
binaries = []
hiddenimports = [
    # Standard library
    'csv',
    'pathlib',
    # Third-party packages
    'click',
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.cell._writer',
    'openpyxl.worksheet',
    'openpyxl.workbook',
    'openpyxl.styles',
    'openpyxl.utils',
    'colorama',
    # Local modules
    '__version__',
    'utils',
    'input_parsers',
    'converters',
    'output_writers',
    'models',
]

# Collect all submodules and data files from dependencies
tmp_ret = collect_all('click')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('openpyxl')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('colorama')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    [script_path],
    pathex=[src_path],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='RapidHarnessToE3SeriesImporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX for maximum compatibility
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
